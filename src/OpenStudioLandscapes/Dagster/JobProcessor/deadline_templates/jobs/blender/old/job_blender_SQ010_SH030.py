# import pathlib
#
# from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins import *
# from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.jobs.job_base import job, InitialStatuses
# from OpenStudioLandscapes.Dagster.JobProcessor.deadline_templates.plugins.blender.plugin_blender__4_1_1 import plugin
#
# # Production:
# # - Test Production (3ede4117-b73c-4bd3-83a2-40d66bc954c5)
# # Task:
# # - SQ010_SH030 Rendering (b0cfdac7-afa9-4382-a75d-3c80a388e136)
#
# job["job_file"] = pathlib.Path(TEST_FIXTURES / "blender" / "sh030_001.blend").as_posix()
# job["plugin_dict"] = plugin
# job["deadline_initial_status"] = str(InitialStatuses.ACTIVE)
# job["kitsu_task"] = "b0cfdac7-afa9-4382-a75d-3c80a388e136"  # SQ010 / SQ010_SH030  Rendering  https://kitsu.pangolin.openstudiolandscapes.cloud-ip.cc/productions/3ede4117-b73c-4bd3-83a2-40d66bc954c5/shots/tasks/b0cfdac7-afa9-4382-a75d-3c80a388e136
# job["append_draft_job_png"] = True
# job["append_draft_job_mov"] = True
# job["with_kitsu_publish"] = True
# job["deadline_job_with_draft"] = True
# job["render_engine"] = "CYCLES"
# job["comment"] = "This is a new Bender job comment"
# job["frame_start"] = 1201
# job["frame_end"] = 1250
#
# # Paste this file in
# # ${OPENSTUDIOLANDSCAPES__DAGSTER_JOBS_IN} (/data/share/in)
# #
# # After processing file
# # - https://dagster-mb.pangolin.openstudiolandscapes.cloud-ip.cc/locations/OpenStudioLandscapes-Dagster-JobProcessor%20Package%20Code%20Location/sensors/ingestion_sensor
# # Run command locally:
# # (because deadlinecommand is not available in OpenStudioLandscapes-Dagster image)
# #
# # /opt/Thinkbox/Deadline10/bin/deadlinecommand -SubmitMultipleJobsV2 -jsonfilepath "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/008/4_1197-1254_4/submission.json"
#
#
# """
# daemon was not added to the CommandLineParser.
# daemon was not added to the CommandLineParser.
# Auto Configuration: Picking configuration based on: lenovo / 192.168.178.195
# Auto Configuration: No auto configuration could be detected, using local configuration
# Local python API (Python 3): Updating
# '/home/michael/Thinkbox/Deadline10/pythonAPIs/Qo2NwgwS4V5oVK3SmUn4lA==' already exists. Skipping extraction of PythonSync.
# Local python API (Python 3): Update complete
# PythonSync Fallback (Python 3): Attempting to decompress pythonsync3 from /home/michael/Thinkbox/Deadline10/cache/MaMVfbEFgksOse8v0NtVegq0wI/pythonsync3/pythonsync3.zip to /opt/Thinkbox/Deadline10/bin/pythonsync3
# PythonSync Fallback (Python 3):pythonsync3 decompression successful
# Local python API (Python 2): Updating
# '/home/michael/Thinkbox/Deadline10/pythonAPIs/hsK64f8mMWnxnvxrwXmhQQ==' already exists. Skipping extraction of PythonSync.
# Local python API (Python 2): Update complete
# PythonSync Fallback (Python 2): Attempting to decompress pythonsync from /home/michael/Thinkbox/Deadline10/cache/MaMVfbEFgksOse8v0NtVegq0wI/pythonsync/pythonsync.zip to /opt/Thinkbox/Deadline10/bin/pythonsync
# PythonSync Fallback (Python 2):pythonsync decompression successful
# Launcher Thread - Launcher thread initializing...
# Launcher Thread - opening remote TCP listening port 17000
# Launcher Thread - creating local listening TCP socket on an available port...
# Launcher Thread - local TCP port bound to: [::1]:45927
# Launcher Thread -  updating local listening port in launcher file: 45927
# Launcher Thread - Launcher thread listening on port 17000
# upgraded was not added to the CommandLineParser.
# upgradefailed was not added to the CommandLineParser.
# service was not added to the CommandLineParser.
# daemon was not added to the CommandLineParser.
# Launching Monitor
# Time to initialize: 39.000 ms
# Launcher Thread - Remote Administration is now enabled
# Launcher Thread - Automatic Updates is now disabled
# Auto Configuration: No auto configuration for Repository Path could be detected, using local configuration
# Connecting to Deadline RCS 10.2 [v10.2.1.1 Release (094cbe890)]
# '/home/michael/Thinkbox/Deadline10/pythonAPIs/Qo2NwgwS4V5oVK3SmUn4lA==' already exists. Skipping extraction of PythonSync.
# '/home/michael/Thinkbox/Deadline10/pythonAPIs/Qo2NwgwS4V5oVK3SmUn4lA==' already exists. Skipping extraction of PythonSync.
# Auto Configuration: Picking configuration based on: lenovo / 192.168.178.195
# Auto Configuration: No auto configuration could be detected, using local configuration
# Time to connect to Repository: 883.000 ms
# Time to check user account: 11.000 ms
# Time to purge old logs and temp files: 3.000 ms
# Time to synchronize plugin icons: 343.000 ms
# QRegularExpressionPrivate::doMatch(): called on an invalid QRegularExpression object
# QRegularExpressionPrivate::doMatch(): called on an invalid QRegularExpression object
# Time to initialize main window: 405.000 ms
# Main Window shown
# Python 3.7.16 | packaged by Thinkbox Software | (default, Mar  2 2023, 21:05:48)
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Time to show main window: 24.000 ms
# Error occurred while updating Worker cache: Connection Server error: Access to the path '/us/Thinkbox/Deadline10' is denied. (System.UnauthorizedAccessException)
#    at System.IO.FileSystem.CreateDirectory(String fullPath)
#    at System.IO.Directory.CreateDirectory(String path)
#    at Deadline.Configuration.DeadlineConfig.i(String dfu)
#    at Deadline.Configuration.DeadlineConfig.CheckConfigFile(Boolean allUsers)
#    at Deadline.Configuration.DeadlineConfig.GetIniFileSetting(String key, String defaultValue, Boolean errorOnNoConfig)
#    at Deadline.Configuration.DeadlineConfig.GetConnectionType()
#    at Deadline.StorageDB.Proxy.Utils.RequestModels.RequestDataFactory.Create(String baseUri, Int32 port, String rootEndpoint, String endPoint, String method, String certificate, Dictionary`2 queryString, Dictionary`2 headers, Object dataObject, String resource)
#    at Deadline.StorageDB.Proxy.ProxySlaveStorage.GetModifiedSlaveInfoSettings(SlaveInfoSettings[]& modifiedSlaveInfoSettings, String[]& deletedSlaveIds, Boolean& hasMore, Nullable`1 lastSettingsAutoUpdate, Nullable`1 lastInfoUpdate, Nullable`1 lastDeletionAutoUpdate)
# ---------- Inner Stack Trace (System.IO.IOException) ----------
#  (FranticX.Database.DatabaseConnectionException)
# '/home/michael/Thinkbox/Deadline10/pythonAPIs/Qo2NwgwS4V5oVK3SmUn4lA==' already exists. Skipping extraction of PythonSync.
# An unhandled exception occurred: Object reference not set to an instance of an object. (System.NullReferenceException)
#    at Deadline.Jobs.JobProperties.Equals(Object obj)
#    at Deadline.Jobs.Job.Equals(Object jobObject)
#    at Python.Runtime.ClassBase.tp_richcompare(IntPtr ob, IntPtr other, Int32 op)
# Unhandled exception. System.NullReferenceException: Object reference not set to an instance of an object.
#    at Deadline.Jobs.JobProperties.Equals(Object obj)
#    at Deadline.Jobs.Job.Equals(Object jobObject)
#    at Python.Runtime.ClassBase.tp_richcompare(IntPtr ob, IntPtr other, Int32 op)
# """
#
# """
# See /data/share/deadline-repository/DeadlineRepository10/events/DraftEventPlugin/DraftQuickSubmission/QuickDraft.py
# -> add DEADLINE_PATH=/opt/Thinkbox/Deadline10/bin
# """
