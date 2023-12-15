import os
from pathlib import Path

project_root = os.path.dirname(__file__)
dirname = os.path.join(Path(project_root).resolve().parents[0], 'static/videos')
playlist = f"playlist.txt"
key = 'rtmp://a.rtmp.youtube.com/live2/qxbg-sdbd-7xt2-5fyt-2ru7' 
# key = 'rtmp://a.rtmp.youtube.com/live2/106t-yr8r-5vde-m0a9-bkqr'
# key = 'rtmp://a.rtmp.youtube.com/live2/fmda-45k8-dugw-7jum-4k6v'
#key = 'rtmp://a.rtmp.youtube.com/live2/uda9-0f1x-dmbk-x4sf-2pxu'

# while True: 
#     files = os.listdir(dirname)  
#     for f in files: 
#         if ".mp4" in f: 
#                 cmd = "ffmpeg -threads 3  -re -i " + dirname + f + " -b:v 700k -maxrate 5000k -bufsize 3000k -c:v libx264 -preset ultrafast -crf 24 -g 3 -b:a 128k -f flv " + key
#         #     "ffmpeg -threads 3  -re -i " + dirname + f + " -b:v 700k -c:v libx264 -preset veryfast -crf 24 -g 3 -b:a 128k -f flv " + key
#                 os.system(cmd)
while True:
        cmd = "ffmpeg -threads 3 -f concat -safe 0 -re -i " + playlist + " -r 30 -b:v 700k -maxrate 5000k -bufsize 3000k -c:v libx264 -x264-params keyint=60:scenecut=0 -preset ultrafast -crf 24 -g 3 -b:a 128k -f flv " + key 
        os.system(cmd)
