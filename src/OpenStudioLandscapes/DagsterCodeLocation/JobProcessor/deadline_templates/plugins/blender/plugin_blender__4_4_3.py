import pathlib
import textwrap
from typing import Literal

from pydantic import Field

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.blender import (
    PluginBlenderBase,
    RenderEngine,
)


class PluginBlender_4_4_3(PluginBlenderBase):
    plugin_type: Literal['PluginBlender_4_4_3']

    executable: pathlib.Path = REZ_PACKAGES / "blender" / "4.4.3" / "blender"

    render_engine: RenderEngine = Field(
        default=RenderEngine.WORKBENCH.value,
        examples=[i.value for i in RenderEngine],
    )

    farm_command: str = textwrap.dedent(
        """
        ```shell
        /data/share/rez-packages/packages/blender/4.4.3/blender \
            --enable-autoexec \
            --background /data/share/AWSPortalRoot1/fixtures/blender/sh010_001.blend \
            --threads 0 \
            --render-format PNG \
            --engine CYCLES \
            --render-output /data/share/out/test/sh010_001.CYCLES.####.png \
            --frame-start 1051 \
            --frame-end 1055 \
            --render-anim \
            -- \
            --cycles-print-stats
        ```
        """
    )

    help_command: str = textwrap.dedent(
        """
        ```shell
        /data/share/rez-packages/packages/blender/4.4.3/blender --help
        ```
        """
    )
