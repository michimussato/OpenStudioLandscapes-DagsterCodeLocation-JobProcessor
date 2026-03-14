from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.nuke.plugin_nuke_base import plugin

plugin["submitter"]["executable"] = REZ_PACKAGES / "nuke" / "15.0v4" / "Nuke15.0"
