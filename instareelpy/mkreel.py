import moviepy.editor as mpy
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip, ColorClip
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
def merge_vimg(image: ImageClip, video: CompositeVideoClip, auto_crop: bool, cta=False,) -> CompositeVideoClip:
  """Merge the video with image 
  Image: takes the duration from the videos (video/ cta)
  Video: set height x width based on the frame dimensions (image/ length)
  Auto_crop: 

  TODO: implement cta, custom frame dimension
  """
  # set vars
  container_size = image.w
  full_duration = video.duration

  # set container
  container = ColorClip(size=(container_size, container_size), 
                        color=(255,255,255)).set_duration(full_duration)
  
  # set video
  # if not auto_crop:
  #   # safe scale of video
  #   v_height = container_size - image.h
  #   video = video.resize(height=v_height)
  #   video = video.set_position(("center", "top"))
  # else:
  #   # full free space allocation (crop if necessary)
  #   video = video.resize(width=container_size)
  #   overlap = image.h + video.h - container_size
  #   video = video.set_position(("center",-overlap))

  # left space for video
  vspace = (container_size - image.h, container_size)
  video = adjust_video(video=video, container=vspace, auto_crop=True)

  # set image
  image = image.set_duration(full_duration)
  image = image.set_position(("center", "bottom"))
  

  return CompositeVideoClip([container, video, image])

def adjust_video(video: CompositeVideoClip, container: tuple, auto_crop=False):
  """Adjust video to fit into a container space
  use auto_crop to force fixing aspect ratio
  """
  ch, cw = container
  # try to adjust by height (as it's safer)
  vtemp = video.resize(height=ch)
  # if vwidth < container and no crop -> done
  # elif vwidth > container and crop -> done
  if ((vtemp.w <= cw and not auto_crop) or 
      (vtemp.w >= cw and auto_crop)):
    return vtemp.set_position(("center", "top"))


  # elif vwidth < container and crop -> adjust by width
  # elif vwidh > container and no crop -> adjust by width
  elif ((vtemp.w <= cw and auto_crop) or 
        (vtemp.w >= cw and not auto_crop)):
    vtemp = video.resize(width=cw)
    if auto_crop:
      # move video up to see subtitles
      overlap = ch - vtemp.h
      return vtemp.set_position(("center",overlap))
    else:
      return vtemp.set_position(("center", "top"))

# Debug
parser = init_argparse()
args = parser.parse_args()
print(args)
# Export
