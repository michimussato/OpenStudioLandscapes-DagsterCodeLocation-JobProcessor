from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.plugin_base import plugin


plugin["submitter"]["render_engines"] = ["CYCLES", "BLENDER_EEVEE", "WORKBENCH"]

plugin["submitter"]["args"].append("--background")
plugin["submitter"]["args"].append('<QUOTE>"{job_file}"<QUOTE>')
plugin["submitter"]["args"].extend(["--render-output", '<QUOTE>"{render_output}"<QUOTE>'])
plugin["submitter"]["args"].extend(["--render-format", "{output_format}"])
plugin["submitter"]["args"].extend(["--engine", "{render_engine}"])
plugin["submitter"]["args"].extend(["--frame-start", "<STARTFRAME>"])
plugin["submitter"]["args"].extend(["--frame-end", "<ENDFRAME>"])
plugin["submitter"]["args"].extend(["--threads", "0"])
plugin["submitter"]["args"].append("--render-anim")
