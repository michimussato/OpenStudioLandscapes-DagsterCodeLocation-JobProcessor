from typing import List

from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import DEADLINE_PLUGINS
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.plugin_base import PluginBase


class PluginHoudiniBase(PluginBase):
    padding_command: str = "'\\$F' + str(EVAL_PADDING)"  # results in "$F4"
    args: List = [
        DEADLINE_PLUGINS / "Houdini" / "hrender_dl.py",
        "-e",
        "-f", "<STARTFRAME> <ENDFRAME> {chunk_size}",
        "-d", "{rop}",
        "-o", "<QUOTE>{render_output}<QUOTE>",
        "<QUOTE>{job_file}<QUOTE>",
    ]