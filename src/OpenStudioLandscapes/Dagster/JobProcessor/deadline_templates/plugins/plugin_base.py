import os
from typing import List

from pydantic import BaseModel, Field

args = list()

plugin = {
    "submitter":
    {
        "executable": None,
        "output_formats_plugin": ["png", "exr", "jpg"],
        "args": args,
        "padding_deadline": "'#' * EVAL_PADDING",  # results in "####"
        "padding_command": "'#' * EVAL_PADDING",   # results in "####"
    }
}


# Refactor to Pydantic


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


# class PluginBase(BaseModel):
#     submitter: SubmitterBase = Field()