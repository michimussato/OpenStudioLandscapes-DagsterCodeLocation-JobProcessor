from six import text_typefrom tkinter import image_types[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

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
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.jobs.blender import job
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender.plugin_blender__4_1_1 import plugin

# http://michimussato-fuji.nord/productions/6c5dfed4-0f11-48f7-aba2-4d4d5cce85fc/shots/tasks/9bb09bfa-0a97-40c6-a6e6-27405b198570


job['job_file'] = '/nfs/AWSPortalRoot1/fixtures/blender/sh030_001.blend'
job['plugin_dict'] = plugin
# job['plugin_file'] = f'{os.getenv("PLUGIN_BASE_DIR")}/plugin_blender__4.1.1.py'
job[
  'kitsu_task'] = 'ca153978-9ed2-4d3b-8f54-22584099490a'  # SQ020 / SQ020_SH030  Layout  http://miniboss/productions/6c5dfed4-0f11-48f7-aba2-4d4d5cce85fc/shots/tasks/ca153978-9ed2-4d3b-8f54-22584099490a
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
BASE_DIR="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/062/4_1197-1254_4/"
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
exrinfo "${BASE_DIR}/raw/sh030_001.${START_F}.exr"
oiiotool "${BASE_DIR}/raw/sh030_001.%04d.exr" --origin ${ORIGIN} --fullsize ${FULLSIZE} --create-dir -o "${BASE_DIR}/oiio/sh030_001.%04d.exr"
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


# create exr
oiiotool --create 100x100 6 -o "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/062/4_1197-1254_4/test.exr"

# add bar to new exr
# --fill
# https://openimageio.readthedocs.io/en/latest/oiiotool.html#cmdoption-fill
oiiotool --create 100x100 3 --fill:color=1,0,0 100x10 -o "test.exr"
oiiotool --create 100x100 3 --fill:color=1,0,0 100x10 --fill:color=1,0,0 100x10 -o "test.exr"
# inspect exr
# iv "test.exr"

# --box
# https://openimageio.readthedocs.io/en/latest/oiiotool.html#cmdoption-box
oiiotool \
    --create 100x100 4 \
    --box:color=1.0,0.0,0.0,1.0:fill=1 0,0,100,10 \
    --box:color=1.0,0.0,0.0,1.0:fill=1 0,90,100,100 \
    -o "red_boxes.exr"
    
oiiotool \
    --create 100x100 4 \
    --fill:color=0,0,1,0.2 100x100 \
    -o "bg.exr"

# Replaces bg entirely
oiiotool \
    "red_boxes.exr" \
    "bg.exr" \
    --paste:all=1 +0+0 \
    -o "pasted.exr"
iv "pasted.exr"

oiiotool \
    "red_boxes.exr" --label "fg" \
    "bg.exr" \
    --siappend \
    -o "siappended.exr"
iv "siappended.exr"

oiiotool \
    "red_boxes.exr" \
    "bg.exr" \
    --over \
    -o "over.exr"
iv "over.exr"

# TEST
# take raw render and expand displayWindow
# - WARNING: --ch: Unknown channel name "A", filling with 0 (actual channels: "R,G,B")
oiiotool \
    -i "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/062/4_1197-1254_4/raw/sh030_001.1197.exr" \
    --ch R,G,B,A \
    --origin +0+100 \
    --fullsize 960x740 \
    --create-dir \
    -o "sh030_001.1197.expanded.exr"
# add overlay frame
oiiotool \
    --create 960x740 4 \
    --box:color=1.0,0.0,0.0,1.0:fill=1 0,0,960,100 \
    --box:color=1.0,0.0,0.0,1.0:fill=1 0,640,960,960x740 \
    -o "sh030_001.1197.overlay_frame.exr"
# "over" fg over bg
oiiotool \
    --metamerge \
    -i "sh030_001.1197.overlay_frame.exr" \
    -i "sh030_001.1197.expanded.exr" \
    --over \
    -o "sh030_001.1197.over.exr"
    
# oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr"    
# parse xml with xmllint
oiiotool --info -i:infoformat=xml "sh030_001.1197.over.exr" | xmllint --format -

# avoid  by skipping the first line (-n +2)
# tail: -n +<1+x>
# sed: -n '1d;p'
oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | tail -n +2 - | xmllint --format -
oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | sed -n '1d;p' - | xmllint --format -

# https://devhints.io/xpath
oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | sed -n '1d;p' - | xmllint --format - --xpath '/ImageSpec/channelnames'
oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | sed -n '1d;p' - | xmllint --format - --xpath '//channelnames/channelname'
oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | sed -n '1d;p' - | xmllint --format - --xpath 'string(//channelnames/channelname)'
oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | sed -n '1d;p' - | xmllint --format - --xpath '/ImageSpec/attrib[@name = "Date"]'
oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | sed -n '1d;p' - | xmllint --format - --xpath 'string(/ImageSpec/attrib[@name = "Date"])' 
oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | sed -n '1d;p' - | xmllint --format - --xpath 'string(/ImageSpec/attrib[@name = "Frame"])' 
oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | sed -n '1d;p' - | xmllint --format - --xpath 'string(/ImageSpec/attrib[@name = "cycles.ViewLayer.samples"])' 

# Dealing with XML
# - https://aur.archlinux.org/packages/xml2

# xml2json (sudo pacman -Sy nodejs-xml2json)
oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | sed -n '1d;p' - | xmllint --format - | xml2json | jq --sort-keys --color-output --indent 2

# xml2yaml
# https://goteleport.com/resources/tools/xml-to-yaml-converter/

# Try Python API...

# Paste image 1 on top of image 2
# https://openimageio.readthedocs.io/en/latest/oiiotool.html#cmdoption-paste

# Resources:
# - https://stackoverflow.com/questions/60212362/combine-image-channels-of-two-images-using-oiiotool


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

OIIO Python API
- https://github.com/AcademySoftwareFoundation/OpenImageIO/blob/main/docs/QuickStart.md
- https://openimageio.readthedocs.io/en/v3.1.11.0/pythonbindings.html
- https://openimageio.readthedocs.io/en/v3.1.11.0/

```python
import pathlib
import OpenImageIO as oiio

# from OpenImageIO import ImageInput, ImageOutput
# from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo

raw = pathlib.Path(
  "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/062/4_1197-1254_4/raw/sh030_001.1197.exr")
# with_text = pathlib.Path("/home/michael/sh030_001.1197.text.exr")
expanded = pathlib.Path("/home/michael/sh030_001.1197.expanded.exr")

# High level
# image_raw = oiio.ImageBuf(raw.as_posix())

# Low level
image_raw = oiio.ImageInput.open(raw.as_posix())
spec = image_raw.spec()
# Get metadata:
# - oiiotool -v --info -i:infoformat=xml "sh030_001.1197.over.exr" | sed -n '1d;p' - | xmllint --format - | xml2json | jq --sort-keys --color-output --indent 2
# - https://openimageio.readthedocs.io/en/latest/imageinput.html#arbitrary-metadata
frame = spec.getattribute("Frame", "000")
# or: frame = spec["Frame"]
data_size = spec.image_bytes()

spec["Version"] = "001"
spec["Sequence"] = "SQ030"
spec["Shot"] = "SH010"
spec["Author.email"] = "michimussato@gmail.com"
# read = image_raw.read_image()

# spec.nchannels = 4
# spec.channelnames = ("R", "G", "B", "A")


border = 100
spec.full_height += 2 * border
spec.full_y += -border
spec_out = spec.copy()
# https://openimageio.readthedocs.io/en/latest/imageoutput.html#specially-designated-channels
spec_out.nchannels = 4
spec_out.channelnames = ("R", "G", "B", "A")
spec_out.alpha_channel = 3
# Can't write to ROI? Looks like...
# spec.roi_full.yend = spec.roi_full.yend + 3 * borders

pixels = read = image_raw.read_image()
# Note: read_image will return a NumPy multi-dimensional array holding
# all the pixel values of the image.
output = oiio.ImageOutput.create(expanded.as_posix())

buf = oiio.ImageBuf(spec_out)
# buf.spec().alpha_channel: 1
# buf_over = oiio.ImageBuf(spec_out)
# oiio.ImageBufAlgo.render_box(buf, x1=0, y1=-border, x2=spec.full_width, y2=border, fill=True, color=[1,0,0,1]) or print("error")
oiio.ImageBufAlgo.render_box(buf, x1=0, y1=-border, x2=spec.full_width, y2=border, fill=True, color=[1,0,0,1]) or print("error")
oiio.ImageBufAlgo.render_text(buf, x=200, y=200, text="hello", fontsize=24, textcolor=[1,1,1,1]) or print("error")

# https://openimageio.readthedocs.io/en/latest/imageoutput.html#multi-image-files

buf_raw = oiio.ImageBuf(raw.as_posix())
# buf_raw.spec().alpha_channel: -1
# oiio.ImageBufAlgo.channel_append(buf_raw, "A")
buf_raw2 = oiio.ImageBufAlgo.channels(buf_raw, channelorder=(0, 1, 2, 1.0), newchannelnames=("", "", "", "A"))
# buf_raw2.spec().alpha_channel: 3

# https://openimageio.readthedocs.io/en/latest/imagebufalgo.html
buf_out = oiio.ImageBufAlgo.over(buf, buf_raw2)
# buf_raw.write(expanded.as_posix())
# buf.write(expanded.as_posix())
buf_out.write(expanded.as_posix())

# output.open(expanded.as_posix(), spec)
# output.write_image(buf)
# output.close()
# # text_algo = oiio.ImageBufAlgo(text)
# # text.make_writable()
# # text


# buf.write(buf)



# output.open(expanded.as_posix(), spec)
# output.write_image(pixels)
# output.close()
```


Refactor

```shell
docker exec -it dagster.2026-01-21_17-22-54__seasoned-jelly-wholesale-mixer bash
pip3 install --root-user-action=ignore --editable OpenStudioLandscapes-Dagster-JobProcessor@git+https://github.com/michimussato/OpenStudioLandscapes-Dagster-JobProcessor.git@yaml-migration
```


```python
# exr2png
import pathlib
import OpenImageIO as oiio

# from OpenImageIO import ImageInput, ImageOutput
# from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo

raw = pathlib.Path(
  "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/062/4_1197-1254_4/raw/sh030_001.1197.exr")
expanded = pathlib.Path("/home/michael/sh030_001.1197.expanded.exr")

# High level
# image_raw = oiio.ImageBuf(raw.as_posix())

# Low level
image_raw = oiio.ImageInput.open(raw.as_posix())
spec = image_raw.spec()
# image_raw.
```

```python
import pathlib
import OpenEXR


raw_render = pathlib.Path(
  "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/062/4_1197-1254_4/raw/sh030_001.1197.exr")
header_data = OpenEXR.File(filename=raw_render.as_posix(), header_only=True)
frame = header_data.header()["Frame"]

exrfile = OpenEXR.File(filename=raw_render.as_posix(), separate_channels=True, header_only=False)
exrfile.header(0)["Frame"]
```

```python
import pathlib
import OpenImageIO as oiio

# Step 1: Read RAW Render
raw_render = pathlib.Path(
  "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/062/4_1197-1254_4/raw/sh030_001.1197.exr"
)
raw_image = oiio.ImageInput.open(raw_render.as_posix())
raw_spec = raw_image.spec()
raw_buf = oiio.ImageBuf(raw_render.as_posix())

# Get Metadata
frame = raw_spec.getattribute("Frame")
camera = raw_spec.getattribute("Camera")
resolution = f"{raw_spec.width}x{raw_spec.height}"
render_time = raw_spec.getattribute("RenderTime")
file_ = raw_spec.getattribute("File")

# Don't change anything to the raw_spec. 
# Just set custom metadata.
raw_spec["Show"] = "My Show"
raw_spec["Sequence"] = "SQ030"
raw_spec["Shot"] = "SH010"
raw_spec["Version"] = "001"
raw_spec["Author.email"] = "michimussato@gmail.com"

# Create overlay ImagaBuf
spec_buf_overlay = raw_spec.copy()
spec_buf_overlay.nchannels = 4
spec_buf_overlay.channelnames = ("R", "G", "B", "A")
spec_buf_overlay.alpha_channel = 3
text_overlay_buf = oiio.ImageBuf(spec_buf_overlay)

text_border = 10
overlay_text_size_frame = 24
overlay_text_size_scaledown = 8

pos = int(spec_buf_overlay.y + text_border) + overlay_text_size_frame
oiio.ImageBufAlgo.render_text(
  text_overlay_buf,
  x=text_border,
  # y=int(spec_buf_overlay.full_height - (overlay_text_size_frame / 2)), 
  y=pos,
  text=f"Frame: {frame}",
  fontsize=overlay_text_size_frame,
  textcolor=[1, 1, 1, 1]
) or print("error")

overlay_text_size_camera = overlay_text_size_frame - overlay_text_size_scaledown
pos += text_border + overlay_text_size_camera
oiio.ImageBufAlgo.render_text(
  text_overlay_buf,
  x=10,
  # y=int((spec_buf_overlay.full_height - overlay_text_size_camera) - (overlay_text_size_frame / 2)), 
  y=pos,
  text=f"Camera: {camera}",
  fontsize=overlay_text_size_camera,
  textcolor=[1, 1, 1, 1]
) or print("error")

overlay_text_size_resolution = overlay_text_size_frame - overlay_text_size_scaledown
pos += text_border + overlay_text_size_resolution
oiio.ImageBufAlgo.render_text(
  text_overlay_buf,
  x=10,
  # y=int((spec_buf_overlay.full_height - overlay_text_size_resolution) - (overlay_text_size_resolution / 2)), 
  y=pos,
  text=f"Resolution: {resolution}",
  fontsize=overlay_text_size_resolution,
  textcolor=[1, 1, 1, 1]
) or print("error")

overlay_text_size_rendertime = overlay_text_size_frame - overlay_text_size_scaledown
pos += text_border + overlay_text_size_rendertime
oiio.ImageBufAlgo.render_text(
  text_overlay_buf,
  x=10,
  # y=int((spec_buf_overlay.full_height - overlay_text_size_resolution) - (overlay_text_size_resolution / 2)), 
  y=pos,
  text=f"RenderTime: {render_time}",
  fontsize=overlay_text_size_rendertime,
  textcolor=[1, 1, 1, 1]
) or print("error")

overlay_text_size_file = overlay_text_size_frame - overlay_text_size_scaledown
pos += text_border + overlay_text_size_file
oiio.ImageBufAlgo.render_text(
  text_overlay_buf,
  x=10,
  # y=int((spec_buf_overlay.full_height - overlay_text_size_resolution) - (overlay_text_size_resolution / 2)), 
  y=pos,
  text=f"File: {file_}",
  fontsize=overlay_text_size_rendertime,
  textcolor=[1, 1, 1, 1]
) or print("error")

overlay_text_size_show = overlay_text_size_frame - overlay_text_size_scaledown
pos += text_border + overlay_text_size_show
oiio.ImageBufAlgo.render_text(
  text_overlay_buf,
  x=10,
  # y=int((spec_buf_overlay.full_height - overlay_text_size_resolution) - (overlay_text_size_resolution / 2)), 
  y=pos,
  text=f"Show: {raw_spec.getattribute('Show')}",
  fontsize=overlay_text_size_show,
  textcolor=[1, 1, 1, 1]
) or print("error")

overlay_text_size_shot = overlay_text_size_frame - overlay_text_size_scaledown
pos += text_border + overlay_text_size_shot
oiio.ImageBufAlgo.render_text(
  text_overlay_buf,
  x=10,
  # y=int((spec_buf_overlay.full_height - overlay_text_size_resolution) - (overlay_text_size_resolution / 2)), 
  y=pos,
  text=f"Shot: {raw_spec.getattribute('Sequence')}_{raw_spec.getattribute('Shot')}",
  fontsize=overlay_text_size_shot,
  textcolor=[1, 1, 1, 1]
) or print("error")

text_overlay_buf.write(pathlib.Path(
  "/home/michael/sh030_001.text_overlay.1197.exr"
).as_posix())

# Overlay Handle
box_height = 20
handle_overlay_buf = oiio.ImageBuf(spec_buf_overlay)
frame_is_handle = False
colors = {
  True: [1,0,0,1],
  False: [0,1,0,1]
}
oiio.ImageBufAlgo.render_box(
  handle_overlay_buf, 
  x1=0, 
  y1=spec_buf_overlay.height - box_height, 
  x2=spec_buf_overlay.width, 
  y2=spec_buf_overlay.height, 
  fill=True, 
  color=colors[frame_is_handle]
) or print("error")

handle_overlay_buf.write(pathlib.Path(
  "/home/michael/sh030_001.handle_overlay.1197.exr"
).as_posix())

filename_out = pathlib.Path(
  "/home/michael/sh030_001.out.1197.exr"
)
out = oiio.ImageOutput.create(filename_out.as_posix())
# nsubimages = 1
out.supports("multiimage")  # 1
out.supports("appendsubimage")  # 0

# Appending subimages seems to be difficult.
# Just write the original EXR with some additional metadata
# with the overlays separately.

raw_image_pixels = raw_image.read_image()
out.open(filename_out.as_posix(), raw_spec, "Create")
out.write_image(raw_image_pixels)
out.close()

# out.open(filename_out.as_posix(), raw_spec, "AppendSubimage")
# out.write_image(raw_image_pixels)
# out.close()
```