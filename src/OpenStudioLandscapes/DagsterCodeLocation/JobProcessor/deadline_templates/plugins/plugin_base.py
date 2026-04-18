import pathlib
from typing import List

from pydantic import BaseModel, Field


class PluginBase(BaseModel):
    executable: pathlib.Path = Field(
        default=None,
    )
    output_formats_plugin: List[str] = [
        "png",
        "exr",
        "jpg",
    ]
    args: List[str] = Field(
        default_factory=list,
    )
    padding_deadline: str = Field(
        default="'#' * EVAL_PADDING",  # Results in ####
        description="The padding character for Deadline",
    )
    # https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#arbitrary-command-line-jobs
    padding_deadline_batch_startframe: str = Field(
        default="'<STARTFRAME%' + str(EVAL_PADDING).zfill(1) + '>'",  # Results in '<STARTFRAME>%4'
        description="Todo",
    )
    padding_deadline_batch_endframe: str = Field(
        default="'<ENDFRAME%' + str(EVAL_PADDING).zfill(1) + '>'",  # Results in '<ENDFRAME>%4'
        description="Todo",
    )
    padding_command: str = Field(
        default="'#' * EVAL_PADDING",  # Results in #####
        description="The padding character for arbitrary commands",
    )
    padding_oiiotool: str = Field(
        # default="'#' * EVAL_PADDING",
        default="'%' + str(EVAL_PADDING).zfill(2) + 'd'",  # Results in '%04d'
        description="The padding character for arbitrary commands",
    )
