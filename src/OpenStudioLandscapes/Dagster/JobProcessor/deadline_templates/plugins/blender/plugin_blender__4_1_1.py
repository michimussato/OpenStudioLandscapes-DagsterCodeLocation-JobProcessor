import pathlib

from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender.plugin_blender_base import plugin

plugin["submitter"]["executable"] = pathlib.Path(REZ_PACKAGES / "blender" / "4.1.1" / "blender").as_posix()
