import pathlib

from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender import plugin, PluginBlenderBase

plugin["submitter"]["executable"] = pathlib.Path(REZ_PACKAGES / "blender" / "4.1.1" / "blender").as_posix()


class PluginBlender_4_1_1(PluginBlenderBase):
    executable = REZ_PACKAGES / "blender" / "4.1.1" / "blender"
