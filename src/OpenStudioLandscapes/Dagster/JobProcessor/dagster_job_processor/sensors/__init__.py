import datetime

from dagster import (
    RunRequest,
    AssetKey,
    SensorResult,
    sensor,
    SensorEvaluationContext,
    AssetSelection,
    AutomationConditionSensorDefinition, DefaultSensorStatus,
)

import os
import json
import pathlib
import shutil

from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor import settings
from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.config.models import DefaultConstants
from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.assets.read_yaml import ASSET_HEADER_JOB_PROCESSOR
from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.assets.submit_jobs import ASSET_HEADER_JOB_SUBMITTER

from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.jobs import submit_synced_jobs, ingest_synced_jobs_yaml


CONFIG: DefaultConstants = DefaultConstants()


@sensor(
    job=submit_synced_jobs,
    default_status=settings.SENSORS_STATUS,
    minimum_interval_seconds=30,
)
def submission_sensor(
        context: SensorEvaluationContext,
):
    path_to_submission_files = pathlib.Path(CONFIG.OUTPUT_ROOT)

    previous_state = json.loads(context.cursor) if context.cursor else {}
    current_state = {}

    runs_to_request = []

    for submission_json in path_to_submission_files.rglob(CONFIG.SUBMISSION_JSON):

        file_path = path_to_submission_files / submission_json

        context.log.info(f'Checking {file_path}...')

        combine_dict_path = pathlib.Path(path_to_submission_files / submission_json).parent / 'combined_dict.json'

        # this is for older versions.
        # once every folder has this file,
        # this part can be removed
        if not combine_dict_path.exists():
            current_state[str(file_path)] = str(combine_dict_path)
            continue
        else:
            with open(combine_dict_path, 'r+') as f:
                combined_dict = json.load(f)

                if 'deadline_job_queued' not in combined_dict:
                    # current_state[str(file_path)] = str(combine_dict_path)
                    continue
                elif 'deadline_job_queued' in combined_dict:
                    if combined_dict['deadline_job_queued'] is True:
                        # current_state[str(file_path)] = str(combine_dict_path)
                        continue
                    else:

                        current_state[str(file_path)] = str(combine_dict_path)

                        # if the file is new or has been modified since the last run, add it to the request queue
                        # if file_path not in previous_state or previous_state[file_path] != last_modified:
                        if file_path not in previous_state:

                            context.log.info(f'Submission file is new: {file_path}...')

                            runs_to_request.append(RunRequest(
                                run_key=f"submit_synced_jobs_{str(file_path).replace(os.sep, '__')}",
                                run_config={
                                    "ops": {
                                        AssetKey([*ASSET_HEADER_JOB_SUBMITTER["key_prefix"], "submit_job"]).to_python_identifier(): {
                                            "config": {
                                                "filename": str(file_path),
                                                "combine_dict_path": str(combine_dict_path),
                                                # **request_config
                                                }
                                            }
                                        }
                                    }
                                )
                            )

                            # This is just the Dagster Job, not the actual
                            # submission to deadline.
                            combined_dict['deadline_job_queued'] = True

                            f.seek(0)  # rewind
                            json.dump(combined_dict, f, ensure_ascii=False, indent=4)
                            f.truncate()

    return SensorResult(
        run_requests=runs_to_request,
        cursor=json.dumps(current_state),
    )


# @sensor(
#     job=ingest_synced_jobs,
#     default_status=settings.SENSORS_STATUS,
#     minimum_interval_seconds=15,
# )
# def ingestion_sensor(
#         context: SensorEvaluationContext,
# ):
#     path_to_submission_files = pathlib.Path(CONFIG.INPUT_ROOT)
#
#     runs_to_request = []
#
#     moves = []
#
#     for job_py in path_to_submission_files.glob('*.py'):
#
#         context.log.info(f'Checking {job_py}...')
#
#         context.log.info(f'Submission file is new: {job_py}...')
#
#         CONFIG.INPUT_ROOT_PROCESSED.mkdir(mode=0o777, exist_ok=True, parents=True)
#         output_file = CONFIG.INPUT_ROOT_PROCESSED / f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")}_{job_py.name}'
#         # shutil.move(job_py, output_file)
#
#         context.log.info(f'{output_file = }...')
#         # context.log.info(f'{constants.INPUT_ROOT_PROCESSED = }...')
#         context.log.info(f'{job_py = }...')
#
#         runs_to_request.append(RunRequest(
#             # whether or not a run will skip is based on the run_key that was assigned to previous ones
#             run_key=f"ingested_jobs__{datetime.datetime.timestamp(datetime.datetime.now())}__{str(job_py).replace(os.sep, '__')}",
#             run_config={
#                 "ops": {
#                     AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "read_job_py"]).to_python_identifier(): {
#                         "config": {
#                             "filename": str(output_file),
#                             }
#                         }
#                     }
#                 }
#             )
#         )
#
#         moves.append({'src': job_py, 'dst': output_file})
#
#     for i in moves:
#         shutil.move(i['src'], i['dst'])
#
#     return SensorResult(
#         run_requests=runs_to_request,
#     )


@sensor(
    job=ingest_synced_jobs_yaml,
    default_status=settings.SENSORS_STATUS,
    minimum_interval_seconds=15,
)
def ingestion_sensor_yaml(
        context: SensorEvaluationContext,
):
    path_to_submission_files = pathlib.Path(CONFIG.INPUT_ROOT)

    runs_to_request = []

    moves = []

    ext_yaml = [
        ".yml",
        ".yaml",
    ]

    for job_yaml in path_to_submission_files.glob('*.*'):

        if job_yaml.suffix in ext_yaml:

            context.log.info(f'Checking {job_yaml}...')

            context.log.info(f'Submission file is new: {job_yaml}...')

            CONFIG.INPUT_ROOT_PROCESSED.mkdir(mode=0o777, exist_ok=True, parents=True)
            output_file = CONFIG.INPUT_ROOT_PROCESSED / f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")}_{job_yaml.name}'
            # shutil.move(job_py, output_file)

            context.log.info(f'{output_file = }...')
            # context.log.info(f'{constants.INPUT_ROOT_PROCESSED = }...')
            context.log.info(f'{job_yaml = }...')

            runs_to_request.append(RunRequest(
                # whether or not a run will skip is based on the run_key that was assigned to previous ones
                run_key=f"ingested_jobs__{datetime.datetime.timestamp(datetime.datetime.now())}__{str(job_yaml).replace(os.sep, '__')}",
                run_config={
                    "ops": {
                        AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "read_job_yaml"]).to_python_identifier(): {
                            "config": {
                                "filename": str(output_file),
                                }
                            }
                        }
                    }
                )
            )

            moves.append({'src': job_yaml, 'dst': output_file})

    for i in moves:
        shutil.move(i['src'], i['dst'])

    return SensorResult(
        run_requests=runs_to_request,
    )


# Custom AutoMaterialize Sensor
# https://docs.dagster.io/concepts/assets/asset-auto-execution#auto-materialize-sensors
my_custom_auto_materialize_sensor = AutomationConditionSensorDefinition(
    "my_custom_auto_materialize_sensor",
    target=AssetSelection.all(include_sources=True),
    minimum_interval_seconds=15,
    default_status=DefaultSensorStatus.RUNNING,
)
