[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

---

<!-- TOC -->
* [OpenStudioLandscapes-Dagster-JobProcessor](#openstudiolandscapes-dagster-jobprocessor)
  * [Install into OpenStudioLandscapes-Dagster](#install-into-openstudiolandscapes-dagster)
  * [Demo Jobs](#demo-jobs)
    * [Blender](#blender)
<!-- TOC -->

---

# OpenStudioLandscapes-Dagster-JobProcessor

## Install into OpenStudioLandscapes-Dagster

Add the following code snippet to the
`dagster_code_locations` section in the `config.yml` file of 
[OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster#default-configuration):

```yaml
dagster_code_locations:
  load_from:
  # [...]
  - python_module:
      location_name: OpenStudioLandscapes-Dagster-JobProcessor Package Code Location
      module_name: OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.definitions
      working_directory: src
      pip_path: OpenStudioLandscapes-Dagster-JobProcessor @ git+https://github.com/michimussato/OpenStudioLandscapes-Dagster-JobProcessor.git@main
  # [...]
```

## Demo Jobs

### Blender

```python
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.jobs.blender.job_blender import job
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender.plugin_blender__4_1_1 import plugin


# http://michimussato-fuji.nord/productions/6c5dfed4-0f11-48f7-aba2-4d4d5cce85fc/shots/tasks/9bb09bfa-0a97-40c6-a6e6-27405b198570


job['job_file'] = '/nfs/AWSPortalRoot1/fixtures/blender/sh030_001.blend'
job['plugin_dict'] = plugin
# job['plugin_file'] = f'{os.getenv("PLUGIN_BASE_DIR")}/plugin_blender__4.1.1.py'
job['kitsu_task'] = 'ca153978-9ed2-4d3b-8f54-22584099490a'  # SQ020 / SQ020_SH030  Layout  http://miniboss/productions/6c5dfed4-0f11-48f7-aba2-4d4d5cce85fc/shots/tasks/ca153978-9ed2-4d3b-8f54-22584099490a
job['append_draft_job_png'] = True
job['append_draft_job_mov'] = True
job['with_kitsu_publish'] = True
job['deadline_job_with_draft'] = True
job['render_engine'] = 'CYCLES'
job['comment'] = 'This is Bender job comment'
job['frame_start'] = 1201
job['frame_end'] = 1250
```

## Development/Debugging in Docker Container (OpenStudioLandscapes)

> [!NOTE]
> 
> This operation is non-persistent and changes are
> reverted after container restart.

Force reinstall updated package without re-deployment:

```shell
python3.11 -m pip install --root-user-action=ignore --force-reinstall 'OpenStudioLandscapes-Dagster-JobProcessor @ git+https://github.com/michimussato/OpenStudioLandscapes-Dagster-JobProcessor.git@main'
```

I think, Deadline Draft (even Deadline as a whole) is a dead end.
Start to implement `ffmpeg` for image sequence conversion and preview generation.

Resources:
- [](https://wavespeed.ai/blog/posts/blog-how-to-convert-images-ffmpeg-jpg-png-webp-gif/)
- [](https://en.wikibooks.org/wiki/FFMPEG_An_Intermediate_Guide/image_sequence)
- [](https://medium.com/@maurice.verhoeven/video-with-timecode-burn-in-using-ffmpeg-d5c776bed4cb)
- [](https://linuxvox.com/blog/bash-variable-expansion-in-single-quote-double-quote/)

```shell
# Convert exr image sequence to movie
ffmpeg -start_number 1197 -i sh030_001.%d.exr -vcodec mpeg4 test.avi

# Convert exr image sequence to half scaled png sequence
# https://trac.ffmpeg.org/wiki/Scaling
ffmpeg -start_number 1197 -i sh030_001.%d.exr -vf "scale=iw/2:ih/2" test_out/sh030_001.%d.png
ffmpeg -start_number 1197 -i sh030_001.%04d.exr -vf "scale=iw/2:-1" -start_number 1197 test_out/sh030_001.%04d.png
ffmpeg -start_number 1197 -i sh030_001.%04d.exr -vf "drawtext=: text='%{frame_num}': rate=25: start_number=1197: x=(w-tw)/2:y=h-(2*lh):fontcolor=white:fontsize=50,scale=iw/2:-1" -start_number 1197 test_out/sh030_001.%04d.png
ffmpeg -start_number 1197 -i sh030_001.%04d.exr -vf "drawtext=: text='%{frame_num}': rate=25: start_number=1197: x=(w-tw)/2:y=h-(2*lh):fontcolor=white:fontsize=50,scale=iw/2:-1" -start_number 1197 test_out/sh030_001.%04d.png
ffmpeg -start_number 1197 -i sh030_001.%04d.exr -vf "drawtext=: text='%{frame_num}': rate=25: start_number=1197: x=(w-tw)/2:y=h:fontcolor=white:fontsize=50,scale=iw/2:-1:force_original_aspect_ratio=1,pad=1000:1000" -start_number 1197 test_out/sh030_001.%04d.png
ffmpeg -start_number 1197 -i sh030_001.%04d.exr -vf "scale=iw/2:-1:force_original_aspect_ratio=1,pad=1000:1000,drawtext=: text='%{frame_num}': rate=25: start_number=1197: x=(w-tw)/2:y=h-(2*lh):fontcolor=white:fontsize=50" -start_number 1197 test_out/sh030_001.%04d.png
ffmpeg -start_number 1197 -i sh030_001.%04d.exr -vf "scale=320:240:force_original_aspect_ratio=1,pad=320:240:(( (ow - iw)/2 )):(( (oh - ih)/2 ))" -start_number 1197 test_out/sh030_001.%04d.png
ffmpeg -start_number 1197 -i sh030_001.%04d.exr -vf "scale=320:240:force_original_aspect_ratio=1,pad=320:240:(( (ow - iw)/2 )):(( (oh - ih)/2 )),drawtext=: text='%{frame_num}': rate=25: start_number=1197: x=(w-tw)/2:y=h-(th):fontcolor=white:fontsize=50" -start_number 1197 test_out/sh030_001.%04d.png

ffmpeg -start_number 1197 -i sh030_001.%04d.exr -vf "scale=iw/2:-1:force_original_aspect_ratio=1,pad=iw:ih+60:0:30:blue,drawtext=: text='%{frame_num}': rate=25: start_number=1197: x=(w-tw)/2:y=h-(30-th/2):fontcolor=white:fontsize=20" -start_number 1197 test_out/sh030_001.%04d.png

ffmpeg -start_number 1197 -i sh030_001.%04d.exr -vf "scale=iw/2:-1:force_original_aspect_ratio=1,pad=iw:ih+60:0:30:red,drawtext=: text='%{frame_num}': rate=25: start_number=1197: x=(w-tw)/2:y=h-(30-th/2):fontcolor=white:fontsize=20" -start_number 1197 -frames:v 4 test_out/sh030_001.%04d.png
ffmpeg -start_number 1201 -i sh030_001.%04d.exr -vf "scale=iw/2:-1:force_original_aspect_ratio=1,pad=iw:ih+60:0:30:green,drawtext=: text='%{frame_num}': rate=25: start_number=1201: x=(w-tw)/2:y=h-(30-th/2):fontcolor=white:fontsize=20" -start_number 1201 -frames:v 10 test_out/sh030_001.%04d.png
ffmpeg -start_number 1211 -i sh030_001.%04d.exr -vf "scale=iw/2:-1:force_original_aspect_ratio=1,pad=iw:ih+60:0:30:red,drawtext=: text='%{frame_num}': rate=25: start_number=1211: x=(w-tw)/2:y=h-(30-th/2):fontcolor=white:fontsize=20" -start_number 1211 -frames:v 4 test_out/sh030_001.%04d.png

ffmpeg -start_number 1211 -i sh030_001.%04d.exr -vf "pad=iw:ih+60:0:30:red,drawtext=: text='%{frame_num}': rate=25: start_number=1211: x=(w-tw)/2:y=h-(30-th/2):fontcolor=white:fontsize=20" -start_number 1211 -frames:v 4 test_out/sh030_001.%04d.exr

# set EXR dataWindow
# https://www.greenworm.net/2021/01/22/oiio.html
# https://linux.die.net/man/1/oiiotool
oiiotool "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/033/4_1197-1214_4/sh030_001.1211.exr" --origin 0+60 --fullsize 960x660 -o "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/033/4_1197-1214_4/test_out/sh030_001.oiio.1211.exr"

# Batch Processing (possible pipeline)
BASE_DIR="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/035/4_1197-1254_4/"
FPS=25
START_F=1197
ENF_F=1254
F_TOTAL=$(echo "${ENF_F} - ${START_F} + 1" | bc)
HEAD_H=4
TAIL_H=4
IN_F=$(echo "${START_F} + ${HEAD_H}" | bc)
OUT_F=$(echo "${ENF_F} - ${TAIL_H}" | bc)
BORDERS=100
ORIGIN=$(echo 0+$(echo $((1 * ${BORDERS}))))
FULLSIZE=$(echo 960x$(echo $((2 * ${BORDERS} + 540))))
HEAD_H_IN=${START_F}
CUT_IN=${IN_F}
CUT_OUT=$(echo "${ENF_F} - ${TAIL_H}" | bc)
CUT=$(echo "${CUT_OUT} - ${CUT_IN} + 1" | bc)
TAIL_H_IN=$(echo "${OUT_F} + 1" | bc)

# oiiotool for EXRs
# mkdir -p "${BASE_DIR}/oiio"
exrinfo "${BASE_DIR}/sh030_001.${START_F}.exr"
oiiotool "${BASE_DIR}/sh030_001.%04d.exr" --origin ${ORIGIN} --fullsize ${FULLSIZE} --create-dir -o "${BASE_DIR}/oiio/sh030_001.%04d.exr"
exrinfo "${BASE_DIR}/oiio/sh030_001.${START_F}.exr"

# ffmpeg for Proxies
mkdir -p "${BASE_DIR}/ffmpeg"
#ffmpeg -start_number ${START_F} -i "${BASE_DIR}/oiio_exr/sh030_001.oiio.%04d.exr" -vf "pad=iw:ih+2*${BORDERS}:0:${BORDERS}:red,drawtext=: text='%{frame_num}': rate=25: start_number=1197: x=(w-tw)/2:y=h-(${BORDERS}-th/2):fontcolor=white:fontsize=20,scale=iw/2:-1:force_original_aspect_ratio=1" -start_number ${HEAD_H_IN} -frames:v ${HEAD_H} "${BASE_DIR}/ffmpeg/sh030_001.%04d.png"
# crop
# - https://www.gumlet.com/learn/ffmpeg-crop-video/
mkdir -p "${BASE_DIR}/ffmpeg/png"
mkdir -p "${BASE_DIR}/ffmpeg/png/full"
mkdir -p "${BASE_DIR}/ffmpeg/png/half"
ffmpeg -hide_banner -y -start_number ${START_F}   -i "${BASE_DIR}/oiio/sh030_001.%04d.exr" -vf "crop=in_w:in_h-2*${BORDERS}:0:${BORDERS}, pad=iw:ih+2*${BORDERS}:0:${BORDERS}:red,   drawtext=: text='%{frame_num}': rate=${FPS}: start_number=${HEAD_H_IN}: x=(w-tw)/2:y=h-th:fontcolor=white:fontsize=${BORDERS}, scale=iw:-1:force_original_aspect_ratio=1"   -start_number ${HEAD_H_IN} -frames:v ${HEAD_H} "${BASE_DIR}/ffmpeg/png/full/sh030_001.%04d.png"
ffmpeg -hide_banner -y -start_number ${START_F}   -i "${BASE_DIR}/oiio/sh030_001.%04d.exr" -vf "crop=in_w:in_h-2*${BORDERS}:0:${BORDERS}, pad=iw:ih+2*${BORDERS}:0:${BORDERS}:red,   drawtext=: text='%{frame_num}': rate=${FPS}: start_number=${HEAD_H_IN}: x=(w-tw)/2:y=h-th:fontcolor=white:fontsize=${BORDERS}, scale=iw/2:-1:force_original_aspect_ratio=1" -start_number ${HEAD_H_IN} -frames:v ${HEAD_H} "${BASE_DIR}/ffmpeg/png/half/sh030_001.%04d.png"
ffmpeg -hide_banner -y -start_number ${IN_F}      -i "${BASE_DIR}/oiio/sh030_001.%04d.exr" -vf "crop=in_w:in_h-2*${BORDERS}:0:${BORDERS}, pad=iw:ih+2*${BORDERS}:0:${BORDERS}:green, drawtext=: text='%{frame_num}': rate=${FPS}: start_number=${CUT_IN}: x=(w-tw)/2:y=h-th:fontcolor=white:fontsize=${BORDERS},    scale=iw:-1:force_original_aspect_ratio=1"   -start_number ${CUT_IN}    -frames:v ${CUT}    "${BASE_DIR}/ffmpeg/png/full/sh030_001.%04d.png"
ffmpeg -hide_banner -y -start_number ${IN_F}      -i "${BASE_DIR}/oiio/sh030_001.%04d.exr" -vf "crop=in_w:in_h-2*${BORDERS}:0:${BORDERS}, pad=iw:ih+2*${BORDERS}:0:${BORDERS}:green, drawtext=: text='%{frame_num}': rate=${FPS}: start_number=${CUT_IN}: x=(w-tw)/2:y=h-th:fontcolor=white:fontsize=${BORDERS},    scale=iw/2:-1:force_original_aspect_ratio=1" -start_number ${CUT_IN}    -frames:v ${CUT}    "${BASE_DIR}/ffmpeg/png/half/sh030_001.%04d.png"
ffmpeg -hide_banner -y -start_number ${TAIL_H_IN} -i "${BASE_DIR}/oiio/sh030_001.%04d.exr" -vf "crop=in_w:in_h-2*${BORDERS}:0:${BORDERS}, pad=iw:ih+2*${BORDERS}:0:${BORDERS}:red,   drawtext=: text='%{frame_num}': rate=${FPS}: start_number=${TAIL_H_IN}: x=(w-tw)/2:y=h-th:fontcolor=white:fontsize=${BORDERS}, scale=iw:-1:force_original_aspect_ratio=1"   -start_number ${TAIL_H_IN} -frames:v ${TAIL_H} "${BASE_DIR}/ffmpeg/png/full/sh030_001.%04d.png"
ffmpeg -hide_banner -y -start_number ${TAIL_H_IN} -i "${BASE_DIR}/oiio/sh030_001.%04d.exr" -vf "crop=in_w:in_h-2*${BORDERS}:0:${BORDERS}, pad=iw:ih+2*${BORDERS}:0:${BORDERS}:red,   drawtext=: text='%{frame_num}': rate=${FPS}: start_number=${TAIL_H_IN}: x=(w-tw)/2:y=h-th:fontcolor=white:fontsize=${BORDERS}, scale=iw/2:-1:force_original_aspect_ratio=1" -start_number ${TAIL_H_IN} -frames:v ${TAIL_H} "${BASE_DIR}/ffmpeg/png/half/sh030_001.%04d.png"

# https://gist.github.com/aadm/661ff15f6b23f1d58c14c87c9a5ed9e0
mkdir -p "${BASE_DIR}/ffmpeg/h264"
mkdir -p "${BASE_DIR}/ffmpeg/h264/full"
#ffmpeg -framerate ${FPS} -start_number ${START_F} -i "${BASE_DIR}/ffmpeg/sh030_001.%04d.png" -frames:v ${F_TOTAL} -vcodec h264 -c:v libx264 -pix_fmt yuv420p out.mp4
ffmpeg -hide_banner -y -framerate ${FPS} -start_number ${START_F} -i "${BASE_DIR}/ffmpeg/png/full/sh030_001.%04d.png" -vcodec h264 -pix_fmt yuv420p "${BASE_DIR}/ffmpeg/h264/full/sh030_001.mp4"

# tw: text width
# th: text height

# Burn in Demo
ffmpeg -loop 1 -framerate 25 -t 10 -i sh030_001.1197.exr -vf "drawtext=:text='%{pts\:hms}':rate=25:start_number=0:x=(w-tw)/2:y=h-(3*lh):fontcolor=white:fontsize=50,drawtext=:text='%{eif\:mod(n\,25)\:d}':rate=25:start_number=0:x=(w-tw)/2:y=h-(2*lh):fontcolor=white:fontsize=50" -c:v libx264 -pix_fmt yuv420p -tune stillimage -r 25 -s 1920x1280 output.mp4
ffmpeg -framerate 25 -start_number 1197 -i sh030_001.%04d.exr -vf "drawtext=:text='%{pts\:hms}':rate=25:start_number=1197:x=(w-tw)/2:y=h-(3*lh):fontcolor=white:fontsize=50,drawtext=:text='%{eif\:mod(n\,25)\:d}':rate=25:start_number=1197:x=(w-tw)/2:y=h-(2*lh):fontcolor=white:fontsize=50" -c:v libx264 -pix_fmt yuv420p -tune stillimage -r 25 -s 1920x1280 output.mp4
ffmpeg -framerate 25 -start_number 1197 -i sh030_001.%04d.exr -vf "drawtext=:text='%{eif\:mod(n\,25)\:d}':rate=25:start_number=1197:x=(w-tw)/2:y=h-(2*lh):fontcolor=white:fontsize=50" -c:v libx264 -pix_fmt yuv420p -tune stillimage -r 25 -s 1920x1280 output.mp4

export FPS=25
export START=1197
ffmpeg -framerate ${FPS} -start_number ${START} -i sh030_001.%04d.exr -vf "drawtext=: text='%{frame_num}': rate=${FPS}: start_number=${START}: x=(w-tw)/2:y=h-(2*lh):fontcolor=white:fontsize=50" -c:v libx264 -pix_fmt yuv420p -tune stillimage -r ${FPS} -s 1920x1280 output.mp4

export FPS="25" START="1197"; ffmpeg -framerate "${FPS}" -start_number "${START}" -i sh030_001.%04d.exr -vf "drawtext=: text='%{frame_num}': rate='${FPS}': start_number='${START}': x=(w-tw)/2:y=h-(2*lh):fontcolor=white:fontsize=50" -c:v libx264 -pix_fmt yuv420p -tune stillimage -r ${FPS} -s 1920x1280 output.mp4
FPS="25" START="1197" && ffmpeg -framerate "${FPS}" -start_number "${START}" -i sh030_001.%04d.exr -vf "drawtext=: text='%{frame_num}': rate='${FPS}': start_number='${START}': x=(w-tw)/2:y=h-(2*lh):fontcolor=white:fontsize=50" -c:v libx264 -pix_fmt yuv420p -tune stillimage -r ${FPS} -s 1920x1280 output.mp4
```


Refactor

```shell
docker exec -it dagster.2026-01-21_17-22-54__seasoned-jelly-wholesale-mixer bash
pip3 install --root-user-action=ignore --editable OpenStudioLandscapes-Dagster-JobProcessor@git+https://github.com/michimussato/OpenStudioLandscapes-Dagster-JobProcessor.git@yaml-migration
```