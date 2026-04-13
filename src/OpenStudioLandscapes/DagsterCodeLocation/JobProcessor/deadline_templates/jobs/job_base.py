import datetime
import pathlib
import uuid
import enum
from typing import Union, Dict, NamedTuple

from pydantic import BaseModel, Field

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.blender.plugin_blender__4_1_1 import PluginBlender_4_1_1
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.houdini.plugin_houdini__19_5_805 import PluginHoudini_19_5_805
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.nuke.plugin_nuke__15_0v4 import PluginNuke_15_0v4


class InitialStatuses(enum.StrEnum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"

class OutputFormats(enum.StrEnum):
    PNG = "png"
    EXR = "exr"
    JPG = "jpg"
    TGA = "tga"

class Resolution(NamedTuple):
    x: int
    y: int

class WorkRange(NamedTuple):  # aka ShotRange
    cut_in: int
    cut_out: int

class CutRange(NamedTuple):
    cut_in: int
    cut_out: int

# job: dict = {
#     "job_file": None,
#     "plugin_dict": {},
#     "plugin_file": None,
#     "job_uuid": str(uuid.uuid4()),
#     "job_timestamp": str(datetime.datetime.timestamp(datetime.datetime.now())),
#     "handles": 4,
#     "output_formats": [str(i.value) for i in OutputFormats],
#     "output_format": OutputFormats.EXR.value,
#     "chunk_size": 1,
#     "initial_statuses": [str(i.value) for i in InitialStatuses],
#     "deadline_initial_status": InitialStatuses.SUSPENDED.value,
#     "append_draft_job_png": False,
#     "append_draft_job_mov": False,
#     "with_kitsu_publish": False,
#     "deadline_job_with_draft": False,
#     "comment": "",
#     "frame_start": 1001,
#     "frame_end": 1100,
#     "resolution_draft_scale": 0.5,
#     "kitsu_task": "",  # SQ010 / SQ010_SH030  Layout  http://miniboss/productions/6c5dfed4-0f11-48f7-aba2-4d4d5cce85fc/shots/tasks/9bb09bfa-0a97-40c6-a6e6-27405b198570
# }


class JobBase(BaseModel):

    job_file: pathlib.Path = Field(
        default=None,
        description="The file to render",
        examples=[
            "/server/scenes/blender/sh030_001.blend",
            "/server/scenes/nuke/sh030_001.nk",
        ]
    )

    job_file_yaml: pathlib.Path = Field(
        default=None,
        description="The path to the YAML file that was submitted",
        examples=[
            "/server/jobs/job.yaml",
            "/server/jobs/job2.yml",
        ]
    )

    farm_cmd: Dict = Field(
        default_factory=dict,
        description="The command to run to send the job to the render farm",
    )

    farm_job_queued: bool = Field(
        default=False,
        description="The command to run to send the job to the render farm",
    )

    task_url: str = Field(
        default_factory=str,
        description="The URL to the Kitsu task",
    )

    plugin_model: Union[
        PluginBlender_4_1_1,
        PluginHoudini_19_5_805,
        PluginNuke_15_0v4,
    ] = Field(
        # Help on discriminator:
        # - https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions-with-callable-discriminator
        description="The plugin model",
        discriminator="plugin_type",
    )
    # plugin_file: os.PathLike = Field(
    #     # This is probably not necessary anymore when working with YAML files
    #     default=None,
    #     description="The file that defines the plugin model",
    # )
    job_uuid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        exclude=True,
    )
    job_timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now().timestamp,
        exclude=True,
    )
    # handles: PositiveInt = Field(
    handles: int = Field(
        default=4,
    )
    output_format: str = Field(
        default=OutputFormats.EXR.value,
        description="The render output format",
        examples=[i.name for i in OutputFormats],
    )
    # chunk_size: PositiveInt = Field()
    # pydantic.errors.PydanticUserError: The `__modify_schema__` method is not supported in Pydantic v2. Use `__get_pydantic_json_schema__` instead in class `PositiveInt`.
    #
    # For further information visit https://errors.pydantic.dev/2.12/u/custom-json-schema
    chunk_size: int = Field(
        default=1,
        description="The chunk size",
    )
    deadline_initial_status: str = Field(
        default=InitialStatuses.SUSPENDED.value,
        description="The initial job status after submission",
        examples=[i.name for i in OutputFormats],
    )
    append_draft_job_png: bool = Field(
        default=False,
    )
    append_draft_job_mov: bool = Field(
        default=False,
    )
    # with_kitsu_publish: bool = Field(
    #     default=False,
    # )
    # deadline_job_with_draft: bool = Field(
    #     default=False,
    # )
    comment: str = Field(
        default_factory=str,
        description="The comment for a render job",
    )
    cut_in: int = Field(
        default=1001,
        description="The cut in",
    )
    cut_out: int = Field(
        default=1100,
        description="The cut out",
    )
    # resolution_draft_scale: PositiveFloat = Field(
    resolution_draft_scale: float = Field(
        default=0.5,
        description="Scale factor for the draft jobs",
    )
    kitsu_task: uuid.UUID = Field(
        default=None,
        description="The kitsu task UUID",
    )
    fps: float = Field(
        default=25.0,
        description="Frames per second",
    )
    resolution: Resolution = Field(
        default=Resolution(
            x=1920,
            y=1080,
        ),
        description="Resolution",
    )
    work_range: WorkRange = Field(
        default=WorkRange(
            cut_in=997,
            cut_out=1104,
        ),
        description="Work range; shot range (includes handles)).",
    )
    cut_range: CutRange = Field(
        default=CutRange(
            cut_in=1001,
            cut_out=1100,
        ),
        description="Cut range (excludes handles).",
    )
