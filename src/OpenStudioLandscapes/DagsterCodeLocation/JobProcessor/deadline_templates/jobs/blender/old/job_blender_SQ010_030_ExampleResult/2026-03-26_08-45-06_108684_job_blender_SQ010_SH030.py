import pathlib

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.jobs.job_base import job, InitialStatuses
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.blender.plugin_blender__4_1_1 import plugin

# Production:
# - Test Production (3ede4117-b73c-4bd3-83a2-40d66bc954c5)
# Task:
# - SQ010_SH030 Rendering (b0cfdac7-afa9-4382-a75d-3c80a388e136)

job["job_file"] = pathlib.Path(TEST_FIXTURES / "blender" / "sh030_001.blend").as_posix()
job["plugin_dict"] = plugin
job["deadline_initial_status"] = str(InitialStatuses.ACTIVE)
job["kitsu_task"] = "b0cfdac7-afa9-4382-a75d-3c80a388e136"  # SQ010 / SQ010_SH030  Rendering  https://kitsu.pangolin.openstudiolandscapes.cloud-ip.cc/productions/3ede4117-b73c-4bd3-83a2-40d66bc954c5/shots/tasks/b0cfdac7-afa9-4382-a75d-3c80a388e136
job["append_draft_job_png"] = True
job["append_draft_job_mov"] = True
job["with_kitsu_publish"] = True
job["deadline_job_with_draft"] = True
job["render_engine"] = "CYCLES"
job["comment"] = "This is a new Bender job comment"
job["frame_start"] = 1201
job["frame_end"] = 1210

# Paste this file in
# ${OPENSTUDIOLANDSCAPES__DAGSTER_JOBS_IN} (/data/share/in)
#
# After processing file
# - https://dagster-mb.pangolin.openstudiolandscapes.cloud-ip.cc/locations/OpenStudioLandscapes-Dagster-JobProcessor%20Package%20Code%20Location/sensors/ingestion_sensor
# Run command locally:
# (because deadlinecommand is not available in OpenStudioLandscapes-Dagster image)
#
# /opt/Thinkbox/Deadline10/bin/deadlinecommand -SubmitMultipleJobsV2 -jsonfilepath "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/008/4_1197-1254_4/submission.json"


"""
daemon was not added to the CommandLineParser.
daemon was not added to the CommandLineParser.
Auto Configuration: Picking configuration based on: lenovo / 192.168.178.195
Auto Configuration: No auto configuration could be detected, using local configuration
Local python API (Python 3): Updating
'/home/michael/Thinkbox/Deadline10/pythonAPIs/Qo2NwgwS4V5oVK3SmUn4lA==' already exists. Skipping extraction of PythonSync.
Local python API (Python 3): Update complete
PythonSync Fallback (Python 3): Attempting to decompress pythonsync3 from /home/michael/Thinkbox/Deadline10/cache/MaMVfbEFgksOse8v0NtVegq0wI/pythonsync3/pythonsync3.zip to /opt/Thinkbox/Deadline10/bin/pythonsync3
PythonSync Fallback (Python 3):pythonsync3 decompression successful
Local python API (Python 2): Updating
'/home/michael/Thinkbox/Deadline10/pythonAPIs/hsK64f8mMWnxnvxrwXmhQQ==' already exists. Skipping extraction of PythonSync.
Local python API (Python 2): Update complete
PythonSync Fallback (Python 2): Attempting to decompress pythonsync from /home/michael/Thinkbox/Deadline10/cache/MaMVfbEFgksOse8v0NtVegq0wI/pythonsync/pythonsync.zip to /opt/Thinkbox/Deadline10/bin/pythonsync
PythonSync Fallback (Python 2):pythonsync decompression successful
Launcher Thread - Launcher thread initializing...
Launcher Thread - opening remote TCP listening port 17000
Launcher Thread - creating local listening TCP socket on an available port...
Launcher Thread - local TCP port bound to: [::1]:45927
Launcher Thread -  updating local listening port in launcher file: 45927
Launcher Thread - Launcher thread listening on port 17000
upgraded was not added to the CommandLineParser.
upgradefailed was not added to the CommandLineParser.
service was not added to the CommandLineParser.
daemon was not added to the CommandLineParser.
Launching Monitor
Time to initialize: 39.000 ms
Launcher Thread - Remote Administration is now enabled
Launcher Thread - Automatic Updates is now disabled
Auto Configuration: No auto configuration for Repository Path could be detected, using local configuration
Connecting to Deadline RCS 10.2 [v10.2.1.1 Release (094cbe890)]
'/home/michael/Thinkbox/Deadline10/pythonAPIs/Qo2NwgwS4V5oVK3SmUn4lA==' already exists. Skipping extraction of PythonSync.
'/home/michael/Thinkbox/Deadline10/pythonAPIs/Qo2NwgwS4V5oVK3SmUn4lA==' already exists. Skipping extraction of PythonSync.
Auto Configuration: Picking configuration based on: lenovo / 192.168.178.195
Auto Configuration: No auto configuration could be detected, using local configuration
Time to connect to Repository: 883.000 ms
Time to check user account: 11.000 ms
Time to purge old logs and temp files: 3.000 ms
Time to synchronize plugin icons: 343.000 ms
QRegularExpressionPrivate::doMatch(): called on an invalid QRegularExpression object
QRegularExpressionPrivate::doMatch(): called on an invalid QRegularExpression object
Time to initialize main window: 405.000 ms
Main Window shown
Python 3.7.16 | packaged by Thinkbox Software | (default, Mar  2 2023, 21:05:48) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
Time to show main window: 24.000 ms
Error occurred while updating Worker cache: Connection Server error: Access to the path '/us/Thinkbox/Deadline10' is denied. (System.UnauthorizedAccessException)
   at System.IO.FileSystem.CreateDirectory(String fullPath)
   at System.IO.Directory.CreateDirectory(String path)
   at Deadline.Configuration.DeadlineConfig.i(String dfu)
   at Deadline.Configuration.DeadlineConfig.CheckConfigFile(Boolean allUsers)
   at Deadline.Configuration.DeadlineConfig.GetIniFileSetting(String key, String defaultValue, Boolean errorOnNoConfig)
   at Deadline.Configuration.DeadlineConfig.GetConnectionType()
   at Deadline.StorageDB.Proxy.Utils.RequestModels.RequestDataFactory.Create(String baseUri, Int32 port, String rootEndpoint, String endPoint, String method, String certificate, Dictionary`2 queryString, Dictionary`2 headers, Object dataObject, String resource)
   at Deadline.StorageDB.Proxy.ProxySlaveStorage.GetModifiedSlaveInfoSettings(SlaveInfoSettings[]& modifiedSlaveInfoSettings, String[]& deletedSlaveIds, Boolean& hasMore, Nullable`1 lastSettingsAutoUpdate, Nullable`1 lastInfoUpdate, Nullable`1 lastDeletionAutoUpdate)
---------- Inner Stack Trace (System.IO.IOException) ----------
 (FranticX.Database.DatabaseConnectionException)
'/home/michael/Thinkbox/Deadline10/pythonAPIs/Qo2NwgwS4V5oVK3SmUn4lA==' already exists. Skipping extraction of PythonSync.
An unhandled exception occurred: Object reference not set to an instance of an object. (System.NullReferenceException)
   at Deadline.Jobs.JobProperties.Equals(Object obj)
   at Deadline.Jobs.Job.Equals(Object jobObject)
   at Python.Runtime.ClassBase.tp_richcompare(IntPtr ob, IntPtr other, Int32 op)
Unhandled exception. System.NullReferenceException: Object reference not set to an instance of an object.
   at Deadline.Jobs.JobProperties.Equals(Object obj)
   at Deadline.Jobs.Job.Equals(Object jobObject)
   at Python.Runtime.ClassBase.tp_richcompare(IntPtr ob, IntPtr other, Int32 op)
"""

"""
See /data/share/deadline-repository/DeadlineRepository10/events/DraftEventPlugin/DraftQuickSubmission/QuickDraft.py
-> add DEADLINE_PATH=/opt/Thinkbox/Deadline10/bin
"""


"""
﻿=======================================================
Error
=======================================================
Error: Renderer returned non-zero error code, 1. Check the log for more information.
   at Deadline.Plugins.PluginWrapper.RenderTasks(Task task, String& outMessage, AbortLevel& abortLevel)

=======================================================
Type
=======================================================
RenderPluginException

=======================================================
Stack Trace
=======================================================
   at Deadline.Plugins.SandboxedPlugin.d(DeadlineMessage bgt, CancellationToken bgu)
   at Deadline.Plugins.SandboxedPlugin.RenderTask(Task task, CancellationToken cancellationToken)
   at Deadline.Slaves.SlaveRenderThread.c(TaskLogWriter ajy, CancellationToken ajz)

=======================================================
Log
=======================================================
2026-03-24 10:50:02:  0: Loading Job's Plugin timeout is Disabled
2026-03-24 10:50:02:  0: SandboxedPlugin: Render Job As User disabled, running as current user 'root'
2026-03-24 10:50:07:  0: Executing plugin command of type 'Initialize Plugin'
2026-03-24 10:50:07:  0: INFO: Executing plugin script '/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/plugins/69c26bc5502b0a4897c95cf3/DraftPlugin.py'
2026-03-24 10:50:08:  0: INFO: Plugin execution sandbox using Python version 3
2026-03-24 10:50:08:  0: INFO: Found Draft python module at: '/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/Draft/Draft.so'
2026-03-24 10:50:08:  0: INFO: Setting Process Environment Variable PYTHONPATH to /var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/Draft:/opt/Thinkbox/Deadline10/bin/pythonsync3:/opt/Thinkbox/Deadline10/bin/python3:/opt/Thinkbox/Deadline10/bin/python3/lib:/opt/Thinkbox/Deadline10/bin/python3/lib/site-packages:/opt/Thinkbox/Deadline10/lib/python3/lib/python37.zip:/opt/Thinkbox/Deadline10/lib/python3/lib/python3.7:/opt/Thinkbox/Deadline10/lib/python3/lib/python3.7/lib-dynload:/opt/Thinkbox/Deadline10/lib/python3/lib/python3.7/site-packages:/opt/Thinkbox/Deadline10/bin/
2026-03-24 10:50:08:  0: INFO: Setting Process Environment Variable MAGICK_CONFIGURE_PATH to /var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/Draft
2026-03-24 10:50:08:  0: INFO: Setting Process Environment Variable LD_LIBRARY_PATH to /opt/Thinkbox/Deadline10/bin/python/lib:/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/Draft
2026-03-24 10:50:08:  0: INFO: About: Draft Plugin for Deadline
2026-03-24 10:50:08:  0: INFO: The job's environment will be merged with the current environment before rendering
2026-03-24 10:50:08:  0: Done executing plugin command of type 'Initialize Plugin'
2026-03-24 10:50:08:  0: Start Job timeout is disabled.
2026-03-24 10:50:08:  0: Task timeout is disabled.
2026-03-24 10:50:08:  0: Loaded job: Test Production - SH030 - 4_1197-1214_4 - Rendering - sh030_001.blend - 028 - blender (Draft PNG) (69c26bc5502b0a4897c95cf3)
2026-03-24 10:50:08:  0: Executing plugin command of type 'Start Job'
2026-03-24 10:50:08:  0: DEBUG: S3BackedCache Client is not installed.
2026-03-24 10:50:08:  0: INFO: Executing global asset transfer preload script '/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/plugins/69c26bc5502b0a4897c95cf3/GlobalAssetTransferPreLoad.py'
2026-03-24 10:50:08:  0: INFO: Looking for legacy (pre-10.0.26) AWS Portal File Transfer...
2026-03-24 10:50:08:  0: INFO: Looking for legacy (pre-10.0.26) File Transfer controller in /opt/Thinkbox/S3BackedCache/bin/task.py...
2026-03-24 10:50:08:  0: INFO: Could not find legacy (pre-10.0.26) AWS Portal File Transfer.
2026-03-24 10:50:08:  0: INFO: Legacy (pre-10.0.26) AWS Portal File Transfer is not installed on the system.
2026-03-24 10:50:08:  0: Done executing plugin command of type 'Start Job'
2026-03-24 10:50:08:  0: Plugin rendering frame(s): 1197-1214
2026-03-24 10:50:08:  0: Executing plugin command of type 'Render Task'
2026-03-24 10:50:08:  0: INFO: Draft job starting...
2026-03-24 10:50:08:  0: INFO: Stdout Redirection Enabled: True
2026-03-24 10:50:08:  0: INFO: Asynchronous Stdout Enabled: False
2026-03-24 10:50:08:  0: INFO: Stdout Handling Enabled: True
2026-03-24 10:50:08:  0: INFO: Popup Handling Enabled: False
2026-03-24 10:50:08:  0: INFO: Using Process Tree: True
2026-03-24 10:50:08:  0: INFO: Hiding DOS Window: True
2026-03-24 10:50:08:  0: INFO: Creating New Console: False
2026-03-24 10:50:08:  0: INFO: Running as user: root
2026-03-24 10:50:08:  0: INFO: Looking for bundled python at: '/opt/Thinkbox/Deadline10/bin/python3/python'
2026-03-24 10:50:08:  0: INFO: Executable: "/opt/Thinkbox/Deadline10/bin/python3/python"
2026-03-24 10:50:08:  0: INFO: Argument: -u "/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/events/DraftEventPlugin/DraftQuickSubmission/QuickDraft.py" resolution="0.5" codec="png" colorSpaceIn="Identity" colorSpaceOut="Identity" annotationsFilePath="/root/Thinkbox/Deadline10/temp/draft_annotations_info_6872549415.txt" annotationsImageString="None" annotationsResWidthString="480.0" annotationsResHeightString="270.0" annotationsFramePaddingSize="4" quality="85" quickType="createImages" isDistributed="False" frameList=1197-1214 startFrame=1197 endFrame=1214 taskStartFrame=1197 taskEndFrame=1214 outFolder="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/png" outFile="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/png/sh030_001.####.png" inFile="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/sh030_001.####.exr" deadlineRepository="deadline-rcs-runner-10-2.openstudiolandscapes.lan:8888/fs/folder/load/folder?subDirectory=" taskStartFrame=1197 taskEndFrame=1214 
2026-03-24 10:50:08:  0: INFO: Full Command: "/opt/Thinkbox/Deadline10/bin/python3/python" -u "/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/events/DraftEventPlugin/DraftQuickSubmission/QuickDraft.py" resolution="0.5" codec="png" colorSpaceIn="Identity" colorSpaceOut="Identity" annotationsFilePath="/root/Thinkbox/Deadline10/temp/draft_annotations_info_6872549415.txt" annotationsImageString="None" annotationsResWidthString="480.0" annotationsResHeightString="270.0" annotationsFramePaddingSize="4" quality="85" quickType="createImages" isDistributed="False" frameList=1197-1214 startFrame=1197 endFrame=1214 taskStartFrame=1197 taskEndFrame=1214 outFolder="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/png" outFile="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/png/sh030_001.####.png" inFile="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/sh030_001.####.exr" deadlineRepository="deadline-rcs-runner-10-2.openstudiolandscapes.lan:8888/fs/folder/load/folder?subDirectory=" taskStartFrame=1197 taskEndFrame=1214 
2026-03-24 10:50:08:  0: INFO: Startup Directory: "/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/Draft"
2026-03-24 10:50:08:  0: INFO: Process Priority: BelowNormal
2026-03-24 10:50:08:  0: INFO: Process Affinity: default
2026-03-24 10:50:08:  0: INFO: Process is now running
2026-03-24 10:50:11:  0: STDOUT: Appending "/root/Thinkbox/Deadline10/cache/qtIjhsu6Gbzz97g1wb8H3ySSDI/events/DraftEventPlugin/DraftQuickSubmission" to system path to import Quick Draft scripts
2026-03-24 10:50:11:  0: STDOUT: Command line args:
2026-03-24 10:50:11:  0: STDOUT: resolution=0.5
2026-03-24 10:50:11:  0: STDOUT: codec=png
2026-03-24 10:50:11:  0: STDOUT: colorSpaceIn=Identity
2026-03-24 10:50:11:  0: STDOUT: colorSpaceOut=Identity
2026-03-24 10:50:11:  0: STDOUT: annotationsFilePath=/root/Thinkbox/Deadline10/temp/draft_annotations_info_6872549415.txt
2026-03-24 10:50:11:  0: STDOUT: annotationsImageString=None
2026-03-24 10:50:11:  0: STDOUT: annotationsResWidthString=480.0
2026-03-24 10:50:11:  0: STDOUT: annotationsResHeightString=270.0
2026-03-24 10:50:11:  0: STDOUT: annotationsFramePaddingSize=4
2026-03-24 10:50:11:  0: STDOUT: quality=85
2026-03-24 10:50:11:  0: STDOUT: quickType=createImages
2026-03-24 10:50:11:  0: STDOUT: isDistributed=False
2026-03-24 10:50:11:  0: STDOUT: frameList=1197-1214
2026-03-24 10:50:11:  0: STDOUT: startFrame=1197
2026-03-24 10:50:11:  0: STDOUT: endFrame=1214
2026-03-24 10:50:11:  0: STDOUT: taskStartFrame=1197
2026-03-24 10:50:11:  0: STDOUT: taskEndFrame=1214
2026-03-24 10:50:11:  0: STDOUT: outFolder=/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/png
2026-03-24 10:50:11:  0: STDOUT: outFile=/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/png/sh030_001.####.png
2026-03-24 10:50:11:  0: STDOUT: inFile=/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/sh030_001.####.exr
2026-03-24 10:50:11:  0: STDOUT: deadlineRepository=deadline-rcs-runner-10-2.openstudiolandscapes.lan:8888/fs/folder/load/folder?subDirectory=
2026-03-24 10:50:11:  0: STDOUT: taskStartFrame=1197
2026-03-24 10:50:11:  0: STDOUT: taskEndFrame=1214
2026-03-24 10:50:11:  0: STDOUT: Draft 1.8.0.4
2026-03-24 10:50:11:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:11:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:12:  0: STDOUT: Progress: 5%
2026-03-24 10:50:12:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:12:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:12:  0: STDOUT: Progress: 11%
2026-03-24 10:50:12:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:12:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:12:  0: STDOUT: Progress: 16%
2026-03-24 10:50:13:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:13:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:13:  0: STDOUT: Progress: 22%
2026-03-24 10:50:13:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:13:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:13:  0: STDOUT: Progress: 27%
2026-03-24 10:50:13:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:13:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:13:  0: STDOUT: Progress: 33%
2026-03-24 10:50:13:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:13:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:14:  0: STDOUT: Progress: 38%
2026-03-24 10:50:14:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:14:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:14:  0: STDOUT: Progress: 44%
2026-03-24 10:50:14:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:14:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:14:  0: STDOUT: Progress: 50%
2026-03-24 10:50:14:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:14:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:15:  0: STDOUT: Progress: 55%
2026-03-24 10:50:15:  0: STDOUT: magick_output_file() Warning: invalid compression 'png' for format png. Using 'default' instead.
2026-03-24 10:50:15:  0: STDOUT: magick_output_file() Warning: quality can not be set for format png.
2026-03-24 10:50:15:  0: STDOUT: Progress: 61%
2026-03-24 10:50:15:  0: STDOUT: Traceback (most recent call last):
2026-03-24 10:50:15:  0: STDOUT:   File "/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/events/DraftEventPlugin/DraftQuickSubmission/QuickDraft.py", line 101, in <module>
2026-03-24 10:50:15:  0: STDOUT:     CreateImages(params)
2026-03-24 10:50:15:  0: STDOUT:   File "/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/events/DraftEventPlugin/DraftQuickSubmission/DraftCreateImages.py", line 88, in CreateImages
2026-03-24 10:50:15:  0: STDOUT:     frame = Draft.Image.ReadFromFile( currInFile )
2026-03-24 10:50:15:  0: STDOUT: RuntimeError: exr_input_file Error: failed to open exr file /data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/sh030_001.1208.exr
2026-03-24 10:50:15:  0: INFO: Process exit code: 1
2026-03-24 10:50:15:  0: Done executing plugin command of type 'Render Task'

=======================================================
Details
=======================================================
Date: 03/24/2026 10:50:19
Frames: 1197-1214
Elapsed Time: 00:00:00:18
Job Submit Date: 03/24/2026 10:47:33
Job User: michael
Average RAM Usage: 1222120192 (8%)
Peak RAM Usage: 1261391872 (8%)
Average CPU Usage: 41%
Peak CPU Usage: 63%
Used CPU Clocks (x10^6 cycles): 13139
Total CPU Clocks (x10^6 cycles): 32045

=======================================================
Worker Information
=======================================================
Worker Name: minion04-deadline-10-2-worker
Version: v10.2.1.1 Release (094cbe890)
Operating System: Linux
Machine User: root
IP Address: 192.168.178.19
MAC Address: 9A:DD:6E:38:6D:16
CPU Architecture: x86_64
CPUs: 4
CPU Usage: 34%
Memory Usage: 1.1 GB / 15.5 GB (7%)
Free Disk Space: 8.626 GB 
Video Card: 
"""

"""
﻿=======================================================
Error
=======================================================
Error: Renderer returned non-zero error code, 1. Check the log for more information.
   at Deadline.Plugins.PluginWrapper.RenderTasks(Task task, String& outMessage, AbortLevel& abortLevel)

=======================================================
Type
=======================================================
RenderPluginException

=======================================================
Stack Trace
=======================================================
   at Deadline.Plugins.SandboxedPlugin.d(DeadlineMessage bgt, CancellationToken bgu)
   at Deadline.Plugins.SandboxedPlugin.RenderTask(Task task, CancellationToken cancellationToken)
   at Deadline.Slaves.SlaveRenderThread.c(TaskLogWriter ajy, CancellationToken ajz)

=======================================================
Log
=======================================================
2026-03-24 10:49:43:  0: Loading Job's Plugin timeout is Disabled
2026-03-24 10:49:43:  0: SandboxedPlugin: Render Job As User disabled, running as current user 'root'
2026-03-24 10:49:48:  0: Executing plugin command of type 'Initialize Plugin'
2026-03-24 10:49:48:  0: INFO: Executing plugin script '/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/plugins/69c26bc5502b0a4897c95cf4/DraftPlugin.py'
2026-03-24 10:49:48:  0: INFO: Plugin execution sandbox using Python version 3
2026-03-24 10:49:49:  0: INFO: Found Draft python module at: '/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/Draft/Draft.so'
2026-03-24 10:49:49:  0: INFO: Setting Process Environment Variable PYTHONPATH to /var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/Draft:/opt/Thinkbox/Deadline10/bin/pythonsync3:/opt/Thinkbox/Deadline10/bin/python3:/opt/Thinkbox/Deadline10/bin/python3/lib:/opt/Thinkbox/Deadline10/bin/python3/lib/site-packages:/opt/Thinkbox/Deadline10/lib/python3/lib/python37.zip:/opt/Thinkbox/Deadline10/lib/python3/lib/python3.7:/opt/Thinkbox/Deadline10/lib/python3/lib/python3.7/lib-dynload:/opt/Thinkbox/Deadline10/lib/python3/lib/python3.7/site-packages:/opt/Thinkbox/Deadline10/bin/
2026-03-24 10:49:49:  0: INFO: Setting Process Environment Variable MAGICK_CONFIGURE_PATH to /var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/Draft
2026-03-24 10:49:49:  0: INFO: Setting Process Environment Variable LD_LIBRARY_PATH to /opt/Thinkbox/Deadline10/bin/python/lib:/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/Draft
2026-03-24 10:49:49:  0: INFO: About: Draft Plugin for Deadline
2026-03-24 10:49:49:  0: INFO: The job's environment will be merged with the current environment before rendering
2026-03-24 10:49:49:  0: Done executing plugin command of type 'Initialize Plugin'
2026-03-24 10:49:49:  0: Start Job timeout is disabled.
2026-03-24 10:49:49:  0: Task timeout is disabled.
2026-03-24 10:49:49:  0: Loaded job: Test Production - SH030 - 4_1197-1214_4 - Rendering - sh030_001.blend - 028 - blender (Draft MOV) (69c26bc5502b0a4897c95cf4)
2026-03-24 10:49:49:  0: Executing plugin command of type 'Start Job'
2026-03-24 10:49:49:  0: DEBUG: S3BackedCache Client is not installed.
2026-03-24 10:49:49:  0: INFO: Executing global asset transfer preload script '/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/plugins/69c26bc5502b0a4897c95cf4/GlobalAssetTransferPreLoad.py'
2026-03-24 10:49:49:  0: INFO: Looking for legacy (pre-10.0.26) AWS Portal File Transfer...
2026-03-24 10:49:49:  0: INFO: Looking for legacy (pre-10.0.26) File Transfer controller in /opt/Thinkbox/S3BackedCache/bin/task.py...
2026-03-24 10:49:49:  0: INFO: Could not find legacy (pre-10.0.26) AWS Portal File Transfer.
2026-03-24 10:49:49:  0: INFO: Legacy (pre-10.0.26) AWS Portal File Transfer is not installed on the system.
2026-03-24 10:49:49:  0: Done executing plugin command of type 'Start Job'
2026-03-24 10:49:49:  0: Plugin rendering frame(s): 1197-1214
2026-03-24 10:49:49:  0: Executing plugin command of type 'Render Task'
2026-03-24 10:49:49:  0: INFO: Draft job starting...
2026-03-24 10:49:49:  0: INFO: Stdout Redirection Enabled: True
2026-03-24 10:49:49:  0: INFO: Asynchronous Stdout Enabled: False
2026-03-24 10:49:49:  0: INFO: Stdout Handling Enabled: True
2026-03-24 10:49:49:  0: INFO: Popup Handling Enabled: False
2026-03-24 10:49:49:  0: INFO: Using Process Tree: True
2026-03-24 10:49:49:  0: INFO: Hiding DOS Window: True
2026-03-24 10:49:49:  0: INFO: Creating New Console: False
2026-03-24 10:49:49:  0: INFO: Running as user: root
2026-03-24 10:49:49:  0: INFO: Looking for bundled python at: '/opt/Thinkbox/Deadline10/bin/python3/python'
2026-03-24 10:49:49:  0: INFO: Executable: "/opt/Thinkbox/Deadline10/bin/python3/python"
2026-03-24 10:49:49:  0: INFO: Argument: -u "/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/events/DraftEventPlugin/DraftQuickSubmission/QuickDraft.py" resolution="0.5" codec="h264" colorSpaceIn="Identity" colorSpaceOut="Identity" annotationsFilePath="/root/Thinkbox/Deadline10/temp/draft_annotations_info_1558715518.txt" annotationsImageString="None" annotationsResWidthString="480.0" annotationsResHeightString="270.0" annotationsFramePaddingSize="4" quality="85" quickType="createMovie" isDistributed="False" frameList=1197-1214 startFrame=1197 endFrame=1214 taskStartFrame==1197 taskEndFrame==1214 frameRate=25 outFolder="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/mov" outFile="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/mov/sh030_001.mov" inFile="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/sh030_001.####.exr" deadlineRepository="deadline-rcs-runner-10-2.openstudiolandscapes.lan:8888/fs/folder/load/folder?subDirectory=" taskStartFrame=1197 taskEndFrame=1214 
2026-03-24 10:49:49:  0: INFO: Full Command: "/opt/Thinkbox/Deadline10/bin/python3/python" -u "/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/events/DraftEventPlugin/DraftQuickSubmission/QuickDraft.py" resolution="0.5" codec="h264" colorSpaceIn="Identity" colorSpaceOut="Identity" annotationsFilePath="/root/Thinkbox/Deadline10/temp/draft_annotations_info_1558715518.txt" annotationsImageString="None" annotationsResWidthString="480.0" annotationsResHeightString="270.0" annotationsFramePaddingSize="4" quality="85" quickType="createMovie" isDistributed="False" frameList=1197-1214 startFrame=1197 endFrame=1214 taskStartFrame==1197 taskEndFrame==1214 frameRate=25 outFolder="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/mov" outFile="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/mov/sh030_001.mov" inFile="/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/sh030_001.####.exr" deadlineRepository="deadline-rcs-runner-10-2.openstudiolandscapes.lan:8888/fs/folder/load/folder?subDirectory=" taskStartFrame=1197 taskEndFrame=1214 
2026-03-24 10:49:49:  0: INFO: Startup Directory: "/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/Draft"
2026-03-24 10:49:49:  0: INFO: Process Priority: BelowNormal
2026-03-24 10:49:49:  0: INFO: Process Affinity: default
2026-03-24 10:49:49:  0: INFO: Process is now running
2026-03-24 10:49:52:  0: STDOUT: Appending "/root/Thinkbox/Deadline10/cache/qtIjhsu6Gbzz97g1wb8H3ySSDI/events/DraftEventPlugin/DraftQuickSubmission" to system path to import Quick Draft scripts
2026-03-24 10:49:52:  0: STDOUT: Command line args:
2026-03-24 10:49:52:  0: STDOUT: resolution=0.5
2026-03-24 10:49:52:  0: STDOUT: codec=h264
2026-03-24 10:49:52:  0: STDOUT: colorSpaceIn=Identity
2026-03-24 10:49:52:  0: STDOUT: colorSpaceOut=Identity
2026-03-24 10:49:52:  0: STDOUT: annotationsFilePath=/root/Thinkbox/Deadline10/temp/draft_annotations_info_1558715518.txt
2026-03-24 10:49:52:  0: STDOUT: annotationsImageString=None
2026-03-24 10:49:52:  0: STDOUT: annotationsResWidthString=480.0
2026-03-24 10:49:52:  0: STDOUT: annotationsResHeightString=270.0
2026-03-24 10:49:52:  0: STDOUT: annotationsFramePaddingSize=4
2026-03-24 10:49:52:  0: STDOUT: quality=85
2026-03-24 10:49:52:  0: STDOUT: quickType=createMovie
2026-03-24 10:49:52:  0: STDOUT: isDistributed=False
2026-03-24 10:49:52:  0: STDOUT: frameList=1197-1214
2026-03-24 10:49:52:  0: STDOUT: startFrame=1197
2026-03-24 10:49:52:  0: STDOUT: endFrame=1214
2026-03-24 10:49:52:  0: STDOUT: taskStartFrame==1197
2026-03-24 10:49:52:  0: STDOUT: taskEndFrame==1214
2026-03-24 10:49:52:  0: STDOUT: frameRate=25
2026-03-24 10:49:52:  0: STDOUT: outFolder=/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/mov
2026-03-24 10:49:52:  0: STDOUT: outFile=/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/mov/sh030_001.mov
2026-03-24 10:49:52:  0: STDOUT: inFile=/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/sh030_001.####.exr
2026-03-24 10:49:52:  0: STDOUT: deadlineRepository=deadline-rcs-runner-10-2.openstudiolandscapes.lan:8888/fs/folder/load/folder?subDirectory=
2026-03-24 10:49:52:  0: STDOUT: taskStartFrame=1197
2026-03-24 10:49:52:  0: STDOUT: taskEndFrame=1214
2026-03-24 10:49:52:  0: STDOUT: Draft 1.8.0.4
2026-03-24 10:49:52:  0: STDOUT: [libopenh264 @ 0x38c5e3c0] Slice count will be set automatically
2026-03-24 10:49:52:  0: STDOUT: [libopenh264 @ 0x38c5e3c0] [OpenH264] this = 0x0x38ada7d0, Warning:SliceArgumentValidationFixedSliceMode(), unsupported setting with Resolution and uiSliceNum combination under RC on! So uiSliceNum is changed to 8!
2026-03-24 10:49:52:  0: STDOUT: [libopenh264 @ 0x38c5e3c0] [OpenH264] this = 0x0x38ada7d0, Warning:bEnableFrameSkip = 0,bitrate can't be controlled for RC_QUALITY_MODE,RC_BITRATE_MODE and RC_TIMESTAMP_MODE without enabling skip frame.
2026-03-24 10:49:52:  0: STDOUT: Output #0, mov, to '/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/draft/mov/sh030_001.mov':
2026-03-24 10:49:52:  0: STDOUT:   Metadata:
2026-03-24 10:49:52:  0: STDOUT:     encoder         : Lavf59.16.100
2026-03-24 10:49:52:  0: STDOUT:   Stream #0:0: Video: h264 (High) (avc1 / 0x31637661), yuv420p(pc, bt709), 480x270, q=2-31, 25 fps, 12800 tbn
2026-03-24 10:49:52:  0: STDOUT: Encoding Progress: 5%
2026-03-24 10:49:52:  0: STDOUT: Encoding Progress: 11%
2026-03-24 10:49:53:  0: STDOUT: Encoding Progress: 16%
2026-03-24 10:49:53:  0: STDOUT: Encoding Progress: 22%
2026-03-24 10:49:53:  0: STDOUT: Encoding Progress: 27%
2026-03-24 10:49:53:  0: STDOUT: Encoding Progress: 33%
2026-03-24 10:49:53:  0: STDOUT: Encoding Progress: 38%
2026-03-24 10:49:53:  0: STDOUT: Encoding Progress: 44%
2026-03-24 10:49:53:  0: STDOUT: Encoding Progress: 50%
2026-03-24 10:49:53:  0: STDOUT: Encoding Progress: 55%
2026-03-24 10:49:53:  0: STDOUT: Encoding Progress: 61%
2026-03-24 10:49:53:  0: STDOUT: Traceback (most recent call last):
2026-03-24 10:49:53:  0: STDOUT:   File "/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/events/DraftEventPlugin/DraftQuickSubmission/QuickDraft.py", line 104, in <module>
2026-03-24 10:49:53:  0: STDOUT:     CreateMovie(params)
2026-03-24 10:49:53:  0: STDOUT:   File "/data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/events/DraftEventPlugin/DraftQuickSubmission/DraftCreateMovie.py", line 87, in CreateMovie
2026-03-24 10:49:53:  0: STDOUT:     frame = Draft.Image.ReadFromFile( currInFile )
2026-03-24 10:49:53:  0: STDOUT: RuntimeError: exr_input_file Error: failed to open exr file /data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/028/4_1197-1214_4/sh030_001.1208.exr
2026-03-24 10:49:54:  0: INFO: Process exit code: 1
2026-03-24 10:49:54:  0: Done executing plugin command of type 'Render Task'

=======================================================
Details
=======================================================
Date: 03/24/2026 10:49:58
Frames: 1197-1214
Elapsed Time: 00:00:00:16
Job Submit Date: 03/24/2026 10:47:33
Job User: michael
Average RAM Usage: 1229308288 (8%)
Peak RAM Usage: 1259024384 (8%)
Average CPU Usage: 32%
Peak CPU Usage: 52%
Used CPU Clocks (x10^6 cycles): 7795
Total CPU Clocks (x10^6 cycles): 24357

=======================================================
Worker Information
=======================================================
Worker Name: minion04-deadline-10-2-worker
Version: v10.2.1.1 Release (094cbe890)
Operating System: Linux
Machine User: root
IP Address: 192.168.178.19
MAC Address: 9A:DD:6E:38:6D:16
CPU Architecture: x86_64
CPUs: 4
CPU Usage: 27%
Memory Usage: 1.1 GB / 15.5 GB (7%)
Free Disk Space: 8.626 GB 
Video Card: 
"""