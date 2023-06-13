import json
import os

import pytest

DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


@pytest.mark.parametrize("app_name", json.load(open(DATA_DIR + "analysis.json")))
@pytest.mark.parametrize("ide", ["vscode"])
def test_analysis_vscode(configurations, setup_vscode, app_name, analysis_data, ide):
    """Analysis tests for VScode using various migration paths"""
    vscode = setup_vscode
    application_data = analysis_data[app_name]

    expected_story_points = application_data["story_points"]

    project = application_data["path"]
    migration_target = application_data["targets"]

    vscode.open_mta_perspective()
    vscode.run_simple_analysis(project, migration_target)
    assert vscode.is_analysis_complete()

    vscode.open_report_page()
    _, html_file_location = configurations
    if "skip_reports" not in application_data["options"]:
        vscode.verify_story_points(
            html_file_location=html_file_location,
            expected_story_points=expected_story_points,
        )
