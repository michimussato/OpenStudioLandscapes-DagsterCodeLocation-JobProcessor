import json
import shlex
import subprocess

from dagster import asset, Config, MaterializeResult, MetadataValue, AssetExecutionContext

from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor import settings


class SubmitJobConfig(Config):
    filename: str
    combine_dict_path: str


@asset(
    group_name="DEADLINE_SUBMIT_JOB",
    deps=["export_combined_dict"]
)
def submit_job(
        context: AssetExecutionContext,
        config: SubmitJobConfig,
) -> MaterializeResult:

    with open(config.combine_dict_path, "r") as combine_dict_file:
        combine_dicts = json.load(combine_dict_file)

    try:

        proc = subprocess.Popen(
            args=combine_dicts["deadline_cmd"]["deadline_cmd"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        # /nfs/AWSPortalRoot1/out/Test Production/Shot/SQ020_SH030/Layout/sh030_001/051/4_1197-1254_4/submit_job.sh
        # /opt/Thinkbox/Deadline10/bin/deadlinecommand -SubmitMultipleJobsV2 -jsonfilepath "/nfs/AWSPortalRoot1/out/Test Production/Shot/SQ020_SH030/Layout/sh030_001/051/4_1197-1254_4/submission.json"
        # "/opt/Thinkbox/Deadline10/bin/deadlinecommand.exe" -RunCommandForRepository "Repository" "/opt/Thinkbox/DeadlineRepository10;/opt/Thinkbox/DeadlineDatabase10/certs/Deadline10Client.pfx" -DoRepositoryRepair True False True
        # "/opt/Thinkbox/Deadline10/bin/deadlinecommand.exe" -RunCommandForRepository "Repository" "/opt/Thinkbox/DeadlineRepository10;/opt/Thinkbox/DeadlineDatabase10/certs/Deadline10Client.pfx" -SubmitMultipleJobsV2 -jsonfilepath "/nfs/AWSPortalRoot1/out/Test Production/Shot/SQ020_SH030/Layout/sh030_001/051/4_1197-1254_4/submission.json"

        result = proc.communicate()[0].decode("utf-8")

        with open(config.combine_dict_path, "w") as combine_dict_file:

            combine_dicts["deadline_job_submitted"] = True
            combine_dicts["deadline_job_submitted_result"] = result

            # combine_dict_file.seek(0)  # rewind
            json.dump(
                obj=combine_dicts,
                fp=combine_dict_file,
                ensure_ascii=False,
                indent=settings.JSON_INDENT,
                sort_keys=True,
            )
            # combine_dict_file.truncate()

    except Exception as err:
        context.log.error(err)
        combine_dicts["deadline_job_submitted"] = False
        combine_dicts["deadline_job_submitted_result"] = err

    return MaterializeResult(
        asset_key="submit_job",
        metadata={
            "url": MetadataValue.url(combine_dicts["task_url"]),
            "job_submitted": MetadataValue.bool(combine_dicts["deadline_job_submitted"]),
            "cmd": MetadataValue.json(combine_dicts["deadline_cmd"]["deadline_cmd"]),
            "cmd_joined": MetadataValue.path(shlex.join(combine_dicts["deadline_cmd"]["deadline_cmd"])),
            # 'destination': MetadataValue.path(config.render_output_directory),
            "result": MetadataValue.text(combine_dicts["deadline_job_submitted_result"])
        }
    )