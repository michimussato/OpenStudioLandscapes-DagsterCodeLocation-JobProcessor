__all__ = [
    "REZ_PACKAGES",
    "DEADLINE_PLUGINS",
    "AWSPORTAL_ROOT_1",
    "TEST_FIXTURES",
    "PROJECTS_ROOT",
]

import pathlib

REZ_PACKAGES: pathlib.Path = pathlib.Path("/data/share/rez-packages/packages")
DEADLINE_PLUGINS: pathlib.Path = pathlib.Path("/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/plugins")
AWSPORTAL_ROOT_1: pathlib.Path = pathlib.Path("/data/share/AWSPortalRoot1")
TEST_FIXTURES: pathlib.Path = AWSPORTAL_ROOT_1 / "fixtures"
PROJECTS_ROOT: pathlib.Path = pathlib.Path("/data/share/projects")
