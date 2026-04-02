import pathlib
from typing import Literal

from pydantic import Field

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.blender import PluginBlenderBase, RenderEngine


class PluginBlender_4_1_1(PluginBlenderBase):
    plugin_type: Literal['PluginBlender_4_1_1']

    executable: pathlib.Path = REZ_PACKAGES / "blender" / "4.1.1" / "blender"

    render_engine: RenderEngine = Field(
        default=RenderEngine.WORKBENCH.value,
        examples=[i.value for i in RenderEngine],
    )
