import json
import os
import time

import pytest

DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


@pytest.mark.parametrize("app_name", json.load(open(DATA_DIR + "analysis.json")))
def test_analysis_intellij(configurations_object, setup_intellij, app_name, analysis_data):
    """
    Analysis tests for intellij using various migration paths
    """
    intellij = setup_intellij
    application_data = analysis_data[app_name]
    migration_targets = application_data["targets"]

    time.sleep(5)
    intellij.open_mta_perspective()

    # Intellij freezes without this sleep
    time.sleep(3)
    intellij.run_simple_analysis(app_name)
    intellij.open_report_page(app_name)

    assert intellij.is_analysis_complete()
    assert intellij.verify_story_points(target=migration_targets[0])
