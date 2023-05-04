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
    project = application_data["path"]
    migration_target = application_data["targets"]

    vscode.open_mta_perspective()
    vscode.run_simple_analysis(project, migration_target)
    assert vscode.is_analysis_complete()

    vscode.open_report_page()
    assert vscode.verify_story_points(migration_target)
