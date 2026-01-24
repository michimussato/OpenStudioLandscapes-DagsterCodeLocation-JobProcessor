import pathlib
from dagster import (
    DefaultSensorStatus,
    EnvVar,
)


"""
ExperimentalWarning: Class `AndAssetCondition` is experimental. It may break in future versions, even between dot releases. To mute warnings for experimental functionality, invoke warnings.filterwarnings("ignore", category=dagster.ExperimentalWarning) or use one of the other methods described at https://docs.python.org/3/library/warnings.html#describing-warning-filters.
"""


SENSORS_STATUS = DefaultSensorStatus.RUNNING
JSON_INDENT = 2
PADDING = 4
SUBMISSION_JSON = "submission.json"
OUTPUT_ROOT = pathlib.Path("/nfs/AWSPortalRoot1/out")
INPUT_ROOT = pathlib.Path(EnvVar("DAGSTER_JOBS_IN").get_value())  # pathlib.Path(os.getenv("DAGSTER_JOBS_IN", "/nfs/in"))
INPUT_ROOT_PROCESSED = pathlib.Path(EnvVar("DAGSTER_JOBS_IN").get_value(), ".processing")  # pathlib.Path(os.getenv("DAGSTER_JOBS_IN", "/nfs/in/")) / ".processing"

DEADLINE_ERRORS = [
    # Connecting to the correct repository?
    "'\nConfiguration Error: Failed to establish connection to michimussato-fuji.nord:4433 due to a communication error.\n'"
    # Changed repo but need to go and enter the passphrase again manually
    "'Error: Error encountered when loading the configured Client Certificate (/nfs/deadline/Deadline10/certs/certs/Deadline10RemoteClient.pfx). It is likely either an invalid x.509 certificate, or the wrong passphrase was provided.\n\nFull Error:\nThe certificate data cannot be read with the provided password, the password may be incorrect.\n'",
]
DEADLINE_SUCCESSES = [
    "'result: System.Collections.Generic.List`1[System.String]\n'",
]
