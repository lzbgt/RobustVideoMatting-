import logging
import os
import subprocess
import time
from PIL import Image
from inference_utils import VideoReader, VideoWriter, ImageSequenceReader
from inference import convert_video
from model import MattingNetwork
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader
from celery import Task, states
from celery.exceptions import Ignore, TaskError
from app.config import celery as capp
from app.payloads import VideoProcessTaskRequest
import torchvision
import torch
import urllib
import traceback
import uuid

logging.info(torch.__version__)
logging.info(torchvision.__version__)


class VideoProc(Task):
    """
    abstract class
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        '''
        avoid multiple loadings of model
        '''
        if not self.model:
            logging.info('model loading')
            self.model = MattingNetwork(
                self.vars[0]).eval().cuda()  # or "resnet50"
            self.model.load_state_dict(torch.load(self.vars[1]))
        return self.run(*args, **kwargs)


@capp.task(ignore_result=False,
           bind=True,
           base=VideoProc,
           vars=('mobilenetv3', 'rvm_mobilenetv3.pth', ),
           name='{}.{}'.format(__name__, 'replace_background')
           )
def replace_background(self, vpRequest: VideoProcessTaskRequest):
    # TODO: avoid same name
    video_url = os.path.basename(vpRequest.video_url)
    bgr_url = os.path.basename(vpRequest.bgr_url)
    _, video_ext = os.path.splitext(video_url)
    _, bgr_ext = os.path.splitext(bgr_url)
    basename = uuid.uuid4().hex
    video_url = f'{basename}{video_ext}'
    bgr_url = f'{uuid.uuid4().hex}{bgr_ext}'
    try:
        uuid.uuid4()
        urllib.request.urlretrieve(vpRequest.video_url, video_url)
        urllib.request.urlretrieve(vpRequest.bgr_url, bgr_url)

        outputname = f'{basename}_out{video_ext}'
        reader = VideoReader(video_url, transform=ToTensor())
        writer = VideoWriter(outputname, frame_rate=30)
        self.update_state(state=states.RECEIVED, meta={'url': ''})

        # probe the video resolution for scaling bgr image
        p = subprocess.Popen('ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 ' +
                             video_url, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        logging.info(f"probe result {output}")
        res = output.decode().split('x')

        # bgr = torch.tensor([.47, 1, .6]).view(3, 1, 1).cuda()  # Green background.
        bgr = Image.open(bgr_url).convert(
            'RGB').resize([int(res[0]), int(res[1])])
        bgr = torch.unsqueeze(ToTensor()(bgr), 0).cuda()
        # Initial recurrent states.
        rec = [None] * 4
        # Adjust based on your video.
        downsample_ratio = 0.25

        with torch.no_grad():
            # RGB tensor normalized to 0 ~ 1.
            for src in DataLoader(reader):
                # Cycle the recurrent states.
                fgr, pha, *rec = self.model(src.cuda(), *rec, downsample_ratio)
                # Composite to green background.
                com = fgr * pha + bgr * (1 - pha)
                writer.write(com)
        return {'url': outputname}
    except Exception as e:
        self.update_state(state=states.FAILURE, meta={
            'url': '',
            'exc_type': type(e).__name__,
            'exc_message': traceback.format_exc(),
        })
        raise Ignore()
    finally:
        os.remove(video_url)
        os.remove(bgr_url)
        os.remove(outputname)
