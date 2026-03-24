from dagster import AssetSelection, define_asset_job, AssetKey

from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.assets.read_yaml import ASSET_HEADER_JOB_PROCESSOR
from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.assets.submit_jobs import ASSET_HEADER_JOB_SUBMITTER


# Asset Selections
submit_jobs_job = AssetSelection.assets(
    AssetKey([*ASSET_HEADER_JOB_SUBMITTER["key_prefix"], "submit_job"]),
)
# ingest_jobs_job = AssetSelection.assets("ingest_job")
read_job_py_job = AssetSelection.assets(
    AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "read_job_py"]),
)


submit_synced_jobs = define_asset_job(
    name="submit_jobs_job",
    selection=submit_jobs_job,
)


ingest_synced_jobs = define_asset_job(
    name="read_job_py_job",
    selection=read_job_py_job,
)
