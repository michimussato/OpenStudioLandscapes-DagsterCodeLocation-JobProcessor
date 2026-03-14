from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.houdini.plugin_houdini_base import plugin

plugin["submitter"]["executable"] = REZ_PACKAGES /  "houdini" / "19.5.805" / "hython"
