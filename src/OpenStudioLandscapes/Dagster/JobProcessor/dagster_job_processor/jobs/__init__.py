from dagster import AssetSelection, define_asset_job, AssetKey

from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.assets.read_yaml import ASSET_HEADER_JOB_PROCESSOR, ASSET_HEADER_JOB_PROCESSOR_READER
from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.assets.submit_jobs import ASSET_HEADER_JOB_SUBMITTER


# Asset Selections
submit_jobs_selection = AssetSelection.assets(
    AssetKey([*ASSET_HEADER_JOB_SUBMITTER["key_prefix"], "submit_job"]),
)
# # ingest_jobs_job = AssetSelection.assets("ingest_job")
# read_job_selection = AssetSelection.assets(
#     AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "read_job_py"]),
# )
# ingest_jobs_job = AssetSelection.assets("ingest_job")
read_job_selection_yaml = AssetSelection.assets(
    AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"]),
)


submit_synced_jobs = define_asset_job(
    name="submit_jobs_job",
    selection=submit_jobs_selection,
)


# ingest_synced_jobs = define_asset_job(
#     name="read_job_py_job",
#     selection=read_job_selection,
# )


ingest_synced_jobs_yaml = define_asset_job(
    name="read_job_yaml_job",
    selection=read_job_selection_yaml,
)
