import getpass
import pathlib
import socket
import textwrap
from typing import List, NamedTuple

from pydantic import BaseModel, Field, field_validator
import enum


class InitialStatuses(enum.StrEnum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"


class CleanupMode(enum.Enum):
    ArchiveJobs = "ArchiveJobs"
    DeleteJobs = "DeleteJobs"


class OnJobCompleteAction(enum.Enum):
    Nothing = "Nothing"
    Delete = "Delete"
    Archive = "Archive"


class EnvironmentKeyValue(NamedTuple):
    key: str
    value: str


class Cleanup(BaseModel):
    """
    References:
    - [Cleanup](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#cleanup)
    """
    DeleteOnComplete: bool = Field(
        default=False,
        description="DeleteOnComplete=<true/false> : Specifies whether or not the job should be automatically deleted after it completes (default = false).",
    )
    ArchiveOnComplete: bool = Field(
        default=False,
        description="ArchiveOnComplete=<true/false> : Specifies whether or not the job should be automatically archived after it completes (default = false).",
    )
    OverrideAutoJobCleanup: bool = Field(
        default=False,
        description="OverrideAutoJobCleanup=<true/false> : If true, the job will ignore the global Job Cleanup settings and instead use its own (default = false).",
    )
    OverrideJobCleanup: bool = Field(
        default=False,
        description="OverrideJobCleanup=<true/false> : If OverrideAutoJobCleanup is true, this will determine if the job should be automatically cleaned up or not.",
    )
    JobCleanupDays: int = Field(
        default=7,
        description="JobCleanupDays=<true/false> : If OverrideAutoJobCleanup and OverrideJobCleanup are both true, this is the number of days to keep the job before cleaning it up.",
    )
    OverrideJobCleanupType: CleanupMode = Field(
        default=CleanupMode.ArchiveJobs.value,
        description="OverrideJobCleanupType=<ArchiveJobs/DeleteJobs> : If OverrideAutoJobCleanup and OverrideJobCleanup are both true, this is the job cleanup mode.",
    )


class DeadlinePlugins(enum.StrEnum):
    CommandLine = "CommandLine"


class CommandLinePluginInfo(BaseModel):
    """
    As we are using the CommandLine plugin
    **exclusively**, only this reference
    is relevant:
    - [Arbitrary Command Line Jobs](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#arbitrary-command-line-jobs)
    ```
    """
    Executable: pathlib.Path = Field(
        description="The executable we wish to use.",
    )
    Arguments: str = Field(
        description=textwrap.dedent(
            """
            The arguments we wish to pass to the executable. In the arguments string, there are a few key words that will be replaced with the appropriate text when rendering the job:
            - <STARTFRAME> will be replaced with the current start frame for each task.
            - <ENDFRAME> will be replaced by the current end frame for each task.
            - <STARTFRAME%#> will be replaced with the current start frame for each task, and will be padded with 0’s to match the length specified for #. For example, <STARTFRAME%4> will ensure a start frame padding of 4.
            - <ENDFRAME%#> will be replaced by the current end frame for each task, and will be padded with 0’s to match the length specified for #. For example, <ENDFRAME%6> will ensure an end frame padding of 6.
            - <QUOTE> will be replaced with an actual quote character (“).
            - <AUXFILE#> will be replaced by the auxiliary file # submitted with the job. For example, <AUXFILE0> will add the file path to the first auxiliary file submitted with the job to the arguments string.
            """
        )
    )


class JobInfo(BaseModel):
    """
    References:
    - [Job Info File Options](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#job-info-file-options)
    """
    Plugin: DeadlinePlugins = Field(
        default=DeadlinePlugins.CommandLine.value,
        description="Plugin=<plugin name> : Specifies the plugin to use. Must match an existing plugin in the repository.",
    )
    Frames: str = Field(
        default="0",
        description="Frames=<1,2,3-10,20> : Specifies the frame range of the render job. See the [Frame List Formatting Options](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/job-submitting.html#frame-list-ref-label) in the Job Submission documentation for more information (default = 0).",
    )
    Name: str = Field(
        default="Untitled",
        description="Name=<job name> : Specifies the name of the job (default = Untitled).",
    )
    Comment: str = Field(
        default_factory=str,
        description="Comment=<comment> : Specifies a comment for the job (default = blank).",
    )
    Department: str = Field(
        default_factory=str,
        description="Department=<department name> : Specifies the department that the job belongs to. This is simply a way to group jobs together, and does not affect rendering in any way (default = blank).",
    )
    BatchName: str = Field(
        default_factory=str,
        description="BatchName=<batch name> : Specifies an optional name to logically group jobs together (default = blank).",
    )
    UserName: str = Field(
        # default_factory=getpass.getuser,
        description="UserName=<username> : Specifies the job’s user (default = current user).",
    )
    MachineName: str = Field(
        # default_factory=socket.gethostname,
        description="MachineName=<machineName> : Specifies the machine the job was submitted from (default = current machine).",
    )
    Pool: str = Field(
        default=None,
        description="Pool=<poolName> : Specifies the pool that the job is being submitted to (default = none).",
    )
    SecondaryPool: str = Field(
        default=None,
        description="SecondaryPool=<poolName> : Specifies the secondary pool that the job can spread to if machines are available. If not specified, the job will not use a secondary pool.",
    )
    Group: str = Field(
        default=None,
        description="Group=<groupName> : Specifies the group that the job is being submitted to (default = none).",
    )
    Priority: int = Field(
        default=50,
        description="Priority=<0 or greater> : Specifies the priority of a job with 0 being the lowest (default = 50). The maximum priority can be configured in the Job Settings of the Repository Options, and defaults to 100.",
    )
    ChunkSize: int = Field(
        default=1,
        description="ChunkSize=<1 or greater> : Specifies how many frames to render per task (default = 1).",
    )
    ConcurrentTasks: int = Field(
        default=1,
        description="ConcurrentTasks=<1-16> : Specifies the maximum number of tasks that a Worker can render at a time (default = 1). This is useful for script plugins that support multithreading.",
    )
    LimitConcurrentTasksToNumberOfCpus: bool = Field(
        default=True,
        description="LimitConcurrentTasksToNumberOfCpus=<true/false> : If ConcurrentTasks is greater than 1, setting this to true will ensure that a Worker will not dequeue more tasks than it has processors (default = true).",
    )
    OnJobComplete: OnJobCompleteAction = Field(
        default=OnJobCompleteAction.Nothing.value,
        description="OnJobComplete=<Nothing/Delete/Archive> : Specifies what should happen to a job after it completes (default = Nothing).",
    )
    SynchronizeAllAuxiliaryFiles: bool = Field(
        default=False,
        description="SynchronizeAllAuxiliaryFiles=<true/false> : If enabled, all job files (as opposed to just the job info and plugin info files) will be synchronized by the Worker between tasks for this job (default = false). Note that this can add significant network overhead, and should only be used if you plan on manually editing any of the files that are being submitted with the job.",
    )
    ForceReloadPlugin: bool = Field(
        default=False,
        description="ForceReloadPlugin=<true/false> : Specifies whether or not to reload the plugin between subsequent frames of a job (default = false). This deals with memory leaks or applications that do not unload all job aspects properly.",
    )
    Sequential: bool = Field(
        default=False,
        description="Sequential=<true/false> : Sequential rendering forces a Worker to render the tasks of a job in order. If an earlier task is ever requeued, the Worker won’t go back to that task until it has finished the remaining tasks in order. Sequential rendering also forces the Worker to finish rendering tasks in order before switching to another job, even if that job has higher priority or this job is interruptible (default = false).",
    )
    SuppressEvents: bool = Field(
        default=False,
        description="SuppressEvents=<true/false> : If true, the job will not trigger any event plugins while in the queue (default = false).",
    )
    Protected: bool = Field(
        default=False,
        description="Protected=<true/false> : If enabled, the job can only be deleted by the job’s user, a super user, or a user that belongs to a user group that has permissions to handle protected jobs. Other users will not be able to delete the job, and the job will also not be cleaned up by Deadline’s automatic house cleaning.",
    )
    InitialStatus: InitialStatuses = Field(
        default=InitialStatuses.ACTIVE.value,
        description="InitialStatus=<Active/Suspended> : Specifies what status the job should be in immediately after submission (default = Active).",
    )
    # NetworkRoot: pathlib.Path = Field(
    #     default="current default repository for the machine from which submission is occurring",
    #     description="NetworkRoot=<repositoryUNCPath> : Specifies the repository that the job will be submitted to. This is required if you are using more than one repository (default = current default repository for the machine from which submission is occurring).",
    # )

    # Dependencies
    JobDependencies: List[str] = Field(
        default_factory=list,
        description="JobDependencies=<jobID,jobID,jobID> : Specifies what jobs must finish before this job will resume (default = blank). These dependency jobs must be identified using their unique job ID, which is outputted after the job is submitted, and can be found in the Monitor in the “Job ID” column.",
    )
    JobDependencyPercentage: int = Field(
        default=-1,
        description="JobDependencyPercentage=<-1, or 0 to 100> : If between 0 and 100, this job will resume when all of its job dependencies have completed the specified percentage number of tasks. If -1, this feature will be disabled (default = -1)."
    )
    IsFrameDependent: bool = Field(
        default=False,
        description="IsFrameDependent=<true/false> : Specifies whether or not the job is frame dependent (default = false)."
    )
    FrameDependencyOffsetStart: int = Field(
        default=0,
        description="FrameDependencyOffsetStart=<-100000 to 100000> : If the job is frame dependent, this is the start frame offset (default = 0)."
    )
    FrameDependencyOffsetEnd: int = Field(
        default=0,
        description="FrameDependencyOffsetEnd=<-100000 to 100000> : If the job is frame dependent, this is the end frame offset (default = 0)."
    )
    ResumeOnCompleteDependencies: bool = Field(
        default=True,
        description="ResumeOnCompleteDependencies=<true/false> : Specifies whether or not the dependent job should resume when its dependencies are complete (default = true)."
    )
    ResumeOnDeletedDependencies: bool = Field(
        default=False,
        description="ResumeOnDeletedDependencies=<true/false> : Specifies whether or not the dependent job should resume when its dependencies have been deleted (default = false)."
    )
    ResumeOnFailedDependencies: bool = Field(
        default=False,
        description="ResumeOnFailedDependencies=<true/false> : Specifies whether or not the dependent job should resume when its dependencies have failed (default = false)."
    )
    RequiredAssets: List[pathlib.Path] = Field(
        default_factory=str,
        description="RequiredAssets=<assetPath,assetPath,assetPath> : Specifies what asset files must exist before this job will resume (default = blank). These asset paths must be identified using full paths, and multiple paths can be separated with commas. If using frame dependencies, you can replace padding in a sequence with the ‘#’ characters, and a task for the job will only be resumed when the required assets for the task’s frame exist."
    )
    ScriptDependencies: List[pathlib.Path] = Field(
        default_factory=str,
        description="ScriptDependencies=<scriptPath,scriptPath,scriptPath> : Specifies what Python script files will be executed to determine if a job can resume (default = blank). These script paths must be identified using full paths, and multiple paths can be separated with commas. See the [dependency scripting section](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/job-scripts.html#job-dependency-scripts-ref-label) of the documentation for more information."
    )

    @field_validator("JobDependencies")
    @classmethod
    def stringify_job_dependencies(cls, v: List[str]) -> str:
        return str(",".join(v))

    @field_validator("RequiredAssets", "ScriptDependencies")
    @classmethod
    def stringify_list_of_paths(cls, v: List[pathlib.Path]) -> str:
        return str(",".join([v.as_posix() for v in v]))
    # Dependencies: JobDependencies = Field(
    #     default=JobDependencies(),
    #     description="",
    # )
    # :  = Field(
    #     default=,
    #     description="",
    # )

    # Todo
    #  - [ ] [Timeouts](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#timeouts)
    #  - [ ] [Interruptible](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#interruptible)
    #  - [ ] [Notifications](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#notifications)
    #  - [ ] [Machine Limit](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#machine-limit)
    #  - [ ] [Limits](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#limits)
    #  - [ ] [Failure Detection](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#failure-detection)
    #  - [ ] [Cleanup](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#cleanup)
    #  - [ ] [Scheduling](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#scheduling)
    #  - [ ] [Scripts](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#scripts)
    #  - [ ] [Event Opt-Ins](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#event-opt-ins)
    #  - [ ] [Environment](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#environment)
    #  - [ ] [Job Extra Info](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#job-extra-info)
    #  - [ ] [Task Extra Info Names](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#task-extra-info-names)
    #  - [ ] [Output](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#output)
    #        [x] Used
    #  - [ ] [Tile Job](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#tile-job)
    #  - [ ] [Maintenance Job](https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#maintenance-job)
    #  - [ ] []()



    # Frames: str
    # InitialStatus: InitialStatuses = InitialStatuses.ACTIVE.value
    # BatchName: str
    # Name: str
    # Priority: int
    # ChunkSize: int
    # StartupDirectory: pathlib.Path
    # Comment: str = ""
    # ForceReloadPlugin: bool = True
    # OutputDirectory0: pathlib.Path
    # OutputFilename0: str



# class Props(BaseModel):
#     Name: str = ""
#     Batch: str = ""
#     User: str = ""
#     Region: str = ""
#     Cmmt: str = ""
#     Dept: str = ""
#     Frames: str = ""
#     Chunk: int = 1000000
#     Tasks: int = 1
#     Grp: str = "none"
#     Pool: str = "none"
#     SecPool: str = None
#     Pri: int = 0
#     ReqAss: List = []
#     ScrDep: List = []
#     Conc: int = 1
#     ConcLimt: bool = True
#     AuxSync: bool = False
#     Int: bool = False
#     IntPer: int = 100
#     RemTmT: int = 0
#     Seq: int = False
#     Reload: bool = True
#     NoEvnt: bool = False
#     OnComp: int = 2
#     Protect: bool = False
#     PathMap: List = []
#     AutoTime: bool = False
#     TimeScrpt: bool = False
#     MinTime: int = 0
#     MaxTime: int = 0
#     Timeout: int = 1
#     FrameTimeout: bool = False
#     StartTime: int = 0
#     InitializePluginTime: int = 0
#     Dep: List[Dep] = []
#     DepFrame: bool = False
#     DepFrameStart: int = 0
#     DepFrameEnd: int = 0
#     DepComp: bool = True
#     DepDel: bool = False
#     DepFail: bool = False
#     DepPer: int = -1.0
#     NoBad: bool = False
#     OverAutoClean: bool = False
#     OverClean: bool = False
#     OverCleanDays: int = 0
#     OverCleanType: int = 1
#     JobFailOvr: bool = False
#     JobFailErr: int = 0
#     TskFailOvr: bool = False
#     TskFailErr: int = 0
#     SndWarn: bool = True
#     NotOvr: bool = False
#     SndEmail: bool = False
#     SndPopup: bool = False
#     NotEmail: List = []
#     NotUser: List = []
#     [...]