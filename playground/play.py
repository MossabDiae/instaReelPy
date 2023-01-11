from moviepy.editor import *


vidfile = VideoFileClip("vid.mp4")

myvid = vidfile.subclip("11:59","12:09")
myvid = myvid.set_position(("center","top"))
myvid = myvid.resize(width=1080)

myimg = ImageClip("img.png").set_duration(3)

myclip = CompositeVideoClip([myimg, myvid])



# The following previw methods need pygame to be installed
# pip install pygame
# show one frame at x second
# myclip.resize(0.3).show(2,interactive=True)

# preview the whole clip
# fix an audio-related bug
# aud = myclip.audio.set_fps(44100)
# myclip = myclip.without_audio().set_audio(aud)
# myclip.resize(0.3).preview()
# ------------
# Quick fast previews (no audio)
myclip.resize(0.3).preview(fps=10, audio=False)

# export
# myclip.write_videofile("movie.mp4")

print(type(myclip))