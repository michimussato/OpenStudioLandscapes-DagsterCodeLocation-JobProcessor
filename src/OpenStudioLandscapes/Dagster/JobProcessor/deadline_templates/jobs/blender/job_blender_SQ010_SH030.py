from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.jobs.blender.job_blender import job
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender.plugin_blender__4_1_1 import plugin

# Production:
# - Test Production (3ede4117-b73c-4bd3-83a2-40d66bc954c5)
# Task:
# - SQ010_SH030 Rendering (b0cfdac7-afa9-4382-a75d-3c80a388e136)

job["job_file"] = TEST_FIXTURES / "blender" / "sh030_001.blend"
job["plugin_dict"] = plugin
job["kitsu_task"] = "b0cfdac7-afa9-4382-a75d-3c80a388e136"  # SQ010 / SQ010_SH030  Rendering  https://kitsu.pangolin.openstudiolandscapes.cloud-ip.cc/productions/3ede4117-b73c-4bd3-83a2-40d66bc954c5/shots/tasks/b0cfdac7-afa9-4382-a75d-3c80a388e136
job["append_draft_job_png"] = True
job["append_draft_job_mov"] = True
job["with_kitsu_publish"] = True
job["deadline_job_with_draft"] = True
job["render_engine"] = "CYCLES"
job["comment"] = "This is Bender job comment"
job["frame_start"] = 1201
job["frame_end"] = 1250
