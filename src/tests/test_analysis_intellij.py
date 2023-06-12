import json
import os
import time

import pytest

DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


@pytest.mark.parametrize("app_name", json.load(open(DATA_DIR + "analysis.json")))
@pytest.mark.parametrize("ide", ["intellij"])
def test_analysis_intellij(configurations, setup_intellij, app_name, analysis_data, ide):
    """
    Analysis tests for intellij using various migration paths
    """
    intellij = setup_intellij
    application_data = analysis_data[app_name]
    expected_story_points = application_data["story_points"]
    # Intellij freezes without this sleep
    time.sleep(3)
    intellij.run_simple_analysis(app_name)
    intellij.open_report_page(app_name)

    _, html_file_location = configurations
    if 'skip_reports' not in application_data['options']:
        intellij.verify_story_points(
            html_file_location=html_file_location,
            expected_story_points=expected_story_points,
        )
