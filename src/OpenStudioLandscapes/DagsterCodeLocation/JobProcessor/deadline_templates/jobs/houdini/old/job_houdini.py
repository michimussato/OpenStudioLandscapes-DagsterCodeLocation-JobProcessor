from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.jobs.job_base import job
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.houdini.plugin_houdini_base import plugin

job["job_file"] = TEST_FIXTURES / "houdini" / "project" / "vivi_025.hip"
job["plugin_dict"] = plugin
job["kitsu_task"] = "9890944f-fe39-4408-baf3-bcd34dc9807d"  # SQ010 / SQ010_SH020  Layout  http://miniboss/productions/6c5dfed4-0f11-48f7-aba2-4d4d5cce85fc/shots/tasks/9890944f-fe39-4408-baf3-bcd34dc9807d
job["append_draft_job_png"] = True
job["append_draft_job_mov"] = True
job["with_kitsu_publish"] = True
job["deadline_job_with_draft"] = True
job["comment"] = "This is Houdini job comment"
job["frame_start"] = 1001
job["frame_end"] = 1020
job["rop"] = "/stage/usdrender_rop_camera2"
