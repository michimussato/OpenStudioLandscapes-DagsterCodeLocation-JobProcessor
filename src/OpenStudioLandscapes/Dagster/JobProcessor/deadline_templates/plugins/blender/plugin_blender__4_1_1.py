import os
from typing import Literal

from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender import PluginBlenderBase


class PluginBlender_4_1_1(PluginBlenderBase):
    plugin_type: Literal['PluginBlender_4_1_1']

    executable: os.PathLike = REZ_PACKAGES / "blender" / "4.1.1" / "blender"
