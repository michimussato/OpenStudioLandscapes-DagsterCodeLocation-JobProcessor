import os
from typing import Literal

from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.houdini import PluginHoudiniBase


class PluginHoudini_19_5_805(PluginHoudiniBase):
    plugin_type: Literal['PluginHoudini_19_5_805']

    executable: os.PathLike = REZ_PACKAGES /  "houdini" / "19.5.805" / "hython"
