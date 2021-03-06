#!/usr/bin/env python3
# workflow-helpers
# Copyright(C) 2020 Francesco Murdaca
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This script run in a workflow task to select Thoth integration workflow to run."""

import json
import os
import logging

from thoth.workflow_helpers.trigger_finished_webhook import trigger_finished_webhook
from thoth.workflow_helpers.configuration import Configuration

from thoth.common import ThothAdviserIntegrationEnum

_LOGGER = logging.getLogger("thoth.select_thoth_integration")


def trigger_integration_workflow() -> None:
    """Trigger specific workflow depending on Thoth integration type."""
    metadata = json.loads(Configuration._THOTH_ADVISER_METADATA)

    if not metadata:
        _LOGGER.warning("No adviser metadata provided. No actions performed.")
        return

    source_type = metadata["source_type"]

    with open("/mnt/workdir/source_type", "w") as f:
        f.write(source_type)
        f.close()

    if source_type == ThothAdviserIntegrationEnum.KEBECHET.name:
        with open("/mnt/workdir/origin", "w") as f:
            f.write(metadata["origin"])
            f.close()

    if source_type == ThothAdviserIntegrationEnum.GITHUB_APP.name:
        trigger_finished_webhook(metadata=metadata, document_id=Configuration._THOTH_DOCUMENT_ID)


if __name__ == "__main__":
    trigger_integration_workflow()
