import moviepy.editor as mpy
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from typing import List
import argparse


# Setting vars
# current container size is determined by image width
# TODO: set custom container size
# container_size = (1080, 1080)
DEBUG = True

def init_argparse():
  parser = argparse.ArgumentParser(
    prog="mkreel.py",
    description="Generate Instagram reels using an image and cuts from a video",   
  )

  parser.add_argument('video', metavar="VIDEO",
                      help="path to source video file")
  parser.add_argument('--img', metavar="IMAGE", nargs="?",
                      help="path to source image file",
                      required=True,)
  parser.add_argument('--vcut', action="append", dest="vcuts",
                      nargs=2, metavar="t", required=True,
                      help="""start and end times for the video cut
                        (use multiple times for multiple cuts)""")
  parser.add_argument('--auto-crop', default=False, action='store_true',
                      help="crop cuts to fit all available space next to image")
  parser.add_argument('-d','--disable-transition', default=False, action="store_true",
                      help='disable transition when merging multiple video cuts')
  parser.add_argument('-o', '--output', default=False,
                      metavar="OUTPUT", nargs="?",
                      help="path to output file, omit to show preview instead")
  
  return parser


def concat_vcuts(video: VideoFileClip, cuts: List[list], transition: bool) -> CompositeVideoClip:
  """Create cuts form the video and concatenate them
  TODO: implement transition animation
  """
  # set transition speed
  transpd = 0.2

  pre_vcuts = [video.subclip(*cut) for cut in cuts]
  
  if transition and len(pre_vcuts) > 1:
    vcuts = [
      pre_vcuts[0].crossfadeout(transpd),
      *[v.crossfadein(transpd).crossfadeout(transpd) for v in pre_vcuts[1:-1]],
      pre_vcuts[-1].crossfadein(transpd)
    ]
  else:
    vcuts = pre_vcuts
  
  merged_v = mpy.concatenate(vcuts)
  return merged_v


def merge_vimg(image: ImageClip, video: CompositeVideoClip, 
               auto_crop: bool, cta=False,) -> CompositeVideoClip:
  """Merge the video with image 
  Image: takes the duration from the videos (video/ cta)
  Video: set height x width based on the frame dimensions (image/ length)
  Auto_crop: fit video into available space

  TODO: implement cta, custom frame dimension
  """
  # set vars
  container_size = image.w
  full_duration = video.duration

  # set container
  container = ColorClip(size=(container_size, container_size), 
                        color=(255,255,255)).set_duration(full_duration)
  
  # set video
  # space left for video
  vspace = (container_size - image.h, container_size)
  video = adjust_video(video=video, container=vspace, auto_crop=auto_crop)

  # set image
  image = image.set_duration(full_duration)
  image = image.set_position(("center", "bottom"))
  

  return CompositeVideoClip([container, video, image])


def adjust_video(video: CompositeVideoClip, container: tuple, auto_crop=False):
  """Adjust video to fit into a container space
  use auto_crop to force fixing aspect ratio
  """
  ch, cw = container
  # try to adjust by height
  vtemp = video.resize(height=ch)

  # if result matches requirements
  if ((vtemp.w <= cw and not auto_crop) or 
      (vtemp.w >= cw and auto_crop)):
    return vtemp.set_position(("center", "top"))

  elif ((vtemp.w <= cw and auto_crop) or 
        (vtemp.w >= cw and not auto_crop)):
    # if not, adjust by width
    vtemp = video.resize(width=cw)
    if auto_crop:
      # move video up to see subtitles if found
      overlap = ch - vtemp.h
      return vtemp.set_position(("center",overlap))
    else:
      return vtemp.set_position(("center", "top"))


if __name__ == "__main__":
  parser = init_argparse()
  args = parser.parse_args()

  if DEBUG:
    print(args)

  vidfile = VideoFileClip(args.video)
  cuts_times = args.vcuts
  enable_transition = not args.disable_transition

  vcuts = concat_vcuts(vidfile, cuts_times, transition=enable_transition)

  myimg = ImageClip(args.img)

  myclip = merge_vimg(image=myimg, video=vcuts, auto_crop=args.auto_crop)


  output = args.output
  if not output:
    print("InstaReelPy - no output file specified, previewing ..")

    # fixing an audio related bug
    aud = myclip.audio.set_fps(44100)
    myclip = myclip.without_audio().set_audio(aud)
    
    myclip.resize(0.3).preview(fps=5, audio=True)
  else:
    # export reel
    myclip.write_videofile(output)
    print(f"InstaReelPy - Finished generating reel, file: {output}")
