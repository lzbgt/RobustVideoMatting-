import torch
import torchvision
print(torch.__version__)
print(torchvision.__version__)

from torch.utils.data import DataLoader
from model import MattingNetwork
from inference import convert_video
from torchvision.transforms import ToTensor
from inference_utils import VideoReader, VideoWriter, ImageSequenceReader
from PIL import Image
import time
import subprocess
import os

model = MattingNetwork('mobilenetv3').eval().cuda()  # or "resnet50"
model.load_state_dict(torch.load('rvm_mobilenetv3.pth'))

# convert_video(
#     model,  # The model, can be on any device (cpu or cuda).
#     input_source='images',  # A video file or an image sequence directory.
#     output_type='video',  # Choose "video" or "png_sequence"
#     output_composition='out2.mp4',  # File path if video; directory path if png sequence.
#     output_video_mbps=2,  # Output video mbps. Not needed for png sequence.
#     downsample_ratio=0.6,  # A hyperparameter to adjust or use None for auto.
#     seq_chunk=8,  # Process n frames at once for better parallelism.
#     num_workers=0,
# )

filename = 'input.mp4'
basename,_ =  os.path.splitext(filename)
outputname = basename + '_output.mp4'
reader = VideoReader(filename, transform=ToTensor())
writer = VideoWriter(outputname, frame_rate=30)

# probe the video resolution
p = subprocess.Popen('ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 ' + filename, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
if err:
    exit()

res = output.decode().split('x')

#bgr = torch.tensor([.47, 1, .6]).view(3, 1, 1).cuda()  # Green background.
bgr = Image.open("bgr.jpg").convert('RGB').resize([int(res[0]), int(res[1])])
bgr = torch.unsqueeze(ToTensor()(bgr), 0).cuda()
rec = [None] * 4                                       # Initial recurrent states.
downsample_ratio = 0.25                                # Adjust based on your video.

with torch.no_grad():
    for src in DataLoader(reader):                     # RGB tensor normalized to 0 ~ 1.
        fgr, pha, *rec = model(src.cuda(), *rec, downsample_ratio)  # Cycle the recurrent states.
        com = fgr * pha + bgr * (1 - pha)              # Composite to green background. 
        writer.write(com)                              # Write frame.
