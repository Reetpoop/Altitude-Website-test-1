Put your video files and photos in this folder.

VIDEO — recommended encode
  Desktop loop : MP4 (H.264), 1920x1080, <= 4 MB, no audio track
  Mobile loop  : MP4 (H.264), 1280x720,  <= 2 MB
  Long films   : MP4 (H.264), 1080p, audio included, any length
  ffmpeg example:
    ffmpeg -i raw.mov -c:v libx264 -crf 26 -an -vf scale=1920:-2 \
           -movflags +faststart facade-wash.mp4
  The -movflags +faststart matters: without it the browser downloads the
  whole file before showing frame one.

POSTER IMAGES
  One still per video, same aspect ratio, <= 150 KB, .jpg or .webp.
  The poster is what loads first and what Google measures, so always set it.

BEFORE / AFTER
  Shoot from a tripod in the same position at the same time of day.
  Name them before-<building>.jpg and after-<building>.jpg
