import moviepy.editor as mpy
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from typing import List
import argparse


# Setting vars
container_size = (1080, 1080)
DEBUG = True

# Collect data from user (video file, image, times)
# TODO: Set argparse

# video, times
# image
def init_argparse():
  parser = argparse.ArgumentParser(
    prog="mkreel.py",
    description="Generate Instagram reels using an image and cuts from a video",   
  )

  parser.add_argument('video', metavar="VIDEO",
                      help="path to video file to make cuts from")
  parser.add_argument('--img', metavar="IMAGE", nargs=1,
                      help="path to image file",
                      required=True,)
  parser.add_argument('--vcut', action="append",
                      nargs=2, metavar="t", required=True,
                      help="start and end times for the video cut (can be multiple)")
  
  return parser


# Generate a video-cuts from sub-clips array
# merge_subclips(video, [(t1, t2), (), ...]) -> vcuts made from sclips array + animation
def concat_vcuts(video: VideoFileClip, cuts: List[list]) -> CompositeVideoClip:
  """Create cuts form the video and concatenate them
  """
  vcuts = [video.subclip(*cut) for cut in cuts]
  merged_v = mpy.concatenate(vcuts)
  return merged_v

# Put things together
def merge_vimg(image: ImageClip, video: CompositeVideoClip, cta=False, vscale=1) -> CompositeVideoClip:
  """Merge the video with image 
  Image: takes the duration from the videos (video/ cta)
  Video: set height x width based on the frame dimensions (image/ length)

  TODO: implement cta, vscale, custom frame dimension
  """
  pass
# 1- Calculate sizes + set positions based on container vars

# 2- Set image + container duration based on vcuts 

# 3- Put things together

# Debug
parser = init_argparse()
args = parser.parse_args()
print(args)
# Export
