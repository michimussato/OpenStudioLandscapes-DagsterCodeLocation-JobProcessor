from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import DEADLINE_PLUGINS
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.plugin_base import plugin

plugin["submitter"]["padding_command"] = "'\\$F' + str(EVAL_PADDING)"  # results in "$F4"
plugin["submitter"]["args"].append(DEADLINE_PLUGINS / "Houdini" / "hrender_dl.py")
plugin["submitter"]["args"].append("-e")
plugin["submitter"]["args"].extend(["-f", "<STARTFRAME> <ENDFRAME> {chunk_size}"])
plugin["submitter"]["args"].extend(["-d", "{rop}"])
plugin["submitter"]["args"].extend(["-o", "<QUOTE>{render_output}<QUOTE>"])
plugin["submitter"]["args"].append("<QUOTE>{job_file}<QUOTE>")
