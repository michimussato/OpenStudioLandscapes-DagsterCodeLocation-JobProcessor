__all__ = [
    "REZ_PACKAGES",
    "DEADLINE_PLUGINS",
    "AWSPORTAL_ROOT_1",
    "TEST_FIXTURES",
    "PROJECTS_ROOT",
]

import enum
import pathlib

REZ_PACKAGES: pathlib.Path = pathlib.Path("/data/share/rez-packages/packages")
DEADLINE_PLUGINS: pathlib.Path = pathlib.Path("/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/plugins")
AWSPORTAL_ROOT_1: pathlib.Path = pathlib.Path("/data/share/AWSPortalRoot1")
TEST_FIXTURES: pathlib.Path = AWSPORTAL_ROOT_1 / "fixtures"
PROJECTS_ROOT: pathlib.Path = pathlib.Path("/data/share/projects")


from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender.plugin_blender__4_1_1 import PluginBlender_4_1_1
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.nuke.plugin_nuke__15_0v4 import PluginNuke_15_0


class Plugins(enum.Enum):
    BLENDER_4_1_1 = PluginBlender_4_1_1
    NUKE_15_0 = PluginNuke_15_0
