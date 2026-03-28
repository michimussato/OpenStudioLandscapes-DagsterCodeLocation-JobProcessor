from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.jobs.job_base import job
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender.plugin_blender_base import plugin

job["job_file"] = PROJECTS_ROOT / "Sandbox" / "2022-12-14_ConnectPoints" / "Connect_Points_004.blend"
job["plugin_dict"] = plugin
job["kitsu_task"] = ""
job["append_draft_job_png"] = True
job["append_draft_job_mov"] = True
job["with_kitsu_publish"] = True
job["deadline_job_with_draft"] = True
job["render_engine"] = "CYCLES"
job["comment"] = "SQ010_SH010"
job["frame_start"] = 1001
job["frame_end"] = 1200
