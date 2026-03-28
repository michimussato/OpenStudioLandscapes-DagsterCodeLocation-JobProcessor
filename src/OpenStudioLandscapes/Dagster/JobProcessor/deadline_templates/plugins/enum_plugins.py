import enum

from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender.plugin_blender__4_1_1 import PluginBlender_4_1_1
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.nuke.plugin_nuke__15_0v4 import PluginNuke_15_0


class Plugins(enum.Enum):
    BLENDER_4_1_1 = PluginBlender_4_1_1()
    NUKE_15_0 = PluginNuke_15_0()
