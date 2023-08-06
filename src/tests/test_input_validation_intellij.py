import os
import time

import pytest

from src.models.configuration.configuration import Configuration

DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


CONFIGURATION_JSON =   {
    "paths": [
      ""
    ],
    "options": {
      "targets": [
        "eap8"
      ]
    },
    "story_points": [
      117
    ]
  },

@pytest.mark.parametrize("ide", ["intellij"])
def test_input_validation(setup_intellij, app_name, ide):
    """
    Analysis tests for intellij using various migration paths
    """

    config = Configuration.from_dict(CONFIGURATION_JSON)
    intellij = setup_intellij

    intellij.refresh_configuration()


    # Intellij freezes without this sleep
    time.sleep(3)
    intellij.run_simple_analysis(app_name)
    intellij.open_report_page(app_name)
