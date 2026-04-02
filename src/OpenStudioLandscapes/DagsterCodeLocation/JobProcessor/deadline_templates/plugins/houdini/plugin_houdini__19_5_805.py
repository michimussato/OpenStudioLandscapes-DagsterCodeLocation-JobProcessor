import pathlib
from typing import Literal

from pydantic.fields import Field

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.houdini import PluginHoudiniBase


class PluginHoudini_19_5_805(PluginHoudiniBase):
    plugin_type: Literal['PluginHoudini_19_5_805']

    executable: pathlib.Path = REZ_PACKAGES /  "houdini" / "19.5.805" / "hython"

    rop: str = Field(
        default="",
        description="The path to the render operator (ROP) to use "
                    "for rendering.",
    )
