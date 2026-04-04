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
    padding_command: str = Field(
        default="'#' * EVAL_PADDING",  # Results in #####
        description="The padding character for arbitrary commands",
    )
    padding_oiiotool: str = Field(
        # default="'#' * EVAL_PADDING",
        default="'%' + str(EVAL_PADDING).zfill(2) + 'd'",  # Results in '%04d'
        description="The padding character for arbitrary commands",
    )
