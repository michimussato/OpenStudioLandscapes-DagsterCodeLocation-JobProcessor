# import os
# import pathlib

from dagster import (
    asset,
    Output,
    AssetMaterialization,
    MetadataValue,
    AssetsDefinition,
)

from OpenStudioLandscapes.Dagster.JobProcessor.dagster_job_processor import settings


GROUP_NAME = "CONSTANTS_ASSET_FACTORY"


assets = [
    # # Template:
    # {
    #     "name": ,
    #     "value": ,
    #     "type": MetadataValue.,
    # },
    {
        "name": "OUTPUT_ROOT",
        "value": settings.OUTPUT_ROOT,
        "type": MetadataValue.path,
    },
    {
        "name": "INPUT_ROOT",
        "value": settings.INPUT_ROOT,
        "type": MetadataValue.path,
    },
    # {
    #     # TODO
    #     "name": "INPUT_ROOT_PROCESSING",
    #     "value": settings.INPUT_ROOT_PROCESSED,
    #     "type": MetadataValue.path,
    # },
    {
        "name": "INPUT_ROOT_PROCESSED",
        "value": settings.INPUT_ROOT_PROCESSED,
        "type": MetadataValue.path,
    },
    {
        "name": "PADDING",
        "value": settings.PADDING,
        "type": MetadataValue.int,
    },
    {
        "name": "JSON_INDENT",
        "value": settings.JSON_INDENT,
        "type": MetadataValue.int,
    },
    {
        "name": "FRAME_JUMPS",
        "value": [10, 5, 2, 1],
        "type": MetadataValue.json,
    },
    {
        "name": "OUTPUT_FORMAT_DEFAULT",
        "value": "exr",
        "type": MetadataValue.text,
    },
    {
        "name": "RESOLUTION_DRAFT_SCALE",
        "value": 0.5,
        "type": MetadataValue.float,
    },
    {
        "name": "DEFAULT_HANDLES",
        "value": 4,
        "type": MetadataValue.int,
    },
    {
        "name": "DEFAULT_FRAME_START",
        "value": 1001,
        "type": MetadataValue.int,
    },
    {
        "name": "DONT_ALLOW_NEGATIVE_FRAMES",
        "value": False,
        "type": MetadataValue.bool,
    },
    {
        "name": "DEFAULT_RESOLUTION",
        "value": (1920, 1080),
        "type": MetadataValue.json,
    },
    {
        "name": "DEFAULT_FPS",
        "value": 24.0,
        "type": MetadataValue.float,
    },
    {
        "name": "SUBMISSION_JSON",
        "value": settings.SUBMISSION_JSON,
        "type": MetadataValue.text,
    },
    {
        # Todo
        #  text -> pathlib.Path
        "name": "GAZU_PY",
        "value": "/opt/gazu/gazuenv/bin/python3.9",
        "type": MetadataValue.text,
    },
    {
        "name": "JOB_DICT_TEMPLATE",
        "value": {
            "JobInfoFilePath": "",
            "PluginInfoFilePath": "",
            "JobDependencies": None,
            "AuxiliaryFiles": []
        },
        "type": MetadataValue.json,
    },
]


def asset_factory(spec) -> AssetsDefinition:

    @asset(
        group_name=GROUP_NAME,
        name=spec["name"],
    )
    def _asset() -> dict:

        yield Output(spec["value"])

        yield AssetMaterialization(
            asset_key=spec["name"],
            metadata={
                spec["name"]: spec["type"](spec["value"]),
            }
        )

    return _asset


assets = [asset_factory(spec) for spec in assets]
