import json
import os
import time

import pytest

DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


@pytest.mark.parametrize("app_name", json.load(open(DATA_DIR + "analysis.json")))
def test_analysis_eap(setup_intellij, app_name, analysis_data):
    """
    Analysis tests for VScode using various migration paths
    """
    intellij = setup_intellij
    time.sleep(5)
    intellij.open_mta_perspective()
    application_data = analysis_data[app_name]
    project = application_data["path"]
    migration_targets = application_data["targets"]

    # Intellij freezes without this sleep
    time.sleep(3)

    intellij.run_simple_analysis(
        project=project,
        migration_target=migration_targets,
    )

    intellij.open_report_page()
    assert intellij.is_analysis_complete()
    assert intellij.verify_story_points(target=migration_targets[0])
