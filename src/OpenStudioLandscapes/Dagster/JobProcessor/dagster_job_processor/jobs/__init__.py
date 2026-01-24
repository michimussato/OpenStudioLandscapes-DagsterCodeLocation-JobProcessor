from dagster import AssetSelection, define_asset_job


# Asset Selections
submit_jobs_job = AssetSelection.assets("submit_job")
# ingest_jobs_job = AssetSelection.assets("ingest_job")
read_job_py_job = AssetSelection.assets("read_job_py")


submit_synced_jobs = define_asset_job(
    name="submit_jobs_job",
    selection=submit_jobs_job,
)


ingest_synced_jobs = define_asset_job(
    name="read_job_py_job",
    selection=read_job_py_job,
)
