from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.jobs.job_base import job
from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.nuke.plugin_nuke_base import plugin


# Overrides
job["chunk_size"] = 10
job["plugin_dict"] = plugin

# Plugin specific k/v
job["write_nodes"] = ["write_farm"]
