__all__ = [
    "REZ_PACKAGES",
    "DEADLINE_PLUGINS",
    "TEST_FIXTURES",
    "PROJECTS_ROOT",
]

import pathlib

REZ_PACKAGES: pathlib.Path = pathlib.Path("/data/share/rez-packages/packages")
DEADLINE_PLUGINS: pathlib.Path = pathlib.Path("/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/plugins")
TEST_FIXTURES: pathlib.Path = pathlib.Path("/data/share/AWSPortalRoot1/fixtures")
PROJECTS_ROOT: pathlib.Path = pathlib.Path("/data/share/projects")
