import os
import pathlib
from typing import Dict, List, Any

from dagster import (
    get_dagster_logger,
)
from pydantic import (
    BaseModel,
    Field,
)

LOG = get_dagster_logger(__name__)

"""
Resources:
- https://app.studyraid.com/en/read/15002/518529/conditional-validation-based-on-other-fields
- https://thelinuxcode.com/work-with-pydantic-fields-detailed-examination/
- https://www.youtube.com/watch?v=Vj-iU-8_xLs
- https://www.youtube.com/watch?v=502XOB0u8OY
- https://docs.pydantic.dev/2.0/usage/models/
"""


FRAME_JUMP_SERIES_LENGTH: int = 5


from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *

class DefaultConstants(BaseModel):
    OUTPUT_ROOT: pathlib.Path = Field(
        default=AWSPORTAL_ROOT_1.joinpath("out"),
    )
    INPUT_ROOT: pathlib.Path = Field(
        default=pathlib.Path(
            os.environ.get("OPENSTUDIOLANDSCAPES__DAGSTER_JOBS_IN", "/data/share/in")
        ),
    )
    @property
    def INPUT_ROOT_PROCESSED(self) -> pathlib.Path:
        return self.INPUT_ROOT.joinpath(".processing")

    PADDING: int = Field(
        default=4,
    )
    PADDING_VERSION: int = Field(
        default=3,
    )
    JSON_INDENT: int = Field(
        default=2,
    )
    FRAME_JUMPS: List[int] = Field(
        default=list(reversed([2**i for i in range(0, FRAME_JUMP_SERIES_LENGTH)])),
    )
    OUTPUT_FORMAT_DEFAULT: str = Field(
        default=[
            "exr",
        ][0],
    )
    RESOLUTION_DRAFT_SCALE: float = Field(
        default=0.5,
    )
    DEFAULT_HANDLES: int = Field(
        default=4,
    )
    DEFAULT_FRAME_START: int = Field(
        default=1001,
    )
    DONT_ALLOW_NEGATIVE_FRAMES: bool = Field(
        default=False,
    )
    DEFAULT_RESOLUTION: tuple = Field(
        default=(1920, 1080),
    )
    DEFAULT_FPS: float = Field(
        default=24.0,
    )
    SUBMISSION_JSON: str = Field(
        default="submission.json",
    )
    GAZU_PY: str = Field(
        default=pathlib.Path("/opt/python3.11/bin/python3.11").as_posix(),
    )
    JOB_DICT_TEMPLATE: Dict[str, Any] = Field(
        default={
            "JobInfoFilePath": "",
            "PluginInfoFilePath": "",
            "JobDependencies": None,
            "AuxiliaryFiles": []
        },
    )
    RENDER_RAW_OUT: str = Field(
        default="raw",
        description="The subfolder where the raw renders will go."
    )


class Submitter(BaseModel):
    pass
