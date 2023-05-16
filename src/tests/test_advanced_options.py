import json
import os

import pytest

DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


@pytest.mark.parametrize("app_name", json.load(open(DATA_DIR + "analysis.json")))
@pytest.mark.parametrize("ide", ["vscode"])
def test_csv_report_vscode(configurations, setup_vscode, analysis_data, ide):
    """Analysis tests for VScode using various migration paths"""
    pytest.set_trace()
    config_object = configurations
    output = config_object[0].options.output
    vscode = setup_vscode
    application_data = analysis_data["weblogic_to_eap7_export"]
    project = application_data["path"]
    migration_target = application_data["targets"]

    vscode.open_mta_perspective()
    vscode.run_simple_analysis(project, migration_target)
    assert vscode.is_analysis_complete()

    assert_valid_csv(os.path.join(output, 'AllIssues.csv'))
    assert_valid_csv(os.path.join(output, 'ApplicationFileTechnologies.csv'))
    assert_valid_csv(os.path.join(output, 'jee_example_app_1_0_0_ear.csv'))
