import os
import pathlib
from dagster import (
    DefaultSensorStatus,
)

from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *


"""
ExperimentalWarning: Class `AndAssetCondition` is experimental. It may break in future versions, even between dot releases. To mute warnings for experimental functionality, invoke warnings.filterwarnings("ignore", category=dagster.ExperimentalWarning) or use one of the other methods described at https://docs.python.org/3/library/warnings.html#describing-warning-filters.
"""


SENSORS_STATUS = DefaultSensorStatus.RUNNING
JSON_INDENT = 2
PADDING = 4
SUBMISSION_JSON = "submission.json"
OUTPUT_ROOT = AWSPORTAL_ROOT_1 / "out"
INPUT_ROOT = pathlib.Path(os.environ.get("OPENSTUDIOLANDSCAPES__DAGSTER_JOBS_IN", "/data/share/in"))
INPUT_ROOT_PROCESSED = pathlib.Path(os.environ.get("OPENSTUDIOLANDSCAPES__DAGSTER_JOBS_IN", "/data/share/in")).joinpath(".processing")

# Todo
#  - [ ] Disable as long as no certificates are involved
DEADLINE_ERRORS = [
    # Connecting to the correct repository?
    "'\nConfiguration Error: Failed to establish connection to michimussato-fuji.nord:4433 due to a communication error.\n'"
    # Changed repo but need to go and enter the passphrase again manually
    "'Error: Error encountered when loading the configured Client Certificate (/nfs/deadline/Deadline10/certs/certs/Deadline10RemoteClient.pfx). It is likely either an invalid x.509 certificate, or the wrong passphrase was provided.\n\nFull Error:\nThe certificate data cannot be read with the provided password, the password may be incorrect.\n'",
]
DEADLINE_SUCCESSES = [
    "'result: System.Collections.Generic.List`1[System.String]\n'",
]
