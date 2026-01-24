<!-- TOC -->
* [OpenStudioLandscapes-Dagster-JobProcessor](#openstudiolandscapes-dagster-jobprocessor)
  * [Install into OpenStudioLandscapes-Dagster](#install-into-openstudiolandscapes-dagster)
<!-- TOC -->

---

# OpenStudioLandscapes-Dagster-JobProcessor

## Install into OpenStudioLandscapes-Dagster

Add the following code snippet to the
`dagster_code_locations` section:

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
