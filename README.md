# instaReelPy
Generate Instagram reels from image frames and video cuts. 

![](instareelpy_cover.png)

## Install
```bash
git clone https://github.com/MossabDiae/instaReelPy.git
cd instaReelPy/instareelpy/

# install dependencies
pip install -r requirements.txt 
```

## Usage

* basic usage (preview only)
```
python mkreel.py input_video.mp4 --img input_img.png --vcut start_time end_time 
```

* output to a file: `-o`
```
python mkreel.py input_video.mp4 --img input_img.png --vcut start_time end_time -o output_reel.mp4
```

* use `--auto-crop` to crop video until fit in available space
```
python mkreel.py input_video.mp4 --img input_img.png --vcut start_time end_time --auto-crop -o output_reel.mp4 
```

* use `--vcut` multiple times to make and concatenate multiple cuts from same input video
```
python mkreel.py input_video.mp4 --img input_img.png --vcut start_time end_time　--vcut start_time2 end_time2 --auto-crop -o output_reel.mp4 
```


* show help
```
python mkreel.py -h
```

