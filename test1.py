import torch
import torchvision
# print(torch.__version__)
# print(torchvision.__version__)

from model import MattingNetwork
from inference import convert_video

model = MattingNetwork('mobilenetv3').eval().cuda()  # or "resnet50"
model.load_state_dict(torch.load('rvm_mobilenetv3.pth'))

convert_video(
    model,  # The model, can be on any device (cpu or cuda).
    input_source='images',  # A video file or an image sequence directory.
    output_type='video',  # Choose "video" or "png_sequence"
    output_composition='out2.mp4',  # File path if video; directory path if png sequence.
    output_video_mbps=2,  # Output video mbps. Not needed for png sequence.
    downsample_ratio=0.6,  # A hyperparameter to adjust or use None for auto.
    seq_chunk=8,  # Process n frames at once for better parallelism.
    num_workers=0,
)
