from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.houdini import plugin, PluginHoudiniBase

plugin["submitter"]["executable"] = REZ_PACKAGES /  "houdini" / "19.5.805" / "hython"

class PluginHoudini_19_5(PluginHoudiniBase):
    executable = REZ_PACKAGES /  "houdini" / "19.5.805" / "hython"
