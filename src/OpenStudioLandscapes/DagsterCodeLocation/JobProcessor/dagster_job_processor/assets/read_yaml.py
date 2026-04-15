import enum
import pathlib
import re
import shutil
import textwrap
from typing import Any, Generator, Dict, List

import yaml
from dagster import (
    asset, AssetIn, MetadataValue,
    AssetMaterialization, Output,
    Config, AssetExecutionContext, AssetKey,
)
import json

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.config.models import DefaultConstants
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.resources import KitsuResource
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.jobs.job_base import JobBase, Resolution
# from OpenStudioLandscapes.DagsterCodeLocation.StreamingProcess import submit_cmds

# TODO
#  rename to generate_job_submission_scripts


group_name = "DEADLINE_GENERATE_JOB_SCRIPTS"


test_jobs = ["blender", "houdini", "nuke"][0]


GROUP_JOB_PROCESSOR_READER = "OpenStudioLandscapes_DagsterCodeLocation_JobProcessor_Reader"
# KEY_CONSTANTS_DEFAULT = [GROUP_CONSTANTS_DEFAULT, "Constants"]
KEY_JOB_PROCESSOR_READER = [GROUP_JOB_PROCESSOR_READER]

ASSET_HEADER_JOB_PROCESSOR_READER = {
    "group_name": GROUP_JOB_PROCESSOR_READER,
    "key_prefix": KEY_JOB_PROCESSOR_READER,
}


# Todo
#  - [ ] Rename to _PREPROCESSOR
GROUP_JOB_PROCESSOR = "OpenStudioLandscapes_DagsterCodeLocation_JobProcessor_PreProcessor"
# KEY_CONSTANTS_DEFAULT = [GROUP_CONSTANTS_DEFAULT, "Constants"]
KEY_JOB_PROCESSOR = [GROUP_JOB_PROCESSOR]

ASSET_HEADER_JOB_PROCESSOR = {
    "group_name": GROUP_JOB_PROCESSOR,
    "key_prefix": KEY_JOB_PROCESSOR,
}


GROUP_JOB_PROCESSOR_PREPROCESSOR_KITSU = "OpenStudioLandscapes_DagsterCodeLocation_JobProcessor_Kitsu"
# KEY_CONSTANTS_DEFAULT = [GROUP_CONSTANTS_DEFAULT, "Constants"]
KEY_JOB_PROCESSOR_PREPROCESSOR_KITSU = [GROUP_JOB_PROCESSOR_PREPROCESSOR_KITSU]

ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU = {
    "group_name": GROUP_JOB_PROCESSOR_PREPROCESSOR_KITSU,
    "key_prefix": KEY_JOB_PROCESSOR_PREPROCESSOR_KITSU,
}


GROUP_JOB_PROCESSOR_DEADLINE = "OpenStudioLandscapes_DagsterCodeLocation_JobProcessor_Deadline"
# KEY_CONSTANTS_DEFAULT = [GROUP_CONSTANTS_DEFAULT, "Constants"]
KEY_JOB_PROCESSOR_DEADLINE = [GROUP_JOB_PROCESSOR_DEADLINE]

ASSET_HEADER_JOB_PROCESSOR_DEADLINE = {
    "group_name": GROUP_JOB_PROCESSOR_DEADLINE,
    "key_prefix": KEY_JOB_PROCESSOR_DEADLINE,
}


class KitsuEntityTypes(enum.StrEnum):
    SHOT = "Shot"


def get_task_name(
        kitsu_dict: Dict,
) -> str:
    """
    {
      "task_type": {
        "allow_timelog": true,
        "archived": false,
        "color": "#F06292",
        "created_at": "2026-01-13T02:07:58",
        "department_id": "9cf1aa43-06f5-4e9a-a51a-2b1fd3ed3c2f",
        "description": null,
        "for_entity": "Shot",
        "id": "859d37ac-24e1-4fba-91a9-5c0479a11766",
        "name": "Rendering",
        "priority": 6,
        "short_name": "",
        "shotgun_id": null,
        "type": "TaskType",
        "updated_at": "2026-01-13T02:07:58"
      },
    }
    """
    _task_name = (
        kitsu_dict
        .get("task_type", {})
        .get("name", "No Task Name")
    )
    return _task_name


def get_entity_type(
        kitsu_dict: Dict,
) -> str:
    """
    {
      "entity_type": {
        "archived": false,
        "created_at": "2026-01-13T02:07:57",
        "description": null,
        "id": "6b85fb0f-a152-412e-b828-0a2c030b1393",
        "name": "Shot",
        "short_name": null,
        "type": "EntityType",
        "updated_at": "2026-01-13T02:07:57"
      },
    }
    """
    _entity_type = (
        kitsu_dict
        .get("entity_type", {})
        .get("name", "No Entity Type")
    )
    return _entity_type


def get_entity_name(
        kitsu_dict: Dict,
) -> str:
    """
    {
      "entity": {
        "canceled": false,
        "code": null,
        "created_at": "2026-03-14T22:38:44",
        "created_by": "108d7c11-b47b-4c4b-9fa2-f955e095d1b8",
        "data": {
          "fps": 25,
          "frame_in": 1201,
          "frame_out": 1250,
          "max_retakes": null,
          "resolution": "960x540"
        },
        "description": null,
        "entity_type_id": "6b85fb0f-a152-412e-b828-0a2c030b1393",
        "id": "89bcad46-1be7-4095-a5db-edeac55c04ab",
        "is_casting_standby": false,
        "is_shared": false,
        "name": "SH030",
        "nb_entities_out": 0,
        "nb_frames": 50,
        "parent_id": "dc80cc66-b934-4fe8-8bb3-cc90bf0a2348",
        "preview_file_id": "a8bad4a4-3d67-4350-8755-bf7976c80831",
        "project_id": "3ede4117-b73c-4bd3-83a2-40d66bc954c5",
        "ready_for": null,
        "shotgun_id": null,
        "source_id": null,
        "status": "running",
        "type": "Entity",
        "updated_at": "2026-03-23T09:43:42"
      },
    }
    """
    _entity_info = (
        kitsu_dict
        .get("entity", {})
        .get("name", "No Entity Name")
    )
    return _entity_info


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={},
)
def CONFIG(
    context: AssetExecutionContext,
) -> Generator[
    Output[DefaultConstants] | AssetMaterialization,
    None,
    None,
]:

    config: DefaultConstants = DefaultConstants()

    context.log.debug(f"{config = }")

    yield Output(config)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.md(
                f"```yaml\n{yaml.safe_dump(json.loads(config.model_dump_json(fallback=str, indent=2)))}\n```"
            ),
        },
    )


class IngestJobConfig(Config):
    filename: str


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_READER,
    description="Parses the job file.",
)
def read_job_yaml(
        context: AssetExecutionContext,
        config: IngestJobConfig,
) -> Generator[Output[JobBase] | AssetMaterialization | Any, Any, None]:

    with open(config.filename) as fr:
        job_dict = yaml.safe_load(fr)

    context.log.debug(f"{job_dict = }")
    context.log.debug(f"{config.filename = }")

    job_model: JobBase = JobBase(
        **job_dict,
        job_file_yaml=pathlib.Path(config.filename),
    )

    context.log.debug(f"{job_model = }")

    yield Output(job_model)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.md(
                f"```yaml\n{yaml.safe_dump(json.loads(job_model.model_dump_json(fallback=str, indent=2)))}\n```"
            ),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU,
    ins={
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    },
)
def get_kitsu_task_dict(
        context: AssetExecutionContext,
        kitsu_resource: KitsuResource,
        job_model: JobBase,
) -> Generator[Output[Any] | AssetMaterialization | Any, Any, None]:
    """Returns a Kitsu task dict as a MaterializeResult object in the JSON format."""

    # TODO: make fail safe

    task_id = job_model.kitsu_task
    task_dict = kitsu_resource.get_kitsu_task_dict(task_id=str(task_id))

    yield Output(task_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(task_dict),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        )
    },
)
def get_task_url(
        context: AssetExecutionContext,
        kitsu_resource: KitsuResource,
        get_kitsu_task_dict: Dict,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    """Returns a Kitsu task dict as a MaterializeResult object in the JSON format."""

    # TODO: make fail safe

    if "error" in get_kitsu_task_dict:
        raise Exception(f"Kitsu task ID is set but can't get Task URL from Kitsu for this shot:\n"
                        f"{get_kitsu_task_dict['error']}")

    task_dict = get_kitsu_task_dict
    task_url = kitsu_resource.get_task_url(task_dict=task_dict)

    yield Output(task_url)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.url(task_url),
        }
    )


# @asset(
#     **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
#     ins={
#         "version": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "version"]),
#         ),
#         "CONFIG": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
#         ),
#         "resolution": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "resolution"]),
#         ),
#         "job_model": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
#         ),
#         "get_kitsu_task_dict": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
#         ),
#     },
# )
# def annotations_string(
#         context: AssetExecutionContext,
#         version: str,
#         CONFIG: DefaultConstants,
#         resolution: Resolution,
#         job_model: JobBase,
#         get_kitsu_task_dict: Dict,
# ) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
#     """Returns the annotations string for the Deadline Draft jobs as a MaterializeResult object in the JSON format."""
#
#     handles = job_model.handles
#
#     # fps = job_model.fps
#     #
#     # fi = job_model.cut_in
#     # fo = job_model.cut_out
#
#     fi_kitsu = 0
#     fo_kitsu = 0
#     if bool(job_model.kitsu_task):
#         if get_task_name(get_kitsu_task_dict) == "Shot":
#             fi_kitsu = get_kitsu_task_dict.get("entity", {}).get("data", {}).get("frame_in", 0)
#             fo_kitsu = get_kitsu_task_dict.get("entity", {}).get("data", {}).get("frame_out", 0)
#
#     # fi_fo = (fi, fo)
#
#     entity_name = get_entity_name(get_kitsu_task_dict)
#     task_name = get_task_name(get_kitsu_task_dict)
#
#     rgb = 95
#     draft_annotations_string = {
#         "NorthWest": {
#             "text": f"{entity_name}/{task_name}",  # Todo: Add Sequence name to Shot if Shot and Shot is part of Sequence
#             "colorR": rgb,
#             "colorG": rgb,
#             "colorB": rgb,
#             "type": ""
#         },
#         "NorthCenter": {
#             "text": f"{job_model.job_file.name}",
#             "colorR": rgb,
#             "colorG": rgb,
#             "colorB": rgb,
#             "type": ""
#         }, "NorthEast": {
#             "text": f"$time ({version})",
#             "colorR": rgb,
#             "colorG": rgb,
#             "colorB": rgb,
#             "type": ""
#         }, "SouthWest": {
#             "text": f"",
#             "colorR": rgb,
#             "colorG": rgb,
#             "colorB": rgb,
#             "type": ""
#         },
#         "SouthCenter": {
#             "text": f"{handles}_{str(job_model.cut_in).zfill(CONFIG.PADDING)}||{handles}_{str(job_model.cut_in).zfill(CONFIG.PADDING)}|$frame|{str(job_model.cut_out).zfill(CONFIG.PADDING)}_{handles}||{str(job_model.cut_out).zfill(CONFIG.PADDING)}_{handles} @{job_model.fps}",
#             "colorR": rgb,
#             "colorG": rgb,
#             "colorB": rgb,
#             "type": ""
#         },
#         "SouthEast": {
#             "text": f"{resolution.x}x{resolution.y} (x{CONFIG.RESOLUTION_DRAFT_SCALE})",
#             "colorR": rgb,
#             "colorG": rgb,
#             "colorB": rgb,
#             "type": ""
#         }
#     }
#
#     yield Output(json.dumps(draft_annotations_string))
#
#     yield AssetMaterialization(
#         asset_key=context.asset_key,
#         metadata={
#             "__".join(context.asset_key.path): MetadataValue.json(draft_annotations_string),
#             "annotations_string": MetadataValue.text(json.dumps(draft_annotations_string)),
#             "cut_in_kitsu": MetadataValue.int(fi_kitsu),
#             "cut_out_kitsu": MetadataValue.int(fo_kitsu),
#         }
#     )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
        "show_name": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "show_name"]),
        ),
        "task_name": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "task_name"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        # "job_model": AssetIn(
        #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "read_job_yaml"])
        # ),
    },
)
def render_version_directory(
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
        show_name: str,
        task_name: str,
        CONFIG: DefaultConstants,
        # job_model: JobBase,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    # TODO: make this fail safe
    entity_name = get_entity_name(get_kitsu_task_dict)

    entity_type = get_entity_type(get_kitsu_task_dict)

    _out = pathlib.Path(f'{CONFIG.OUTPUT_ROOT}/{show_name}/{entity_type}/{entity_name}/{task_name}/')
    _out.mkdir(parents=True, exist_ok=True)

    yield Output(_out)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(_out),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "render_version_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_version_directory"]),
        ),
    },
)
def version(
        context: AssetExecutionContext,
        CONFIG: DefaultConstants,
        render_version_directory: pathlib.Path,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    # This directory must exist in order for it to be iterable

    pattern = re.compile(f"^[0-9]{{{CONFIG.PADDING_VERSION}}}")

    dirs = [i.name for i in render_version_directory.iterdir() if i.is_dir() and pattern.match(i.name)]
    dirs.append(str(0).zfill(CONFIG.PADDING_VERSION))
    dirs.sort()
    version_ = max(dirs)
    new_version = str(int(version_) + 1).zfill(CONFIG.PADDING_VERSION)
    new_version_dir = pathlib.Path(f"{render_version_directory}/{new_version}")
    new_version_dir.mkdir(parents=True, exist_ok=True)

    yield Output(new_version)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(new_version),
            "dirs": MetadataValue.json(dirs),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "job_title": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title"])
        ),
        "output_format": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "output_format"])
        ),
        "frame_start_absolute": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_start_absolute"])
        ),
        "frame_end_absolute": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_end_absolute"])
        ),
    },
)
def render_output_filename(
        context: AssetExecutionContext,
        CONFIG: DefaultConstants,
        job_model: JobBase,
        job_title: str,
        output_format: str,
        frame_start_absolute: int,
        frame_end_absolute: int,
) -> Generator[Output[Dict[str, str]] | AssetMaterialization | Any, Any, None]:

    # padding_bash_expansion = "{%i..%i}" % (frame_start_absolute, frame_end_absolute)
    padding_deadline = f"{job_model.plugin_model.padding_deadline}"
    padding_command = f"{job_model.plugin_model.padding_command}"
    padding_oiiotool = f"{job_model.plugin_model.padding_oiiotool}"

    # # Don't uncomment
    # # Required to eval(padding_deadline) and eval(padding_command)
    # from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.settings import PADDING as EVAL_PADDING
    EVAL_PADDING = CONFIG.PADDING

    ret = {
        # "padding_bash_expansion": f"{job_title}.{padding_bash_expansion}.{output_format}",
        "padding_deadline": f"{job_title}.{eval(padding_deadline)}.{output_format}",
        "padding_command": f"{job_title}.{eval(padding_command)}.{output_format}",
        "padding_oiiotool": f"{job_title}.{eval(padding_oiiotool)}.{output_format}",
    }

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "version": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "version"]),
        ),
        # "CONFIG": AssetIn(
        #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        # ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "render_version_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_version_directory"])
        ),
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
    }
)
def render_output_directory(
        context: AssetExecutionContext,
        version: str,
        # CONFIG: DefaultConstants,
        job_model: JobBase,
        render_version_directory: pathlib.Path,
        get_kitsu_task_dict: Dict,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    # handles = job_model.handles

    _out = render_version_directory / version
    _out.mkdir(parents=True, exist_ok=True)

    if bool(job_model.kitsu_task):
        entity_type = get_entity_type(get_kitsu_task_dict)
        if entity_type == 'Shot':
            # filename = f'{str(handles)}_{str(job_model.cut_in - job_model.handles).zfill(CONFIG.PADDING)}-{str(job_model.cut_out + job_model.handles).zfill(CONFIG.PADDING)}_{str(handles)}'
            # with open(_out / filename, "w") as fw:
            #     fw.write(f"{str(job_model.kitsu_task) = }")
            # with open(_out / "kitsu_task_id.txt", "w") as fw:
            #     fw.write(str(job_model.kitsu_task))
            with open(_out / "kitsu_task.json", "w") as fw:
                json.dump(
                    get_kitsu_task_dict,
                    fw,
                    indent=2,
                    default=str,
                    ensure_ascii=True,
                    sort_keys=True,
                )

    _out.mkdir(parents=True, exist_ok=True)

    yield Output(_out)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(_out)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def job_title(
        context: AssetExecutionContext,
        job_model: JobBase,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:

    base, first_dot, rest = job_model.job_file.name.partition(".")

    yield Output(base)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(base),
            "job_file".join(context.asset_key.path): MetadataValue.path(job_model.job_file),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
    }
)
def show_name(
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
) -> Generator[Output[str | Any] | AssetMaterialization | Any, Any, None]:

    ret = (
        get_kitsu_task_dict
        .get("project", {})
        .get("name", "No Show")
    )

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
    }
)
def task_name(
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
) -> Generator[Output[str | Any] | AssetMaterialization | Any, Any, None]:

    ret = get_task_name(get_kitsu_task_dict)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "version": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "version"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "show_name": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "show_name"])
        ),
        "task_name": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "task_name"]),
        ),
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
    }
)
def job_title_str(
        context: AssetExecutionContext,
        version: str,
        CONFIG: DefaultConstants,
        job_model: JobBase,
        show_name: str,
        task_name: str,
        get_kitsu_task_dict: Dict,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:

    entity_name = get_entity_name(get_kitsu_task_dict)
    entity_type = get_entity_type(get_kitsu_task_dict)

    if bool(job_model.kitsu_task):
        if entity_type == KitsuEntityTypes.SHOT.value:
            entity_name = f'{entity_name} - {str(job_model.handles)}_{str(job_model.cut_in).zfill(CONFIG.PADDING)}-{str(job_model.cut_out).zfill(CONFIG.PADDING)}_{job_model.handles}'
            # entity_name = f'{self.sequence_name}_{self.entity_name} - {str(self.handles)}_{str(self.frame_start).zfill(self.PADDING)}-{str(self.frame_end).zfill(self.PADDING)}_{self.handles}'

    ret = f'{show_name} - {entity_name} - {task_name} - {job_model.job_file.name} - {version} - {pathlib.Path(job_model.plugin_model.executable).name}'

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "job_title_str": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title_str"]),
        ),
    }
)
def batch_name(
        context: AssetExecutionContext,
        job_title_str: str
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:

    ret = f"Batch: {job_title_str}"

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


# @asset(
#     **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
#     ins={
#         "render_output_directory": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
#         ),
#         "render_output_filename": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_filename"])
#         ),
#         "batch_name": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "batch_name"])
#         ),
#         "job_model": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
#         ),
#     }
# )
# def props(
#         context: AssetExecutionContext,
#         render_output_directory: pathlib.Path,
#         render_output_filename: Dict,
#         batch_name: str,
#         job_model: JobBase,
# ) -> Generator[Output[List[str]] | AssetMaterialization | Any, Any, None]:
#
#     props = [
#         # ('Comment', f'{job_model.comment}'),  # TODO
#         # ('ForceReloadPlugin', True),
#         # ('InitialStatus', job_model.deadline_initial_status),
#         # ('OutputDirectory0', f'{render_output_directory}'),
#         # ('OutputFilename0', f'{render_output_filename["padding_deadline"]}'),
#         # ('BatchName', f'{batch_name}'),
#         # This should not end up in plugin_info_file it seems: https://docs.thinkboxsoftware.com/products/deadline/10.1/1_User%20Manual/manual/manual-submission.html#job-info-ref-label
#     ]
#
#     props_ = [f'{k}={v}' for k, v in props]
#
#     yield Output(props_)
#
#     yield AssetMaterialization(
#         asset_key=context.asset_key,
#         metadata={
#             "__".join(context.asset_key.path): MetadataValue.json(props_)
#         }
#     )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def fps(
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
        job_model: JobBase,
) -> Generator[Output[float] | AssetMaterialization | Any, Any, None]:

    """
    frame_in = get_kitsu_task_dict["entity"]["data"]["frame_in"]
    frame_out = get_kitsu_task_dict["entity"]["data"]["frame_out"]
    nb_frames = get_kitsu_task_dict["entity"]["nb_frames"]
    """

    if bool(job_model.kitsu_task):
        if "error" in get_kitsu_task_dict:
            raise Exception(f"Kitsu task ID is set but can't get FPS from Kitsu for this shot:\n"
                            f"{get_kitsu_task_dict['error']}")

    # if bool(read_job_py["kitsu_task"]):
    fps_job = job_model.fps

    fps_kitsu_project = float(get_kitsu_task_dict.get("project", {}).get("fps", 0))

    kitsu_entity_type = get_entity_type(get_kitsu_task_dict)
    fps_kitsu_shot = float(0)
    if kitsu_entity_type == "Shot":
        fps_kitsu_entity = fps_kitsu_shot = float(get_kitsu_task_dict.get("entity", {}).get("data", {}).get("fps", 0))

    yield Output(fps_job)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.float(fps_job),
            "fps_job": MetadataValue.float(fps_job),
            "fps_kitsu_project": MetadataValue.float(fps_kitsu_project),
            "kitsu_entity_type": MetadataValue.text(kitsu_entity_type),
            "fps_kitsu_shot": MetadataValue.float(fps_kitsu_shot),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    },
    description="Returns the output format of the render."
)
def output_format(
        context: AssetExecutionContext,
        job_model: JobBase,
) -> Generator[Output[Any] | AssetMaterialization | Any, Any, None]:

    # if read_job_py["output_format"] is None:
    #     raise ValueError("output_format is not defined.")

    # if job_model.output_format not in read_job_py["plugin_dict"]["submitter"]["output_formats_plugin"]:
    #     raise ValueError(f"output_format is not supported: {read_job_py['output_format']}")

    yield Output(job_model.output_format)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(job_model.output_format)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
    }
)
def frame_start_absolute(
        # Todo:
        #  - [ ] rename to `work_in`
        #  - [ ] use `shot_range` instead?
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
        job_model: JobBase,
        CONFIG: DefaultConstants,
) -> Generator[Output[int | Any] | AssetMaterialization | Any, Any, None]:

    """
    frame_in = get_kitsu_task_dict["entity"]["data"]["frame_in"]
    frame_out = get_kitsu_task_dict["entity"]["data"]["frame_out"]
    nb_frames = get_kitsu_task_dict["entity"]["nb_frames"]
    """

    fs = job_model.cut_in

    fs_kitsu = get_kitsu_task_dict.get("entity", {}).get("data", {}).get("frame_in", 0)

    fsa = fs - job_model.handles

    if CONFIG.DONT_ALLOW_NEGATIVE_FRAMES:
        raise Exception("Negative frames not allowed")

    yield Output(fsa)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.int(fsa),
            "work_in": MetadataValue.int(fsa),
            "cut_in": MetadataValue.int(fs),
            "cut_in_kitsu": MetadataValue.int(fs_kitsu),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
    }
)
def frame_end_absolute(
        # Todo:
        #  - [ ] rename to `work_out`
        #  - [ ] use `shot_range` instead?
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
        job_model: JobBase,
        CONFIG: DefaultConstants,
) -> Generator[Output[int | Any] | AssetMaterialization | Any, Any, None]:

    fe = job_model.cut_out

    fe_kitsu = get_kitsu_task_dict.get("entity", {}).get("data", {}).get("frame_out", 0)

    fea = fe + job_model.handles

    if CONFIG.DONT_ALLOW_NEGATIVE_FRAMES:
        raise Exception("Negative frames not allowed")

    yield Output(fea)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.int(fea),
            "work_out": MetadataValue.int(fea),
            "cut_out": MetadataValue.int(fe),
            "cut_out_kitsu": MetadataValue.int(fe_kitsu),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "frame_start_absolute": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_start_absolute"])
        ),
        "frame_end_absolute": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_end_absolute"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def frames(
        # Todo
        #  - [ ] use `cut_range` and `shot_range`/`work_range` instead?
        context: AssetExecutionContext,
        CONFIG: DefaultConstants,
        frame_start_absolute: int,
        frame_end_absolute: int,
        job_model: JobBase,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:

    # make sure we filter frame jumps according to the chunk_size
    # for nuke, render time could be way slower if it has
    # to be launched for every single frame
    # frame_jumps = [i for i in constants.FRAME_JUMPS if i <= combine_dicts["yaml_submission"]["chunk_size"]]

    if job_model.chunk_size > 1:
        frame_jumps = [min(CONFIG.FRAME_JUMPS)]
    else:
        frame_jumps = CONFIG.FRAME_JUMPS

    frame_list = ",".join([
        f"{frame_start_absolute}-{frame_end_absolute}x{int(i)}"
        for i in frame_jumps
    ])

    yield Output(frame_list)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(frame_list)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
    ins={
        "batch_name": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "batch_name"])
        ),
        "job_title_str": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title_str"])
        ),
        "render_output_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
        ),
        "frames": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frames"])
        ),
        # "props": AssetIn(
        #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "props"])
        # ),
        "render_output_filename": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_filename"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def job_info_file(
        context: AssetExecutionContext,
        batch_name: str,
        job_title_str: str,
        render_output_directory: pathlib.Path,
        frames: str,
        # props: List,
        render_output_filename: Dict,
        job_model: JobBase,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    # https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#job-info-file-options
    # render_output_directory.mkdir(parents=True, exist_ok=True)
    path = render_output_directory / "jobinfo_info.txt"

    context.log.debug(f"{path = }")

    from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.jobs import models_submission

    job_info_dict = {
        "Plugin": models_submission.DeadlinePlugins.CommandLine.value,
        "Frames": frames,
        "Name": job_title_str,
        "Comment": job_model.comment,
        # "Department"
        "BatchName": batch_name,
        # "UserName"
        # "Pool"
        # "SecondaryPool"
        # "Group"
        "Priority": 50,
        "ChunkSize": job_model.chunk_size,
        # "ConcurrentTasks"
        # "LimitConcurrentTasksToNumberOfCpus"
        # "OnJobComplete"
        # "SynchronizeAllAuxiliaryFiles"
        "ForceReloadPlugin": True,
        # "Sequential"
        # "SuppressEvents"
        # "Protected"
        "InitialStatus": job_model.deadline_initial_status,
        # "StartupDirectory"
        "OutputDirectory0": render_output_directory.as_posix(),
        "OutputFilename0": render_output_filename["padding_deadline"],
    }

    job_info = models_submission.JobInfo(
        **job_info_dict,
    )

    context.log.debug(f"{job_info = }")

    job_info_file_str = str
    for k, v in job_info_dict.items():
        job_info_file_str += f"{k}={v}\n"

    context.log.debug(f"{job_info_file_str = }")

    # job_info_file_str = textwrap.dedent(
    #     f"""\
    #     InitialStatus={job_model.deadline_initial_status}
    #     BatchName={batch_name}
    #     Name={job_title_str}
    #     Frames={frames}
    #     ChunkSize={job_model.chunk_size}
    #     ForceReloadPlugin=True
    #     Comment={job_model.comment}
    #     Plugin=CommandLine
    #     StartupDirectory=
    #     OutputDirectory0={render_output_directory}
    #     OutputFilename0={render_output_filename["padding_deadline"]}
    #     """
    # )

    with open(path, "w") as fw:
        fw.write(job_info_file_str)

    yield Output(path)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(path),
            # "job_info_file_str": MetadataValue.text(job_info_file_str),
            "job_info_file_str": MetadataValue.md(f"```\n{job_info_file_str}\n```"),
            "job_info_file_yaml": MetadataValue.md(
                f"```yaml\n{yaml.safe_dump(json.loads(job_info.model_dump_json(indent=2, fallback=str)))}\n```"
            ),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
    ins={
        "render_output_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
        ),
        "render_arguments": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_arguments"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def plugin_info_file(
        context: AssetExecutionContext,
        render_output_directory: pathlib.Path,
        render_arguments: str,
        job_model: JobBase,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    # https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#plug-in-info-file
    # render_output_directory.mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(f"{render_output_directory}/plugin_info.txt")

    job_info_file_str = textwrap.dedent(
        f"""
        Executable={job_model.plugin_model.executable.as_posix()}
        Arguments="{render_arguments}"
        """
    )

    with open(path, "w") as job_info_file:
        job_info_file.write(job_info_file_str)

    yield Output(path)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(path),
            # "job_info_file_str": MetadataValue.text(job_info_file_str),
            "job_info_file_str": MetadataValue.md(f"```\n{job_info_file_str}\n```"),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
    ins={
        "job_info_file": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "job_info_file"])
        ),
        "plugin_info_file": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "plugin_info_file"])
        ),
    }
)
def job_main(
        context: AssetExecutionContext,
        job_info_file: pathlib.Path,
        plugin_info_file: pathlib.Path,
) -> Generator[Output[Dict[str, str]] | AssetMaterialization | Any, Any, None]:

    ret = {
        "JobInfoFilePath": job_info_file.as_posix(),
        "PluginInfoFilePath": plugin_info_file.as_posix(),
    }

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    # deps=[
    #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "job_submission_tree"]),
    # ],
    ins={
        "render_output_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def archive_job_yaml(
        context: AssetExecutionContext,
        render_output_directory: pathlib.Path,
        job_model: JobBase,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    job_yaml = job_model.job_file_yaml

    if not render_output_directory.exists():
        raise FileNotFoundError(f"Rendering output directory {render_output_directory} does not exist yet.")

    try:
        shutil.move(job_yaml, render_output_directory)
    except FileNotFoundError as e:
        context.log.warning(f"Job YAML file {job_yaml} not found: {e}")

    ret = pathlib.Path(render_output_directory) / job_yaml.name

    if not ret.exists():
        raise FileNotFoundError(f"Job YAML file {job_yaml.name} could not be found in {render_output_directory}")

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(ret)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        # "combine_dicts": AssetIn(
        #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "combine_dicts"])
        # ),
        "render_output_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
        ),
        "render_output_filename": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_filename"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"])
        ),
    }
)
def render_arguments(
        context: AssetExecutionContext,
        # combine_dicts: dict,
        render_output_directory: pathlib.Path,
        render_output_filename: Dict,
        job_model: JobBase,
        CONFIG: DefaultConstants,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    args = job_model.plugin_model.args
    render_output = str(render_output_directory / CONFIG.RENDER_RAW_OUT / render_output_filename["padding_command"])

    job_model_dict = json.loads(
        job_model.model_dump_json(
            fallback=str,
        )
    )
    # Todo:
    #  - [x] why output_format had to be capital here?
    #        combine_dicts["yaml_submission"]["output_format"] = combine_dicts["yaml_submission"]["output_format"].upper()
    #        -> Blender requires that. Logic moved to the Blender Plugin
    job_model_dict["output_format"]: str = job_model_dict["output_format"].upper()

    plugin_model_dict = json.loads(
        job_model.plugin_model.model_dump_json(
            fallback=str,
        )
    )

    context.log.debug(f"{args = }")
    context.log.debug(f"{render_output = }")
    context.log.debug(f"{job_model_dict = }")
    context.log.debug(f"{plugin_model_dict = }")

    ret = " ".join(args).format(
        render_output=render_output,
        **job_model_dict,
        **plugin_model_dict,
    )

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
    ins={
        "render_output_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
        ),
        # "job_draft_png": AssetIn(
        #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "job_draft_png"])
        # ),
        # "job_draft_mov": AssetIn(
        #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "job_draft_mov"])
        # ),
        # "job_kitsu_publish": AssetIn(
        #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "job_kitsu_publish"])
        # ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        # "job_model": AssetIn(
        #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        # ),
        "job_main": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "job_main"])
        ),
    }
)
def job_submission_tree(
        context: AssetExecutionContext,
        render_output_directory: pathlib.Path,
        # job_draft_png: Dict,
        # job_draft_mov: Dict,
        # job_kitsu_publish: Dict,
        CONFIG: DefaultConstants,
        # job_model: JobBase,
        job_main: Dict[str, str],
) -> Generator[Output[dict[str, list[str]]] | AssetMaterialization | Any, Any, None]:

    ####
    # {
    #  Jobs:
    #  [
    #   {
    #    Job
    #    Deps
    #    Aux
    #   }
    #   {
    #    Job
    #    Deps
    #    Aux
    #   }
    #   {
    #    Job
    #    Deps
    #    Aux
    #   }
    #  ]
    # }
    #
    ####

    job_dict_template = CONFIG.JOB_DICT_TEMPLATE
    job_dict_main = job_dict_template.copy()
    job_dict_main.update(job_main)

    i = 0

    multiple_jobs_v2_dict = dict()
    multiple_jobs_v2_dict["Jobs"] = jobs = []
    job_0 = job_dict_main
    job_0_dependencies = job_0["JobDependencies"]  # we could add the jobs here, on which this job depends on
    job_0_index = i
    jobs.append(job_0)
    i += 1

    # if job_model.append_draft_job_png:
    #
    #     job = job_dict_template.copy()
    #     job["JobInfoFilePath"] = str(job_draft_png["JobInfoFilePath"])
    #     job["PluginInfoFilePath"] = str(job_draft_png["PluginInfoFilePath"])
    #     job_dependencies = job["JobDependencies"] = []  # Change from None to []
    #
    #     parents = [job_0_index]
    #
    #     for i_ in parents:
    #         job_dependencies.append(f"index://{i_}")
    #
    #     jobs.append(job)
    #     job_draft_png_index = i
    #     i += 1

    # if job_model.append_draft_job_mov:
    #
    #     job = job_dict_template.copy()
    #     job["JobInfoFilePath"] = str(job_draft_mov["JobInfoFilePath"])
    #     job["PluginInfoFilePath"] = str(job_draft_mov["PluginInfoFilePath"])
    #     job_dependencies = job["JobDependencies"] = []  # Change from None to []
    #
    #     parents = [job_0_index]
    #
    #     for i_ in parents:
    #         job_dependencies.append(f"index://{i_}")
    #
    #     jobs.append(job)
    #     job_draft_mov_index = i
    #     i += 1

    # if bool(job_model.kitsu_task) and job_model.with_kitsu_publish:
    #
    #     job = job_dict_template.copy()
    #     job["JobInfoFilePath"] = str(job_kitsu_publish["JobInfoFilePath"])
    #     job["PluginInfoFilePath"] = str(job_kitsu_publish["PluginInfoFilePath"])
    #     job_dependencies = job["JobDependencies"] = []  # Change from None to []
    #
    #     parents = [job_draft_mov_index]
    #
    #     for i_ in parents:
    #         job_dependencies.append(f"index://{i_}")
    #
    #     # self.LOGGER.info(f'Generating Kitsu Publish Job (MOV)...')
    #     # job_kitsu_publish_, job_kitsu_publish_jobinfo, job_kitsu_publish_plugininfo = self.job_kitsu_publish(parents=[job_draft_mov_index])
    #     jobs.append(job)
    #     job_draft_kitsu_publish_index = i
    #     i += 1

    # https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#plug-in-info-file
    # render_output_directory.mkdir(parents=True, exist_ok=True)
    submission_file = render_output_directory / CONFIG.SUBMISSION_JSON
    with open(submission_file, "w") as submit_v2:
        json.dump(multiple_jobs_v2_dict, submit_v2, ensure_ascii=False, indent=CONFIG.JSON_INDENT, sort_keys=True)

    cmd = [
        "/opt/Thinkbox/Deadline10/bin/deadlinecommand",
        "-SubmitMultipleJobsV2",
        "-jsonfilepath", f"{str(submission_file)}",
    ]

    ret = {"deadline_cmd": cmd}

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret)
        }
    )


# @asset(
#     **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
#     ins={
#         # "combine_dicts": AssetIn(),
#         "render_output_directory": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
#         ),
#         "render_output_filename": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_filename"])
#         ),
#         "batch_name": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "batch_name"])
#         ),
#         "job_title_str": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title_str"])
#         ),
#         "job_title": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title"])
#         ),
#         "resolution_draft": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "resolution_draft"])
#         ),
#         "annotations_string": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "annotations_string"])
#         ),
#         "CONFIG": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
#         ),
#         "frame_start_absolute": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_start_absolute"])
#         ),
#         "frame_end_absolute": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_end_absolute"])
#         ),
#         "job_model": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
#         ),
#     }
# )
# def job_draft_png(
#         context: AssetExecutionContext,
#         # combine_dicts: dict,
#         render_output_directory: pathlib.Path,
#         render_output_filename: dict,
#         batch_name: str,
#         job_title_str: str,
#         job_title: str,
#         resolution_draft: tuple,
#         annotations_string: str,
#         CONFIG: DefaultConstants,
#         frame_start_absolute: int,
#         frame_end_absolute: int,
#         job_model: JobBase,
# ) -> Generator[Output[dict[str, str]] | AssetMaterialization | Any, Any, None]:
#     """
#     The QuickDraft PNG Job
#
#     :param parents:
#     :return:
#     """
#
#     # job_title =  combine_dicts["yaml_submission"]["job_title"]
#
#     quick_type = "createImages"
#     codec = "png"
#
#     draft_out_dir = render_output_directory / "draft" / codec
#     draft_out_dir.mkdir(parents=True, exist_ok=True)
#
#     path_job_info = draft_out_dir / f"job_draft_{codec}_info_job.txt"
#
#     job_info_file_str = textwrap.dedent(
#         f"""\
#         BatchName={batch_name}
#         Name={job_title_str} (Draft {codec.upper()})
#         Frames={frame_start_absolute}-{frame_end_absolute}
#         Priority=0
#         ChunkSize=1000000
#         Plugin=DraftPlugin
#         OutputDirectory0={draft_out_dir}
#         OutputFilename0={job_model.plugin_model.padding_deadline}
#         InitialStatus={job_model.deadline_initial_status}
#         """
#     )
#
#     with open(path_job_info, "w") as job_info_file:
#         job_info_file.write(job_info_file_str)
#
#     path_plugin_info = draft_out_dir/f"job_draft_{codec}_info_plugin.txt"
#
#     plugin_info_file_str = textwrap.dedent(
#         f"""\
#         ScriptArg0=resolution="{CONFIG.RESOLUTION_DRAFT_SCALE}"
#         ScriptArg1=codec="{codec}"
#         ScriptArg2=colorSpaceIn="Identity"
#         ScriptArg3=colorSpaceOut="Identity"
#         ScriptArg4=annotationsString="{annotations_string}"
#         ScriptArg5=annotationsImageString="None"
#         ScriptArg6=annotationsResWidthString="{resolution_draft[0]}"
#         ScriptArg7=annotationsResHeightString="{resolution_draft[1]}"
#         ScriptArg8=annotationsFramePaddingSize="{CONFIG.PADDING}"
#         ScriptArg9=quality="85"
#         ScriptArg10=quickType="{quick_type}"
#         ScriptArg11=isDistributed="False"
#         ScriptArg12=frameList={frame_start_absolute}-{frame_end_absolute}
#         ScriptArg13=startFrame={frame_start_absolute}
#         ScriptArg14=endFrame={frame_end_absolute}
#         ScriptArg15=taskStartFrame={frame_start_absolute}
#         ScriptArg16=taskEndFrame={frame_end_absolute}
#         ScriptArg17=outFolder="{draft_out_dir}"
#         ScriptArg18=outFile="{draft_out_dir}/{job_title}.{"#" * CONFIG.PADDING}.{codec}"
#         ScriptArg19=inFile="{pathlib.Path(render_output_directory / CONFIG.RENDER_RAW_OUT / render_output_filename["padding_deadline"]).as_posix()}"
#         """
#     )
#
#     with open(path_plugin_info, "w") as plugin_info_file:
#         plugin_info_file.write(plugin_info_file_str)
#
#     ret = {
#         "JobInfoFilePath": str(path_job_info),
#         "PluginInfoFilePath": str(path_plugin_info),
#     }
#
#     yield Output(ret)
#
#     yield AssetMaterialization(
#         asset_key=context.asset_key,
#         metadata={
#             "__".join(context.asset_key.path): MetadataValue.json(ret)
#         }
#     )


# @asset(
#     **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
#     ins={
#         "render_output_directory": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"]),
#         ),
#         "render_output_filename": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_filename"]),
#         ),
#         "batch_name": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "batch_name"]),
#         ),
#         "job_title_str": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title_str"]),
#         ),
#         "job_title": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title"]),
#         ),
#         "resolution_draft": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "resolution_draft"]),
#         ),
#         "annotations_string": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "annotations_string"]),
#         ),
#         "CONFIG": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
#         ),
#         "frame_start_absolute": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_start_absolute"])
#         ),
#         "frame_end_absolute": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_end_absolute"])
#         ),
#         "job_model": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
#         ),
#         "fps": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "fps"])
#         ),
#     }
# )
# def job_draft_mov(
#         context: AssetExecutionContext,
#         render_output_directory: pathlib.Path,
#         render_output_filename: Dict,
#         batch_name: str,
#         job_title_str: str,
#         job_title: str,
#         resolution_draft: tuple,
#         annotations_string: str,
#         CONFIG: DefaultConstants,
#         frame_start_absolute: int,
#         frame_end_absolute: int,
#         job_model: JobBase,
#         fps: float,
# ) -> Generator[Output[dict[str, str]] | AssetMaterialization | Any, Any, None]:
#     """
#     The QuickDraft MOV Job
#
#     :return:
#     """
#
#     quick_type = "createMovie"
#     extension = "mov"
#     _codec = "h264"
#
#     draft_out_dir = render_output_directory / "draft" / extension
#     draft_out_dir.mkdir(parents=True, exist_ok=True)
#
#     path_job_info = draft_out_dir / f"job_draft_{extension}_info_job.txt"
#
#     job_info_file_str = textwrap.dedent(
#         f"""\
#         BatchName={batch_name}
#         Name={job_title_str} (Draft {extension.upper()})
#         Frames={frame_start_absolute}-{frame_end_absolute}
#         Priority=0
#         ChunkSize=1000000
#         Plugin=DraftPlugin
#         OutputDirectory0={draft_out_dir}
#         OutputFilename0={job_model.plugin_model.padding_deadline}
#         InitialStatus={job_model.deadline_initial_status}
#         """
#     )
#
#     with open(path_job_info, "w") as job_info_file:
#         job_info_file.write(job_info_file_str)
#
#     path_plugin_info = draft_out_dir / f"job_draft_{extension}_info_plugin.txt"
#
#     plugin_info_file_str = textwrap.dedent(
#         f"""\
#         ScriptArg0=resolution="{CONFIG.RESOLUTION_DRAFT_SCALE}"
#         ScriptArg1=codec="{_codec}"
#         ScriptArg2=colorSpaceIn="Identity"
#         ScriptArg3=colorSpaceOut="Identity"
#         ScriptArg4=annotationsString="{annotations_string}"
#         ScriptArg5=annotationsImageString="None"
#         ScriptArg6=annotationsResWidthString="{resolution_draft[0]}"
#         ScriptArg7=annotationsResHeightString="{resolution_draft[1]}"
#         ScriptArg8=annotationsFramePaddingSize="{CONFIG.PADDING}"
#         ScriptArg9=quality="85"
#         ScriptArg10=quickType="{quick_type}"
#         ScriptArg11=isDistributed="False"
#         ScriptArg12=frameList={frame_start_absolute}-{frame_end_absolute}
#         ScriptArg13=startFrame={frame_start_absolute}
#         ScriptArg14=endFrame={frame_end_absolute}
#         ScriptArg15=taskStartFrame=={frame_start_absolute}
#         ScriptArg16=taskEndFrame=={frame_end_absolute}
#         ScriptArg17=frameRate={fps}
#         ScriptArg18=outFolder="{draft_out_dir}"
#         ScriptArg19=outFile="{draft_out_dir}/{job_title}.{extension}"
#         ScriptArg20=inFile="{pathlib.Path(render_output_directory/ CONFIG.RENDER_RAW_OUT / render_output_filename["padding_deadline"]).as_posix()}"
#         """
#     )
#
#     with open(path_plugin_info, "w") as plugin_info_file:
#         plugin_info_file.write(plugin_info_file_str)
#         # TODO show and shot fps
#
#     ret = {
#         "JobInfoFilePath": str(path_job_info),
#         "PluginInfoFilePath": str(path_plugin_info),
#     }
#
#     yield Output(ret)
#
#     yield AssetMaterialization(
#         asset_key=context.asset_key,
#         metadata={
#             "__".join(context.asset_key.path): MetadataValue.json(ret)
#         }
#     )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "resolution": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "resolution"]),
        ),
    }
)
def resolution_draft(
        context: AssetExecutionContext,
        CONFIG: DefaultConstants,
        resolution: Resolution,
) -> Generator[Output[Resolution] | AssetMaterialization | Any, Any, None]:

    ret = Resolution(*tuple(ti * CONFIG.RESOLUTION_DRAFT_SCALE for ti in resolution))

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def resolution(
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
        job_model: JobBase,
) -> Generator[Output[Resolution] | AssetMaterialization | Any, Any, None]:

    resolution_job: Resolution = job_model.resolution

    resolution_kitsu_project = Resolution(*tuple(int(i) for i in str(get_kitsu_task_dict.get("project", {}).get("resolution", "0x0")).split("x")))
    resolution_kitsu_shot = Resolution(*tuple(int(i) for i in str(get_kitsu_task_dict.get("entity", {}).get("data", {}).get("resolution", "0x0")).split("x")))

    yield Output(resolution_job)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(resolution_job),
            "resolution_job": MetadataValue.json(resolution_job),
            "resolution_kitsu_project": MetadataValue.json(resolution_kitsu_project),
            "resolution_kitsu_shot": MetadataValue.json(resolution_kitsu_shot),
        }
    )


# @asset(
#     **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
#     ins={
#         "render_arguments": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_arguments"])
#         ),
#         "render_output_directory": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
#         ),
#         "version": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "version"])
#         ),
#         "batch_name": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "batch_name"])
#         ),
#         "job_title_str": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title_str"])
#         ),
#         "job_title": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title"])
#         ),
#         "CONFIG": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
#         ),
#         "job_model": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
#         ),
#         "frame_start_absolute": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_start_absolute"])
#         ),
#         "frame_end_absolute": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_end_absolute"])
#         ),
#     }
# )
# def job_kitsu_publish(
#         context: AssetExecutionContext,
#         render_arguments: str,
#         render_output_directory: pathlib.Path,
#         version: str,
#         batch_name: str,
#         job_title_str: str,
#         job_title: str,
#         CONFIG: DefaultConstants,
#         job_model: JobBase,
#         frame_start_absolute: int,
#         frame_end_absolute: int,
# ) -> Generator[Output[Dict[str, str]] | AssetMaterialization | Any, Any, None]:
#     """
#     The Kitsu-Publish Job
#
#     :return:
#     """
#
#     extension = "mov"
#
#     handles = job_model.handles
#
#     # TODO this is needed to find the movie, but could be more elegant
#     draft_out_dir = render_output_directory / "draft" / extension
#
#     kitsu_job_out_dir = render_output_directory / "kitsu"
#     kitsu_job_out_dir.mkdir(parents=True, exist_ok=True)
#
#     executable = CONFIG.GAZU_PY
#     args = []
#     # Todo:
#     #  - [ ] Use gazu[cli] directly
#     #        - [CLI](https://github.com/cgwire/gazu?tab=readme-ov-file#cli)
#     #          root@dagster:/dagster# gazu-cli --help
#     #          Usage: gazu-cli [OPTIONS] COMMAND [ARGS]...
#     #
#     #            Gazu CLI - Command-line client for the Kitsu API.
#     #
#     #          Options:
#     #            --json     Output as JSON.
#     #            --version  Show the version and exit.
#     #            --help     Show this message and exit.
#     #
#     #          Commands:
#     #            asset          Show details for an asset.
#     #            asset-types    List asset types.
#     #            assets         List assets for a project.
#     #            comment        Post a comment on a task (with status change).
#     #            episodes       List episodes for a project.
#     #            login          Log in to a Kitsu instance and store credentials.
#     #            logout         Log out and clear stored credentials.
#     #            my-tasks       List tasks assigned to current user.
#     #            persons        List all persons.
#     #            project        Show details for a project.
#     #            projects       List projects.
#     #            search         Search for entities across the Kitsu instance.
#     #            sequences      List sequences for a project.
#     #            shot-casting   Show casting (assets linked) for a shot.
#     #            shots          List shots for a project.
#     #            status         Show current connection status.
#     #            task           Show details for a task (by ID).
#     #            task-statuses  List task statuses.
#     #            task-types     List task types.
#     #            tasks          List tasks for a project.
#     args.extend(['<QUOTE>/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/custom/events/Kitsu/kitsu_submission_cli.py<QUOTE>'])
#     args.extend(['--very-verbose'])
#     args.extend(['--task-id', '<QUOTE>{}<QUOTE>'.format(str(job_model.kitsu_task))])
#     args.extend(['--comment', f'<QUOTE>'
#                               f'Output directory: `{render_output_directory}`<br>'
#                               f'Version: `{version}`<br>'
#                               f'Frames: `{handles}_{frame_start_absolute}-{frame_end_absolute}_{handles}`<br>'
#                               f'Comment: {job_model.comment}<br>'
#                               f'<br>'
#                               f'---<br>'
#                               f'<br>'
#                               f'Execution Command: `{job_model.plugin_model.executable.as_posix()} {render_arguments}`<br>'
#                               f'Submission Command: Todo<br>'
#                               f'Job file: `{job_model.job_file.as_posix()}`<br>'
#                               f'<QUOTE>'
#                               f''])
#     args.extend(['--host', f'<QUOTE>{"http://10.1.2.15:4545/api"}<QUOTE>'])  # Todo: make dynamic
#     args.extend(['--user', f'<QUOTE>{"admin@example.com"}<QUOTE>'])  # Todo: make dynamic
#     args.extend(['--password', f'<QUOTE>{"mysecretpassword"}<QUOTE>'])  # Todo: make dynamic
#     args.extend(['--movie-file', f'<QUOTE>{draft_out_dir}/{job_title}.{extension}<QUOTE>'])
#     args.extend(['--version', f'<QUOTE>{version}<QUOTE>'])
#
#     path_job_info = kitsu_job_out_dir / "job_kitsu_publish_info_job.txt"
#
#     job_info_file_str = textwrap.dedent(
#         f"""\
#         BatchName={batch_name}
#         Name={job_title_str} (Kitsu Publish)
#         Frames=1
#         Priority=0
#         ChunkSize=1000000
#         OutputDirectory0={draft_out_dir}
#         OutputFilename0={job_model.plugin_model.padding_deadline}
#         InitialStatus={job_model.deadline_initial_status}
#         Plugin=CommandLine
#         ForceReloadPlugin=True
#         """
#     )
#
#     with open(path_job_info, "w") as job_info_file:
#         job_info_file.write(job_info_file_str)
#
#     path_plugin_info = kitsu_job_out_dir / "job_draft_kitsu_publish_info_plugin.txt"
#
#     plugin_info_file_str = textwrap.dedent(
#         f"""\
#         Executable={executable}
#         Arguments={" ".join(args)}
#         """
#     )
#
#     with open(path_plugin_info, "w") as plugin_info_file:
#         plugin_info_file.write(plugin_info_file_str)
#
#     ret = {
#         "JobInfoFilePath": str(path_job_info),
#         "PluginInfoFilePath": str(path_plugin_info),
#     }
#
#     yield Output(ret)
#
#     yield AssetMaterialization(
#         asset_key=context.asset_key,
#         metadata={
#             "__".join(context.asset_key.path): MetadataValue.json(ret)
#         }
#     )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
    # # This can fail if the job has already been archived
    # deps=[
    #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "archive_job_yaml"]),
    # ],
    ins={
        "render_output_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"]),
        ),
        "job_submission_tree": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "job_submission_tree"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "get_task_url": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "get_task_url"])
        ),
    },
)
def export_combined_dict(
        context: AssetExecutionContext,
        render_output_directory: pathlib.Path,
        job_submission_tree: Dict,
        CONFIG: DefaultConstants,
        job_model: JobBase,
        get_task_url: str,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    """
    Before:
    cat "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/037/4_1197-1254_4/combined_dict.json"

    After
    cat "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/045/4_0997-1104_4/combined_dict.json"
    """

    job_model.farm_cmd = job_submission_tree
    job_model.task_url = get_task_url

    out = render_output_directory / "combined_dict.json"

    # model_dict = json.loads(
    #     job_model.model_dump_json(
    #         fallback=str,
    #         indent=CONFIG.JSON_INDENT,
    #     )
    # )

    model_dict = job_model.model_dump(
        fallback=str,
    )

    with open(out, "w") as fo:
        json.dump(
            obj=model_dict,
            fp=fo,
            indent=CONFIG.JSON_INDENT,
            sort_keys=True,
            default=str,
        )

    yield Output(out)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(out),
            "model_dict": MetadataValue.md(
                f"```json\n{json.dumps(model_dict, default=str, indent=CONFIG.JSON_INDENT)}\n```"
            ),
            "destination": MetadataValue.path(out.parent),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
    # # This can fail if the job has already been archived
    # deps=[
    #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "archive_job_yaml"]),
    # ],
    ins={
        "job_info_file": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "job_info_file"]),
        ),
        "plugin_info_file": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "plugin_info_file"]),
        ),
    },
)
def job(
        context: AssetExecutionContext,
        job_info_file: pathlib.Path,
        plugin_info_file: pathlib.Path,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    """
    Before:
    cat "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/037/4_1197-1254_4/combined_dict.json"

    After
    cat "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/045/4_0997-1104_4/combined_dict.json"
    """

    # job_model.farm_cmd = job_submission_tree
    # job_model.task_url = get_task_url
    #
    # out = render_output_directory / "combined_dict.json"
    #
    # # model_dict = json.loads(
    # #     job_model.model_dump_json(
    # #         fallback=str,
    # #         indent=CONFIG.JSON_INDENT,
    # #     )
    # # )
    #
    # model_dict = job_model.model_dump(
    #     fallback=str,
    # )
    #
    # with open(out, "w") as fo:
    #     json.dump(
    #         obj=model_dict,
    #         fp=fo,
    #         indent=CONFIG.JSON_INDENT,
    #         sort_keys=True,
    #         default=str,
    #     )

    yield Output(out)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        # metadata={
        #     "__".join(context.asset_key.path): MetadataValue.path(out),
        #     "model_dict": MetadataValue.md(
        #         f"```json\n{json.dumps(model_dict, default=str, indent=CONFIG.JSON_INDENT)}\n```"
        #     ),
        #     "destination": MetadataValue.path(out.parent),
        # }
    )
