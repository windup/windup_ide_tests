import json
import os

import pytest

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/data/"


@pytest.mark.parametrize("app_name", json.load(open(DATA_DIR + "analysis.json")))
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_analysis_vscode(setup_vscode, configurations, app_name, ide):
    # def test_analysis_vscode(setup_vscode, configurations, app_name, analysis_data, ide):
    """Analysis tests for VScode using various migration paths"""
    vscode = setup_vscode
    # application_data = analysis_data[app_name]

    _, html_file_location, _ = configurations
    # expected_story_points = application_data["story_points"]

    vscode.set_focus()
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(app_name)
    status, message = vscode.is_analysis_complete(timeout=(5 * 60))
    assert status, message

    # vscode.verify_story_points(
    #     html_file_location=html_file_location,
    #     expected_story_points=expected_story_points,
    # )
