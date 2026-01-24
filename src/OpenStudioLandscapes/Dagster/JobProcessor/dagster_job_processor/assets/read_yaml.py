import pathlib
import re
import importlib.util
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Generator

from dagster import (
    asset, AssetIn, MetadataValue,
    AssetMaterialization, Output,
    Config, AssetExecutionContext,
)
import json

from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.resources import KitsuResource


# TODO
#  rename to generate_job_submission_scripts


group_name = 'DEADLINE_GENERATE_JOB_SCRIPTS'


test_jobs = ['blender', 'houdini', 'nuke'][0]


class IngestJobConfig(Config):
    filename: str


@asset(
    group_name=group_name,
    description="Parses the job file.",
)
def read_job_py(
        context: AssetExecutionContext,
        config: IngestJobConfig,
) -> Generator[Output[Any] | AssetMaterialization | Any, Any, None]:

    parent = config.filename

    spec = importlib.util.spec_from_file_location(str(pathlib.Path(parent).parent).replace(os.sep, '.'), parent)
    module_from_spec = importlib.util.module_from_spec(spec)
    sys.modules[str(pathlib.Path(parent).parent).replace(os.sep, '.')] = module_from_spec
    spec.loader.exec_module(module_from_spec)
    job = module_from_spec.job

    job['job_file_py'] = config.filename

    yield Output(job)

    yield AssetMaterialization(
        asset_key="read_job_py",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(job),
        }
    )


# @asset(
#     ins={
#         "read_job_py": AssetIn(),
#     },
#     group_name=group_name,
#     description="Parses the plugin file.",
# )
# def read_plugin_py(
#         read_job_py: dict,
# ) -> dict:
#
#     # plugin_dict = read_job_py['plugin_dict']
#
#     # if parent is None:
#     #     raise Exception(f'Plugin file not set: {read_job_py["plugin_file"] = }')
#     #
#     # spec = importlib.util.spec_from_file_location(str(pathlib.Path(parent).parent).replace(os.sep, '.'), parent)
#     # module_from_spec = importlib.util.module_from_spec(spec)
#     # sys.modules[str(pathlib.Path(parent).parent).replace(os.sep, '.')] = module_from_spec
#     # spec.loader.exec_module(module_from_spec)
#     # plugin = module_from_spec.plugin
#
#     if read_job_py['plugin_dict']['submitter']['executable'] is None:
#         raise Exception(f'Plugin executable not set: {plugin = }')
#
#     yield Output(plugin)
#
#     yield AssetMaterialization(
#         asset_key="read_plugin_py",
#         metadata={
#             'json': MetadataValue.json(plugin)
#         }
#     )


# @asset(
#     group_name=group_name,
#     ins={
#         "read_job_py": AssetIn(),
#         # "read_plugin_py": AssetIn(),
#     },
# )
# def merge_dicts(
#         read_job_py: dict,
#         # read_plugin_py: dict,
# ) -> dict:
#     """Merges the `job.py` dict and the `plugin.py` dict
#      into one single dict and returns its contents as a `MaterializeResult` object in the JSON format."""
#
#     # merge dicts
#     yaml_dict = read_job_py | read_plugin_py
#
#     # https://discuss.dagster.io/t/18787421/u0667dnc02y-when-returning-a-materializeresult-from-an-asset#87efa45e-008f-4d1d-b628-01fd07220ff6
#     # https://discuss.dagster.io/t/18787421/u0667dnc02y-when-returning-a-materializeresult-from-an-asset#891a726e-e379-4c14-a19c-64ec7945e344
#
#     yield Output(yaml_dict)
#
#     yield AssetMaterialization(
#         asset_key="merge_dicts",
#         metadata={
#             'json': MetadataValue.json(yaml_dict)
#         }
#     )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn()
    },
)
def get_kitsu_task_dict(
        context: AssetExecutionContext,
        kitsu_resource: KitsuResource,
        read_job_py: dict,
) -> Generator[Output[Any] | AssetMaterialization | Any, Any, None]:
    """Returns a Kitsu task dict as a MaterializeResult object in the JSON format."""

    # TODO: make fail safe

    task_id = read_job_py["kitsu_task"]
    task_dict = kitsu_resource.get_kitsu_task_dict(task_id=task_id)

    yield Output(task_dict)

    yield AssetMaterialization(
        asset_key="get_kitsu_task_dict",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(task_dict),
        }
    )


@asset(
    group_name=group_name,
    ins={"get_kitsu_task_dict": AssetIn()},
)
def get_task_url(
        context: AssetExecutionContext,
        kitsu_resource: KitsuResource,
        get_kitsu_task_dict: dict,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    """Returns a Kitsu task dict as a MaterializeResult object in the JSON format."""

    # TODO: make fail safe

    # if bool(merge_dicts["kitsu_task"]):
    if "error" in get_kitsu_task_dict:
        raise Exception(f"Kitsu task ID is set but can't get Task URL from Kitsu for this shot:\n"
                        f"{get_kitsu_task_dict['error']}")

    task_dict = get_kitsu_task_dict
    task_url = kitsu_resource.get_task_url(task_dict=task_dict)

    yield Output(task_url)

    yield AssetMaterialization(
        asset_key="get_task_url",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.url(task_url),
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "version": AssetIn(),
        "PADDING": AssetIn(),
        "RESOLUTION_DRAFT_SCALE": AssetIn(),
    },
)
def annotations_string(
        context: AssetExecutionContext,
        combine_dicts: dict,
        version: str,
        PADDING: int,
        RESOLUTION_DRAFT_SCALE: float,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    """Returns the annotations string for the Deadline Draft jobs as a MaterializeResult object in the JSON format."""

    frame_start_absolute = combine_dicts['yaml_submission']['frame_start']
    frame_end_absolute = combine_dicts['yaml_submission']['frame_end']
    handles = combine_dicts['yaml_submission']['handles']

    resolution = combine_dicts['yaml_submission']["resolution"]

    fps = combine_dicts['yaml_submission']["fps"]

    fi = frame_start_absolute + handles
    fo = frame_end_absolute - handles

    if bool(combine_dicts["yaml_submission"]["kitsu_task"]):
        if combine_dicts["entity_type"]["name"] == 'Shot':
            fi = combine_dicts['entity']['data']['frame_in']
            fo = combine_dicts['entity']['data']['frame_out']

    fi_fo = (fi, fo)

    rgb = 95
    draft_annotations_string = {
        "NorthWest": {
            "text": f"{combine_dicts['entity']['name']}/{combine_dicts['task_type']['name']}",  # Todo: Add Sequence name to Shot if Shot and Shot is part of Sequence
            "colorR": rgb,
            "colorG": rgb,
            "colorB": rgb,
            "type": ""
        },
        "NorthCenter": {
            "text": f"{pathlib.Path(combine_dicts['yaml_submission']['job_file']).name}",
            "colorR": rgb,
            "colorG": rgb,
            "colorB": rgb,
            "type": ""
        }, "NorthEast": {
            "text": f"$time ({version})",
            "colorR": rgb,
            "colorG": rgb,
            "colorB": rgb,
            "type": ""
        }, "SouthWest": {
            "text": f"",
            "colorR": rgb,
            "colorG": rgb,
            "colorB": rgb,
            "type": ""
        },
        "SouthCenter": {
            "text": f"{handles}_{str(fi_fo[0]).zfill(PADDING)}||{handles}_{str(frame_start_absolute + handles).zfill(PADDING)}|$frame|{str(frame_end_absolute - handles).zfill(PADDING)}_{handles}||{str(fi_fo[1]).zfill(PADDING)}_{handles} @{fps}",
            "colorR": rgb,
            "colorG": rgb,
            "colorB": rgb,
            "type": ""
        },
        "SouthEast": {
            "text": f"{resolution[0]}x{resolution[1]} (x{RESOLUTION_DRAFT_SCALE})",
            "colorR": rgb,
            "colorG": rgb,
            "colorB": rgb,
            "type": ""
        }
    }

    yield Output(json.dumps(draft_annotations_string))

    yield AssetMaterialization(
        asset_key="annotations_string",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(draft_annotations_string),
            'annotations_string': MetadataValue.text(json.dumps(draft_annotations_string))
        }
    )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn(),
        "get_kitsu_task_dict": AssetIn(),
        "get_task_url": AssetIn(),
        "handles": AssetIn(),
        "frame_start_absolute": AssetIn(),
        "frame_end_absolute": AssetIn(),
        "resolution": AssetIn(),
        "show_name": AssetIn(),
        "job_title": AssetIn(),
        "render_version_directory": AssetIn(),
        "task_name": AssetIn(),
        "fps": AssetIn(),
        "output_format": AssetIn(),
        "JOB_DICT_TEMPLATE": AssetIn(),
    },
)
def combine_dicts(
        context: AssetExecutionContext,
        read_job_py: dict,
        get_kitsu_task_dict: dict,
        get_task_url: str,
        handles: int,
        frame_start_absolute: int,
        frame_end_absolute: int,
        resolution: tuple,
        show_name: str,
        job_title: str,
        render_version_directory: str,
        task_name: str,
        fps: float,
        output_format: str,
        JOB_DICT_TEMPLATE: dict,
) -> Generator[Output[dict] | AssetMaterialization | Any, Any, None]:

    read_job_py.update({"handles": handles})
    read_job_py.update({"frame_start": frame_start_absolute})
    read_job_py.update({"frame_end": frame_end_absolute})
    read_job_py.update({"resolution": resolution})
    read_job_py.update({"show_name": show_name})
    read_job_py.update({"job_title": job_title})
    read_job_py.update({"render_version_directory": render_version_directory})
    read_job_py.update({"task_name": task_name})
    read_job_py.update({"fps": fps})
    read_job_py.update({"output_format": output_format})

    get_kitsu_task_dict['yaml_submission'] = read_job_py
    get_kitsu_task_dict['job_dict_template'] = JOB_DICT_TEMPLATE
    get_kitsu_task_dict['task_url'] = get_task_url
    get_kitsu_task_dict['deadline_job_submitted'] = False
    get_kitsu_task_dict['deadline_job_queued'] = False
    get_kitsu_task_dict['deadline_job_submitted_result'] = None

    yield Output(get_kitsu_task_dict)

    yield AssetMaterialization(
        asset_key="combine_dicts",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(get_kitsu_task_dict),
        }
    )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn(),
        "get_kitsu_task_dict": AssetIn(),
        "show_name": AssetIn(),
        "task_name": AssetIn(),
        "OUTPUT_ROOT": AssetIn(),
    },
)
def render_version_directory(
        context: AssetExecutionContext,
        read_job_py: dict,
        get_kitsu_task_dict: dict,
        show_name: str,
        task_name: str,
        OUTPUT_ROOT: pathlib.Path,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:

    # TODO: make this fail safe
    if bool({read_job_py["kitsu_task"]}):
        entity_name = get_kitsu_task_dict["entity"]["name"]
    else:
        entity_name = 'No Entity Name'

    entity_type = f'{get_kitsu_task_dict["entity_type"]["name"]}/{entity_name}'

    _out = pathlib.Path(f'{OUTPUT_ROOT}/{show_name}/{entity_type}/{task_name}/')
    _out.mkdir(parents=True, exist_ok=True)

    yield Output(str(_out))

    yield AssetMaterialization(
        asset_key="render_version_directory",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(_out),
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
    },
)
def version(
        context: AssetExecutionContext,
        combine_dicts: dict,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    # This directory must exist in order for it to be iterable

    padding = 3

    render_version_directory = pathlib.Path(combine_dicts['yaml_submission']['render_version_directory'])

    pattern = re.compile(f'^[0-9]{{{padding}}}')

    dirs = [i.name for i in render_version_directory.iterdir() if i.is_dir() and pattern.match(i.name)]
    dirs.append(str(0).zfill(padding))
    dirs.sort()
    version_ = max(dirs)
    new_version = str(int(version_) + 1).zfill(padding)
    new_version_dir = pathlib.Path(f'{render_version_directory}/{new_version}')
    new_version_dir.mkdir(parents=True, exist_ok=True)

    yield Output(new_version)

    yield AssetMaterialization(
        asset_key="version",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(new_version),
            'dirs': MetadataValue.json(dirs),
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
    },
)
def render_output_filename(
        context: AssetExecutionContext,
        combine_dicts: dict,
) -> Generator[Output[dict[str, str]] | AssetMaterialization | Any, Any, None]:

    job_title = combine_dicts['yaml_submission']['job_title']

    output_format = combine_dicts['yaml_submission']['output_format']

    # if 'output_format' in combine_dicts['yaml_submission']:
    #     if combine_dicts['yaml_submission']['output_format'] is not None:
    #         output_format = combine_dicts['yaml_submission']['output_format']

    padding_deadline = f"{combine_dicts['yaml_submission']['plugin_dict']['submitter']['padding_deadline']}"
    padding_command = f"{combine_dicts['yaml_submission']['plugin_dict']['submitter']['padding_command']}"

    # Don't uncomment
    # Required to eval(padding_deadline) and eval(padding_command)
    from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor.settings import PADDING as EVAL_PADDING

    ret = {
        'padding_deadline': f'{job_title}.{eval(padding_deadline)}.{output_format}',
        'padding_command': f'{job_title}.{eval(padding_command)}.{output_format}',
    }

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="render_output_filename",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "version": AssetIn(),
        "PADDING": AssetIn(),
    }
)
def render_output_directory(
        context: AssetExecutionContext,
        combine_dicts: dict,
        version: str,
        PADDING: int,
) -> Generator[Output[Path] | AssetMaterialization | Any, Any, None]:

    handles = combine_dicts['yaml_submission']['handles']
    render_version_directory = pathlib.Path(combine_dicts['yaml_submission']['render_version_directory'])

    _out = render_version_directory / version

    if bool(combine_dicts["yaml_submission"]["kitsu_task"]):
        if combine_dicts["entity_type"]["name"] == 'Shot':
            _out = _out / f'{str(handles)}_{str(combine_dicts["yaml_submission"]["frame_start"]).zfill(PADDING)}-{str(combine_dicts["yaml_submission"]["frame_end"]).zfill(PADDING)}_{str(handles)}'  # _out.joinpath(f'')

    yield Output(_out)

    yield AssetMaterialization(
        asset_key="render_output_directory",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(_out)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn(),
    }
)
def job_title(
        context: AssetExecutionContext,
        read_job_py: dict,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    base, first_dot, rest = pathlib.Path(read_job_py["job_file"]).name.partition('.')

    yield Output(base)

    yield AssetMaterialization(
        asset_key="job_title",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(base)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn(),
        "get_kitsu_task_dict": AssetIn(),
    }
)
def show_name(
        context: AssetExecutionContext,
        read_job_py: dict,
        get_kitsu_task_dict: dict,
) -> Generator[Output[str | Any] | AssetMaterialization | Any, Any, None]:
    if bool(read_job_py["kitsu_task"]):
        ret = get_kitsu_task_dict['project']['name']
    else:
        ret = 'No Show'

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="show_name",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn(),
        "get_kitsu_task_dict": AssetIn(),
    }
)
def task_name(
        context: AssetExecutionContext,
        read_job_py: dict,
        get_kitsu_task_dict: dict,
) -> Generator[Output[str | Any] | AssetMaterialization | Any, Any, None]:
    if bool(read_job_py["kitsu_task"]):
        ret = get_kitsu_task_dict['task_type']['name']
    else:
        ret = 'No Task Name'

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="task_name",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "version": AssetIn(),
        "PADDING": AssetIn(),
    }
)
def job_title_str(
        context: AssetExecutionContext,
        combine_dicts: dict,
        version: str,
        PADDING: int,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    _entity_info = combine_dicts["entity"]["name"]

    handles = combine_dicts['yaml_submission']['handles']
    show_name = combine_dicts['yaml_submission']['show_name']
    task_name = combine_dicts['yaml_submission']['task_name']

    if bool(combine_dicts['yaml_submission']["kitsu_task"]):
        if combine_dicts["entity_type"]["name"] == 'Shot':
            _entity_info = f'{_entity_info} - {str(handles)}_{str(combine_dicts["yaml_submission"]["frame_start"]).zfill(PADDING)}-{str(combine_dicts["yaml_submission"]["frame_end"]).zfill(PADDING)}_{handles}'
            # _entity_info = f'{self.sequence_name}_{self.entity_name} - {str(self.handles)}_{str(self.frame_start).zfill(self.PADDING)}-{str(self.frame_end).zfill(self.PADDING)}_{self.handles}'

    ret = f'{show_name} - {_entity_info} - {task_name} - {pathlib.Path(combine_dicts["yaml_submission"]["job_file"]).name} - {version} - {pathlib.Path(combine_dicts["yaml_submission"]["plugin_dict"]["submitter"]["executable"]).name}'

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="job_title_str",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "job_title_str": AssetIn(),
    }
)
def batch_name(
        context: AssetExecutionContext,
        job_title_str: str
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:

    ret = f'Batch: {job_title_str}'

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="batch_name",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "render_output_directory": AssetIn(),
        "render_output_filename": AssetIn(),
        "batch_name": AssetIn(),
    }
)
def props(
        context: AssetExecutionContext,
        combine_dicts: dict,
        render_output_directory: pathlib.Path,
        render_output_filename: dict,
        batch_name: str,
) -> Generator[Output[list[str]] | AssetMaterialization | Any, Any, None]:

    props = [
        ('Comment', f'{combine_dicts["yaml_submission"]["comment"]}'),  # TODO
        ('ForceReloadPlugin', True),
        ('InitialStatus', combine_dicts["yaml_submission"]["deadline_initial_status"]),
        ('OutputDirectory0', f'{render_output_directory}'),
        ('OutputFilename0', f'{render_output_filename["padding_deadline"]}'),
        ('BatchName', f'{batch_name}'),
        # This should not end up in plugin_info_file it seems: https://docs.thinkboxsoftware.com/products/deadline/10.1/1_User%20Manual/manual/manual-submission.html#job-info-ref-label
    ]

    props_ = [f'{k}={v}' for k, v in props]

    yield Output(props_)

    yield AssetMaterialization(
        asset_key="props",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(props_)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn(),
        "DEFAULT_HANDLES": AssetIn(),
    }
)
def handles(
        context: AssetExecutionContext,
        read_job_py: dict,
        DEFAULT_HANDLES: int,
) -> Generator[Output[int | Any] | AssetMaterialization | Any, Any, None]:
    """Handles with default"""
    key = "handles"
    if key in read_job_py:
        ret = read_job_py[key]
    else:
        ret = DEFAULT_HANDLES

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.int(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn(),
        "get_kitsu_task_dict": AssetIn(),
        "DEFAULT_FPS": AssetIn(),
    }
)
def fps(
        context: AssetExecutionContext,
        read_job_py: dict,
        get_kitsu_task_dict: dict,
        DEFAULT_FPS: float,
) -> Generator[Output[float] | AssetMaterialization | Any, Any, None]:

    """
    frame_in = get_kitsu_task_dict["entity"]["data"]["frame_in"]
    frame_out = get_kitsu_task_dict["entity"]["data"]["frame_out"]
    nb_frames = get_kitsu_task_dict["entity"]["nb_frames"]
    """

    if bool(read_job_py["kitsu_task"]):
        if "error" in get_kitsu_task_dict:
            raise Exception(f"Kitsu task ID is set but can't get FPS from Kitsu for this shot:\n"
                            f"{get_kitsu_task_dict['error']}")

    if "fps" in read_job_py:
        if bool(read_job_py["fps"]):
            fps = float(read_job_py["fps"])

    elif bool(read_job_py["kitsu_task"]):
        fps = float(get_kitsu_task_dict['project']['fps'])
        if get_kitsu_task_dict["entity_type"]["name"] == 'Shot':
            if get_kitsu_task_dict['entity']['data'] is not None:
                fps = float(get_kitsu_task_dict['entity']['data']['fps'])
    else:
        fps = DEFAULT_FPS

    yield Output(fps)

    yield AssetMaterialization(
        asset_key="fps",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.float(fps)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn(),
    },
    description="Returns the output format of the render."
)
def output_format(
        context: AssetExecutionContext,
        read_job_py: dict,
) -> Generator[Output[Any] | AssetMaterialization | Any, Any, None]:

    if read_job_py['output_format'] is None:
        raise ValueError("output_format is not defined.")

    if read_job_py['output_format'] not in read_job_py["plugin_dict"]['submitter']['output_formats_plugin']:
        raise ValueError(f"output_format is not supported: {read_job_py['output_format']}")

    yield Output(read_job_py['output_format'])

    yield AssetMaterialization(
        asset_key="output_format",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(read_job_py['output_format'])
        }
    )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn(),
        "handles": AssetIn(),
        "DEFAULT_FRAME_START": AssetIn(),
        "DONT_ALLOW_NEGATIVE_FRAMES": AssetIn(),
    }
)
def frame_start_absolute(
        context: AssetExecutionContext,
        read_job_py: dict,
        handles: int,
        DEFAULT_FRAME_START: int,
        DONT_ALLOW_NEGATIVE_FRAMES: bool,
) -> Generator[Output[int | Any] | AssetMaterialization | Any, Any, None]:

    """
    frame_in = get_kitsu_task_dict["entity"]["data"]["frame_in"]
    frame_out = get_kitsu_task_dict["entity"]["data"]["frame_out"]
    nb_frames = get_kitsu_task_dict["entity"]["nb_frames"]
    """

    fs = DEFAULT_FRAME_START

    if "frame_start" in read_job_py:
        if bool(read_job_py["frame_start"]):
            fs = read_job_py["frame_start"]

    fsa = fs - handles

    if DONT_ALLOW_NEGATIVE_FRAMES:
        raise Exception('Negative frames not allowed')

    yield Output(fsa)

    yield AssetMaterialization(
        asset_key="frame_start_absolute",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.int(fsa)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "read_job_py": AssetIn(),
        "get_kitsu_task_dict": AssetIn(),
        "handles": AssetIn(),
        "DEFAULT_FRAME_START": AssetIn(),
        "DONT_ALLOW_NEGATIVE_FRAMES": AssetIn(),
    }
)
def frame_end_absolute(
        context: AssetExecutionContext,
        read_job_py: dict,
        get_kitsu_task_dict: dict,
        handles: int,
        DEFAULT_FRAME_START: int,
        DONT_ALLOW_NEGATIVE_FRAMES: bool,
) -> Generator[Output[int | Any] | AssetMaterialization | Any, Any, None]:

    nb_frames = get_kitsu_task_dict["entity"]["nb_frames"]
    fe = DEFAULT_FRAME_START + (nb_frames - 1)

    if "frame_end" in read_job_py:
        if bool(read_job_py["frame_end"]):
            fe = read_job_py["frame_end"]

    fea = fe + handles

    if DONT_ALLOW_NEGATIVE_FRAMES:
        raise Exception('Negative frames not allowed')

    # if self._frame_end is None:
    #     if self.use_kitsu:
    #         if self.entity_type_name == 'Shot':
    #             self._frame_end = self.shot_frame_out
    #             self.LOGGER.info(f'Frame End automatically set to {self._frame_end}')
    #
    # assert self._frame_end is not None, 'Set Frame End manually first (cannot use Kitsu).'

    yield Output(fea)

    yield AssetMaterialization(
        asset_key="frame_end_absolute",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.int(fea)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "FRAME_JUMPS": AssetIn(),
    }
)
def frames(
        context: AssetExecutionContext,
        combine_dicts: dict,
        FRAME_JUMPS: list,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:

    frame_start_absolute = combine_dicts['yaml_submission']['frame_start']
    frame_end_absolute = combine_dicts['yaml_submission']['frame_end']

    # make sure we filter frame jumps according to the chunk_size
    # for nuke, render time could be way slower if it has
    # to be launched for every single frame
    # frame_jumps = [i for i in constants.FRAME_JUMPS if i <= combine_dicts['yaml_submission']['chunk_size']]

    if combine_dicts['yaml_submission']['chunk_size'] > 1:
        frame_jumps = [min(FRAME_JUMPS)]
    else:
        frame_jumps = FRAME_JUMPS

    frame_list = ",".join([
        f'{frame_start_absolute}-{frame_end_absolute}x{int(i)}'
        for i in frame_jumps
    ])

    yield Output(frame_list)

    yield AssetMaterialization(
        asset_key="frames",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(frame_list)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "batch_name": AssetIn(),
        "job_title_str": AssetIn(),
        "render_output_directory": AssetIn(),
        "frames": AssetIn(),
        "props": AssetIn(),
    }
)
def job_info_file(
        context: AssetExecutionContext,
        combine_dicts: dict,
        batch_name: str,
        job_title_str: str,
        render_output_directory: pathlib.Path,
        frames: str,
        props: list,
) -> Generator[Output[Path] | AssetMaterialization | Any, Any, None]:

    # https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#job-info-file-options
    render_output_directory.mkdir(parents=True, exist_ok=True)
    path = render_output_directory / 'jobinfo_info.txt'
    with open(path, 'w') as job_info_file:
        job_info_file.write(f'InitialStatus={combine_dicts["yaml_submission"]["deadline_initial_status"]}\n')
        job_info_file.write(f'BatchName={batch_name}\n')
        job_info_file.write(f'Name={job_title_str}\n')
        job_info_file.write(f'Frames={frames}\n')
        job_info_file.write(f'ChunkSize={combine_dicts["yaml_submission"]["chunk_size"]}\n')
        job_info_file.write(f'Plugin=CommandLine\n')
        job_info_file.write(f'StartupDirectory=\n')
        for prop in props:
            job_info_file.write(f'{prop}\n')

    yield Output(path)

    yield AssetMaterialization(
        asset_key="job_info_file",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(path)
        }
    )


@asset(
    group_name=group_name,
    deps=['job_submission_tree'],
    ins={
        "render_output_directory": AssetIn(),
        "combine_dicts": AssetIn(),
    }
)
def paste_job_py(
        context: AssetExecutionContext,
        render_output_directory: pathlib.Path,
        combine_dicts: dict,
) -> Generator[Output[Path] | AssetMaterialization | Any, Any, None]:

    job_py = pathlib.Path(combine_dicts["yaml_submission"]['job_file_py'])

    shutil.move(job_py, render_output_directory)

    ret = pathlib.Path(render_output_directory) / job_py.name

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="paste_job_py",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "render_output_directory": AssetIn(),
        "render_output_filename": AssetIn(),
    }
)
def render_arguments(
        context: AssetExecutionContext,
        combine_dicts: dict,
        render_output_directory: pathlib.Path,
        render_output_filename: dict,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    args = combine_dicts["yaml_submission"]["plugin_dict"]["submitter"]["args"]

    combine_dicts["yaml_submission"]["output_format"] = combine_dicts["yaml_submission"]["output_format"].upper()
    render_output = str(render_output_directory / render_output_filename["padding_command"])

    ret = " ".join(args).format(
        render_output=render_output,
        **combine_dicts["yaml_submission"],
    )

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="render_arguments",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "render_output_directory": AssetIn(),
        "combine_dicts": AssetIn(),
        "render_arguments": AssetIn(),
    }
)
def plugin_info_file(
        context: AssetExecutionContext,
        render_output_directory: pathlib.Path,
        combine_dicts: dict,
        render_arguments: str,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    # https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#plug-in-info-file
    render_output_directory.mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(f'{render_output_directory}/plugin_info.txt')
    with open(path, 'w') as job_info_file:
        job_info_file.write(f'Executable={combine_dicts["yaml_submission"]["plugin_dict"]["submitter"]["executable"]}\n')
        job_info_file.write(f'Arguments="{render_arguments}"\n')

    yield Output(path)

    yield AssetMaterialization(
        asset_key="plugin_info_file",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(path)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "render_output_directory": AssetIn(),
        "job_info_file": AssetIn(),
        "plugin_info_file": AssetIn(),
        "job_draft_png": AssetIn(),
        "job_draft_mov": AssetIn(),
        "job_kitsu_publish": AssetIn(),
        "JSON_INDENT": AssetIn(),
        "SUBMISSION_JSON": AssetIn(),
        "JOB_DICT_TEMPLATE": AssetIn(),
    }
)
def job_submission_tree(
        context: AssetExecutionContext,
        combine_dicts: dict,
        render_output_directory: pathlib.Path,
        job_info_file: pathlib.Path,
        plugin_info_file: pathlib.Path,
        job_draft_png: dict,
        job_draft_mov: dict,
        job_kitsu_publish: dict,
        JSON_INDENT: int,
        SUBMISSION_JSON: str,
        JOB_DICT_TEMPLATE: dict,
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

    job_dict_template = JOB_DICT_TEMPLATE
    job_dict_main = job_dict_template.copy()
    job_dict_main['JobInfoFilePath'] = str(job_info_file)
    job_dict_main['PluginInfoFilePath'] = str(plugin_info_file)

    i = 0

    multiple_jobs_v2_dict = dict()
    multiple_jobs_v2_dict['Jobs'] = jobs = []
    job_0 = job_dict_main
    job_0_dependencies = job_0['JobDependencies']  # we could add the jobs here, on which this job depends on
    job_0_index = i
    jobs.append(job_0)
    i += 1

    if combine_dicts["yaml_submission"]["append_draft_job_png"]:

        job = job_dict_template.copy()
        job['JobInfoFilePath'] = str(job_draft_png['JobInfoFilePath'])
        job['PluginInfoFilePath'] = str(job_draft_png['PluginInfoFilePath'])
        job_dependencies = job['JobDependencies'] = []  # Change from None to []

        parents = [job_0_index]

        for i_ in parents:
            job_dependencies.append(f'index://{i_}')

        jobs.append(job)
        job_draft_png_index = i
        i += 1

    if combine_dicts["yaml_submission"]["append_draft_job_mov"]:

        job = job_dict_template.copy()
        job['JobInfoFilePath'] = str(job_draft_mov['JobInfoFilePath'])
        job['PluginInfoFilePath'] = str(job_draft_mov['PluginInfoFilePath'])
        job_dependencies = job['JobDependencies'] = []  # Change from None to []

        parents = [job_0_index]

        for i_ in parents:
            job_dependencies.append(f'index://{i_}')

        jobs.append(job)
        job_draft_mov_index = i
        i += 1

    if bool(combine_dicts['yaml_submission']["kitsu_task"]) and bool(combine_dicts['yaml_submission']["with_kitsu_publish"]):

        job = job_dict_template.copy()
        job['JobInfoFilePath'] = str(job_kitsu_publish['JobInfoFilePath'])
        job['PluginInfoFilePath'] = str(job_kitsu_publish['PluginInfoFilePath'])
        job_dependencies = job['JobDependencies'] = []  # Change from None to []

        parents = [job_draft_mov_index]

        for i_ in parents:
            job_dependencies.append(f'index://{i_}')

        # self.LOGGER.info(f'Generating Kitsu Publish Job (MOV)...')
        # job_kitsu_publish_, job_kitsu_publish_jobinfo, job_kitsu_publish_plugininfo = self.job_kitsu_publish(parents=[job_draft_mov_index])
        jobs.append(job)
        job_draft_kitsu_publish_index = i
        i += 1

    # https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#plug-in-info-file
    render_output_directory.mkdir(parents=True, exist_ok=True)
    submission_file = render_output_directory / SUBMISSION_JSON
    with open(submission_file, 'w') as submit_v2:
        json.dump(multiple_jobs_v2_dict, submit_v2, ensure_ascii=False, indent=JSON_INDENT, sort_keys=True)

    cmd = [
        '/opt/Thinkbox/Deadline10/bin/deadlinecommand',
        '-SubmitMultipleJobsV2',
        '-jsonfilepath', f'{str(submission_file)}',
    ]

    ret = {"deadline_cmd": cmd}

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="job_submission_tree",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "render_output_directory": AssetIn(),
        "render_output_filename": AssetIn(),
        "batch_name": AssetIn(),
        "job_title_str": AssetIn(),
        "resolution_draft": AssetIn(),
        "annotations_string": AssetIn(),
        "PADDING": AssetIn(),
        "RESOLUTION_DRAFT_SCALE": AssetIn(),
    }
)
def job_draft_png(
        context: AssetExecutionContext,
        combine_dicts: dict,
        render_output_directory: pathlib.Path,
        render_output_filename: dict,
        batch_name: str,
        job_title_str: str,
        resolution_draft: tuple,
        annotations_string: str,
        PADDING: int,
        RESOLUTION_DRAFT_SCALE: float,
) -> Generator[Output[dict[str, str]] | AssetMaterialization | Any, Any, None]:
    """
    The QuickDraft PNG Job

    :param parents:
    :return:
    """

    frame_start_absolute = combine_dicts['yaml_submission']['frame_start']
    frame_end_absolute = combine_dicts['yaml_submission']['frame_end']
    job_title = combine_dicts['yaml_submission']['job_title']

    quick_type = "createImages"
    codec = "png"

    draft_out_dir = render_output_directory / 'draft' / codec
    draft_out_dir.mkdir(parents=True, exist_ok=True)

    path_job_info = draft_out_dir / f'job_draft_{codec}_info_job.txt'
    with open(path_job_info, 'w') as job_info_file:
        job_info_file.write(f'BatchName={batch_name}\n')
        job_info_file.write(f'Name={job_title_str} (Draft {codec.upper()})\n')
        job_info_file.write(f'Frames={frame_start_absolute}-{frame_end_absolute}\n')
        job_info_file.write(f'Priority=0\n')
        job_info_file.write(f'ChunkSize=1000000\n')
        job_info_file.write(f'Plugin=DraftPlugin\n')
        job_info_file.write(f'OutputDirectory0={draft_out_dir}\n')
        job_info_file.write(f'OutputFilename0={render_output_filename["padding_deadline"]}\n')
        job_info_file.write(f'InitialStatus=Suspended\n')

    path_plugin_info = draft_out_dir/f'job_draft_{codec}_info_plugin.txt'
    with open(path_plugin_info, 'w') as plugin_info_file:
        plugin_info_file.write(f'ScriptArg0=resolution="{RESOLUTION_DRAFT_SCALE}"\n')
        plugin_info_file.write(f'ScriptArg1=codec="{codec}"\n')
        plugin_info_file.write(f'ScriptArg2=colorSpaceIn="Identity"\n')
        plugin_info_file.write(f'ScriptArg3=colorSpaceOut="Identity"\n')
        plugin_info_file.write(f'ScriptArg4=annotationsString="{annotations_string}"\n')
        plugin_info_file.write(f'ScriptArg5=annotationsImageString="None"\n')
        plugin_info_file.write(f'ScriptArg6=annotationsResWidthString="{resolution_draft[0]}"\n')
        plugin_info_file.write(f'ScriptArg7=annotationsResHeightString="{resolution_draft[1]}"\n')
        plugin_info_file.write(f'ScriptArg8=annotationsFramePaddingSize="{PADDING}"\n')
        plugin_info_file.write(f'ScriptArg9=quality="85"\n')
        plugin_info_file.write(f'ScriptArg10=quickType="{quick_type}"\n')
        plugin_info_file.write(f'ScriptArg11=isDistributed="False"\n')
        plugin_info_file.write(f'ScriptArg12=frameList={frame_start_absolute}-{frame_end_absolute}\n')
        plugin_info_file.write(f'ScriptArg13=startFrame={frame_start_absolute}\n')
        plugin_info_file.write(f'ScriptArg14=endFrame={frame_end_absolute}\n')
        plugin_info_file.write(f'ScriptArg15=taskStartFrame={frame_start_absolute}\n')
        plugin_info_file.write(f'ScriptArg16=taskEndFrame={frame_end_absolute}\n')
        plugin_info_file.write(f'ScriptArg17=outFolder="{draft_out_dir}"\n')
        plugin_info_file.write('ScriptArg18=outFile="{}/{}.{}.{}"\n'.format(draft_out_dir, job_title, "#" * PADDING, codec))
        in_file = render_output_directory / render_output_filename["padding_deadline"]
        plugin_info_file.write(f'ScriptArg19=inFile="{str(in_file)}"\n')

    ret = {
        'JobInfoFilePath': str(path_job_info),
        'PluginInfoFilePath': str(path_plugin_info),
    }

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="job_draft_png",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "render_output_directory": AssetIn(),
        "render_output_filename": AssetIn(),
        "batch_name": AssetIn(),
        "job_title_str": AssetIn(),
        "resolution_draft": AssetIn(),
        "annotations_string": AssetIn(),
        "PADDING": AssetIn(),
        "RESOLUTION_DRAFT_SCALE": AssetIn(),
    }
)
def job_draft_mov(
        context: AssetExecutionContext,
        combine_dicts: dict,
        render_output_directory: pathlib.Path,
        render_output_filename: dict,
        batch_name: str,
        job_title_str: str,
        resolution_draft: tuple,
        annotations_string: str,
        PADDING: int,
        RESOLUTION_DRAFT_SCALE: float,
) -> Generator[Output[dict[str, str]] | AssetMaterialization | Any, Any, None]:
    """
    The QuickDraft MOV Job

    :param parents:
    :return:
    """

    frame_start_absolute = combine_dicts['yaml_submission']['frame_start']
    frame_end_absolute = combine_dicts['yaml_submission']['frame_end']
    job_title = combine_dicts['yaml_submission']['job_title']

    annotations_string = annotations_string

    quick_type = "createMovie"
    extension = "mov"
    _codec = "h264"

    draft_out_dir = render_output_directory / 'draft' / extension
    draft_out_dir.mkdir(parents=True, exist_ok=True)

    path_job_info = draft_out_dir / f'job_draft_{extension}_info_job.txt'
    with open(path_job_info, 'w') as job_info_file:
        job_info_file.write(f'BatchName={batch_name}\n')
        job_info_file.write(f'Name={job_title_str} (Draft {extension.upper()})\n')
        job_info_file.write(f'Frames={frame_start_absolute}-{frame_end_absolute}\n')
        job_info_file.write(f'Priority=0\n')
        job_info_file.write(f'ChunkSize=1000000\n')
        job_info_file.write(f'Plugin=DraftPlugin\n')
        job_info_file.write(f'OutputDirectory0={draft_out_dir}\n')
        job_info_file.write(f'OutputFilename0={render_output_filename["padding_deadline"]}\n')
        job_info_file.write(f'InitialStatus=Suspended\n')

    path_plugin_info = draft_out_dir / f'job_draft_{extension}_info_plugin.txt'
    with open(path_plugin_info, 'w') as plugin_info_file:
        plugin_info_file.write(f'ScriptArg0=resolution="{RESOLUTION_DRAFT_SCALE}"\n')
        plugin_info_file.write(f'ScriptArg1=codec="{_codec}"\n')
        plugin_info_file.write(f'ScriptArg2=colorSpaceIn="Identity"\n')
        plugin_info_file.write(f'ScriptArg3=colorSpaceOut="Identity"\n')
        plugin_info_file.write(f'ScriptArg4=annotationsString="{annotations_string}"\n')
        plugin_info_file.write(f'ScriptArg5=annotationsImageString="None"\n')
        plugin_info_file.write(f'ScriptArg6=annotationsResWidthString="{resolution_draft[0]}"\n')
        plugin_info_file.write(f'ScriptArg7=annotationsResHeightString="{resolution_draft[1]}"\n')
        plugin_info_file.write(f'ScriptArg8=annotationsFramePaddingSize="{PADDING}"\n')
        plugin_info_file.write(f'ScriptArg9=quality="85"\n')
        plugin_info_file.write(f'ScriptArg10=quickType="{quick_type}"\n')
        plugin_info_file.write(f'ScriptArg11=isDistributed="False"\n')
        plugin_info_file.write(f'ScriptArg12=frameList={frame_start_absolute}-{frame_end_absolute}\n')
        plugin_info_file.write(f'ScriptArg13=startFrame={frame_start_absolute}\n')
        plugin_info_file.write(f'ScriptArg14=endFrame={frame_end_absolute}\n')
        plugin_info_file.write(f'ScriptArg15=taskStartFrame=={frame_start_absolute}\n')
        plugin_info_file.write(f'ScriptArg16=taskEndFrame=={frame_end_absolute}\n')
        # TODO show and shot fps
        plugin_info_file.write('ScriptArg17=frameRate={}\n'.format(combine_dicts['entity']['data']['fps']))
        plugin_info_file.write(f'ScriptArg18=outFolder="{draft_out_dir}"\n')
        plugin_info_file.write(f'ScriptArg19=outFile="{draft_out_dir}/{job_title}.{extension}"\n')
        in_file = render_output_directory / render_output_filename["padding_deadline"]
        plugin_info_file.write(f'ScriptArg20=inFile="{str(in_file)}"\n')

    ret = {
        'JobInfoFilePath': str(path_job_info),
        'PluginInfoFilePath': str(path_plugin_info),
    }

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="job_draft_mov",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "RESOLUTION_DRAFT_SCALE": AssetIn(),
    }
)
def resolution_draft(
        context: AssetExecutionContext,
        combine_dicts: dict,
        RESOLUTION_DRAFT_SCALE: float,
) -> Generator[Output[tuple[float | Any, ...]] | AssetMaterialization | Any, Any, None]:

    resolution = combine_dicts['yaml_submission']["resolution"]

    ret = tuple(ti * RESOLUTION_DRAFT_SCALE for ti in resolution)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="resolution_draft",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "get_kitsu_task_dict": AssetIn(),
        "read_job_py": AssetIn(),
        "DEFAULT_RESOLUTION": AssetIn(),
    }
)
def resolution(
        context: AssetExecutionContext,
        get_kitsu_task_dict: dict,
        read_job_py: dict,
        DEFAULT_RESOLUTION: tuple[int, int],
) -> Generator[Output[tuple[int, ...] | None | tuple[int, int] | Any] | AssetMaterialization | Any, Any, None]:

    resolution_project = get_kitsu_task_dict['project']['resolution']
    resolution_shot = get_kitsu_task_dict["entity"]["data"]["resolution"]

    resolution_manual = None

    if 'resolution' in read_job_py:
        resolution_manual = read_job_py['resolution']

    if bool(read_job_py["kitsu_task"]):
        if get_kitsu_task_dict["entity_type"]["name"] == 'Shot':
            r = resolution_shot
        else:
            r = resolution_project
        w_h = tuple(int(i) for i in str(r).split('x'))
    else:
        w_h = resolution_manual or DEFAULT_RESOLUTION

    yield Output(w_h)

    yield AssetMaterialization(
        asset_key="resolution",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(w_h)
        }
    )


@asset(
    group_name=group_name,
    ins={
        "combine_dicts": AssetIn(),
        "render_arguments": AssetIn(),
        "render_output_directory": AssetIn(),
        "render_output_filename": AssetIn(),
        "version": AssetIn(),
        "batch_name": AssetIn(),
        "job_title_str": AssetIn(),
        "GAZU_PY": AssetIn(),
    }
)
def job_kitsu_publish(
        context: AssetExecutionContext,
        combine_dicts: dict,
        render_arguments: str,
        render_output_directory: pathlib.Path,
        render_output_filename: dict,
        version: str,
        batch_name: str,
        job_title_str: str,
        GAZU_PY: str,
) -> Generator[Output[dict[str, str]] | AssetMaterialization | Any, Any, None]:
    """
    The Kitsu-Publish Job

    :param parents:
    :return:
    """

    extension = "mov"

    handles = combine_dicts['yaml_submission']['handles']
    job_title = combine_dicts['yaml_submission']['job_title']

    # TODO this is needed to find the movie, but could be more elegant
    draft_out_dir = render_output_directory / 'draft' / extension

    kitsu_job_out_dir = render_output_directory / 'kitsu'
    kitsu_job_out_dir.mkdir(parents=True, exist_ok=True)

    executable = GAZU_PY
    args = []
    args.extend(['<QUOTE>/nfs/deadline-repository/DeadlineRepository10/custom/events/Kitsu/kitsu_submission_cli.py<QUOTE>'])
    args.extend(['--task-id', '<QUOTE>{}<QUOTE>'.format(combine_dicts['yaml_submission']["kitsu_task"])])
    args.extend(['--comment', f'<QUOTE>'
                              f'Output directory: `{render_output_directory}`<br>'
                              f'Version: `{version}`<br>'
                              f'Frames: `{handles}_{combine_dicts["yaml_submission"]["frame_start"]}-{combine_dicts["yaml_submission"]["frame_end"]}_{handles}`<br>'
                              f'Comment: {combine_dicts["yaml_submission"]["comment"]}<br>'
                              f'<br>'
                              f'---<br>'
                              f'<br>'
                              f'Execution Command: `{combine_dicts["yaml_submission"]["plugin_dict"]["submitter"]["executable"]} {render_arguments}`<br>'
                              f'Submission Command: Todo<br>'
                              f'Job file: `{combine_dicts["yaml_submission"]["job_file"]}`<br>'
                              f'<QUOTE>'
                              f''])
    args.extend(['--host', f'<QUOTE>{"http://10.1.2.15/api"}<QUOTE>'])
    args.extend(['--user', f'<QUOTE>{"michimussato@gmail.com"}<QUOTE>'])
    args.extend(['--password', f'<QUOTE>{"mysecretpassword"}<QUOTE>'])
    args.extend(['--movie-file', f'<QUOTE>{draft_out_dir}/{job_title}.{extension}<QUOTE>'])
    args.extend(['--version', f'<QUOTE>{version}<QUOTE>'])

    path_job_info = kitsu_job_out_dir / 'job_kitsu_publish_info_job.txt'
    with open(path_job_info, 'w') as job_info_file:
        job_info_file.write(f'BatchName={batch_name}\n')
        job_info_file.write(f'Name={job_title_str} (Kitsu Publish)\n')
        job_info_file.write(f'Frames=1\n')
        job_info_file.write(f'Priority=0\n')
        job_info_file.write(f'ChunkSize=1000000\n')
        job_info_file.write(f'OutputDirectory0={draft_out_dir}\n')
        job_info_file.write(f'OutputFilename0={render_output_filename["padding_deadline"]}\n')
        job_info_file.write(f'InitialStatus=Suspended\n')
        job_info_file.write(f'Plugin=CommandLine\n')
        job_info_file.write(f'ForceReloadPlugin=True\n')

    path_plugin_info = kitsu_job_out_dir / 'job_draft_kitsu_publish_info_plugin.txt'
    with open(path_plugin_info, 'w') as plugin_info_file:
        plugin_info_file.write(f'Executable={executable}\n')
        plugin_info_file.write(f'Arguments={" ".join(args)}\n')

    ret = {
        'JobInfoFilePath': str(path_job_info),
        'PluginInfoFilePath': str(path_plugin_info),
    }

    yield Output(ret)

    yield AssetMaterialization(
        asset_key="job_kitsu_publish",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret)
        }
    )


@asset(
    group_name=group_name,
    deps=['paste_job_py'],
    ins={
        "render_output_directory": AssetIn(),
        "combine_dicts": AssetIn(),
        "job_submission_tree": AssetIn(),
        "JSON_INDENT": AssetIn(),
    },
)
def export_combined_dict(
        context: AssetExecutionContext,
        render_output_directory: pathlib.Path,
        combine_dicts: dict,
        job_submission_tree: dict,
        JSON_INDENT: int,
) -> Generator[Output[Path] | AssetMaterialization | Any, Any, None]:

    combine_dicts['deadline_cmd'] = job_submission_tree

    out = render_output_directory / 'combined_dict.json'

    with open(out, 'w') as fo:
        json.dump(combine_dicts, fo, indent=JSON_INDENT, sort_keys=True)

    yield Output(out)

    yield AssetMaterialization(
        asset_key="export_combined_dict",
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(out),
            'destination': MetadataValue.path(out.parent),
        }
    )
