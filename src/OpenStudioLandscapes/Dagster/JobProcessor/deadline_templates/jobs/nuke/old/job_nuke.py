from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.jobs.nuke.old.job_template_nuke import job
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.nuke.plugin_nuke__15_0v4 import plugin

job["job_file"] = TEST_FIXTURES / "nuke" / "fixture_v001.nk"
job["plugin_dict"] = plugin
job["kitsu_task"] = "9bb09bfa-0a97-40c6-a6e6-27405b198570"  # SQ010 / SQ010_SH030  Layout  http://miniboss/productions/6c5dfed4-0f11-48f7-aba2-4d4d5cce85fc/shots/tasks/9bb09bfa-0a97-40c6-a6e6-27405b198570
job["append_draft_job_png"] = True
job["append_draft_job_mov"] = True
job["with_kitsu_publish"] = True
job["deadline_job_with_draft"] = True
job["comment"] = "This is Nuke job comment"
job["frame_start"] = 1051
job["frame_end"] = 1100
