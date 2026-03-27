from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.nuke import plugin, PluginNukeBase

plugin["submitter"]["executable"] = REZ_PACKAGES / "nuke" / "15.0v4" / "Nuke15.0"


class PluginNuke_15_0(PluginNukeBase):
    executable = REZ_PACKAGES / "nuke" / "15.0v4" / "Nuke15.0"
