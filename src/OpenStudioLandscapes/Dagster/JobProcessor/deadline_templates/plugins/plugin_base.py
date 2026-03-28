import os
from typing import List

from pydantic import BaseModel, Field


class PluginBase(BaseModel):
    executable: os.PathLike = Field(
        default=None,
    )
    output_formats_plugin: List[str] = ["png", "exr", "jpg"]
    args: List[str] = Field(
        default_factory=list,
    )
    padding_deadline: str = Field(
        default="'#' * EVAL_PADDING",
        description="The padding character for Deadline",
    )
    padding_command: str = Field(
        default="'#' * EVAL_PADDING",
        description="The padding character for arbitrary commands",
    )
