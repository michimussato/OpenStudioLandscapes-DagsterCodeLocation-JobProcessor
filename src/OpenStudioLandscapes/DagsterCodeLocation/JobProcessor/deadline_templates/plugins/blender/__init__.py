import enum
from typing import List

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.plugin_base import PluginBase

# plugin["submitter"]["render_engines"] = ["CYCLES", "BLENDER_EEVEE", "WORKBENCH"]
#
# plugin["submitter"]["args"].append("--background")
# plugin["submitter"]["args"].append('<QUOTE>"{job_file}"<QUOTE>')
# plugin["submitter"]["args"].extend(["--render-output", '<QUOTE>"{render_output}"<QUOTE>'])
# plugin["submitter"]["args"].extend(["--render-format", "{output_format}"])
# plugin["submitter"]["args"].extend(["--engine", "{render_engine}"])
# plugin["submitter"]["args"].extend(["--frame-start", "<STARTFRAME>"])
# plugin["submitter"]["args"].extend(["--frame-end", "<ENDFRAME>"])
# plugin["submitter"]["args"].extend(["--threads", "0"])
# plugin["submitter"]["args"].append("--render-anim")


class RenderEngine(enum.StrEnum):
    CYCLES = "CYCLES"
    BLENDER_EEVEE = "BLENDER_EEVEE"
    WORKBENCH = "WORKBENCH"


class PluginBlenderBase(PluginBase):
    args: List = [
        "--background",
        '<QUOTE>"{job_file}"<QUOTE>',
        "--render-output", '<QUOTE>"{render_output}"<QUOTE>',
        "--render-format", "{output_format}",
        "--engine", "{render_engine}",
        "--frame-start", "<STARTFRAME>",
        "--frame-end", "<ENDFRAME>",
        "--threads", "0",
        "--render-anim",
    ]
