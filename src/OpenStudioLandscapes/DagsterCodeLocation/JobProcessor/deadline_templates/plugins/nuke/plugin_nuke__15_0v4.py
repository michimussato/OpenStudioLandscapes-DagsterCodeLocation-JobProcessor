import pathlib
from typing import Literal

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.nuke import PluginNukeBase


class PluginNuke_15_0v4(PluginNukeBase):
    plugin_type: Literal['PluginNuke_15_0v4']

    executable: pathlib.Path = REZ_PACKAGES / "nuke" / "15.0v4" / "Nuke15.0"
