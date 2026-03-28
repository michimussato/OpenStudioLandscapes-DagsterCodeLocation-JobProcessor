import os

from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.nuke import PluginNukeBase

# plugin["submitter"]["executable"] = REZ_PACKAGES / "nuke" / "15.0v4" / "Nuke15.0"


class PluginNuke_15_0v4(PluginNukeBase):
    executable: os.PathLike = REZ_PACKAGES / "nuke" / "15.0v4" / "Nuke15.0"
