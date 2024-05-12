import json
import os
import time

import pytest

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/data/"


@pytest.mark.parametrize("app_name", json.load(open(DATA_DIR + "analysis.json")))
@pytest.mark.parametrize("ide", ["intellij"])
@pytest.mark.intellij
def test_analysis_intellij(configurations, setup_intellij, app_name, analysis_data, ide, intellij_config):
    """
    Analysis tests for intellij using various migration paths
    """
    intellij = setup_intellij
    time.sleep(3)
    intellij.run_simple_analysis(app_name)
