from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.jobs.job_base import job
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender.plugin_blender__4_1_1 import plugin

job["job_file"] = PROJECTS_ROOT / "tests" / "blender" / "2023-11-13_EskofBubble" / "ColoredBubble_013.blend"
job["plugin_dict"] = plugin
job["kitsu_task"] = ""
job["append_draft_job_png"] = True
job["append_draft_job_mov"] = True
job["with_kitsu_publish"] = True
job["deadline_job_with_draft"] = True
job["render_engine"] = "CYCLES"
job["comment"] = "SQ010_SH030"
job["frame_start"] = 1001
job["frame_end"] = 1300
