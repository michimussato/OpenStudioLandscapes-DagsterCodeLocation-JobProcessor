from six import text_typefrom tkinter import image_types[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

---

<!-- TOC -->
* [OpenStudioLandscapes-Dagster-JobProcessor](#openstudiolandscapes-dagster-jobprocessor)
  * [Install into OpenStudioLandscapes-Dagster](#install-into-openstudiolandscapes-dagster)
  * [Demo Jobs](#demo-jobs)
    * [Blender](#blender)
  * [Development/Debugging in Docker Container (OpenStudioLandscapes)](#developmentdebugging-in-docker-container-openstudiolandscapes)
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
      location_name: OpenStudioLandscapes-DagsterCodeLocation-JobProcessor Package Code Location
      module_name: OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.definitions
      working_directory: src
      pip_path: OpenStudioLandscapes-DagsterCodeLocation-JobProcessor @ git+https://github.com/michimussato/OpenStudioLandscapes-DagsterCodeLocation-JobProcessor.git@main
  # [...]
```

## Demo Jobs

### Blender

```yaml
job_file: /data/share/AWSPortalRoot1/fixtures/blender/sh030_001.blend
plugin_model:
  plugin_type: PluginBlender_4_1_1
  render_engine: CYCLES
deadline_initial_status: Active
kitsu_task: b0cfdac7-afa9-4382-a75d-3c80a388e136  # SQ010 / SQ010_SH030  Rendering  https://kitsu.pangolin.openstudiolandscapes.cloud-ip.cc/productions/3ede4117-b73c-4bd3-83a2-40d66bc954c5/shots/tasks/b0cfdac7-afa9-4382-a75d-3c80a388e136
append_draft_job_png: true
append_draft_job_mov: true
with_kitsu_publish: true
deadline_job_with_draft: true
comment: This is a new Bender job comment
cut_in: 1201  # frame_start
cut_out: 1250  # frame_end
```

## Development/Debugging in Docker Container (OpenStudioLandscapes)

> [!NOTE]
> 
> This operation is non-persistent and changes are
> reverted after container restart.

Force reinstall updated package without re-deployment:

```shell
python3.11 -m pip install --root-user-action=ignore --force-reinstall 'OpenStudioLandscapes-DagsterCodeLocation-JobProcessor @ git+https://github.com/michimussato/OpenStudioLandscapes-DagsterCodeLocation-JobProcessor.git@yaml-migration'
```

> [!TIP]
> 
> Reinstall this package inside the container it was deployed to:
> 
> ```shell
> docker exec -it dagster.2026-01-21_17-22-54__seasoned-jelly-wholesale-mixer bash
> pip3 install --root-user-action=ignore --editable 'OpenStudioLandscapes-DagsterCodeLocation-JobProcessor @ git+https://github.com/michimussato/OpenStudioLandscapes-DagsterCodeLocation-JobProcessor.git@main'
> ```
