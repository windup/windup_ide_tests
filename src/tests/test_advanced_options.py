import json
import os

import pytest

DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


@pytest.mark.parametrize("app_name", json.load(open(DATA_DIR + "analysis.json")))
@pytest.mark.parametrize("ide", ["vscode"])
def test_csv_report_vscode(configurations, setup_vscode, analysis_data, ide):
    """Analysis tests for VScode using various migration paths"""
    vscode = setup_vscode
    conf_object = configurations
    output_path = conf_object.configurations[0].options.output
    application_data = analysis_data["weblogic_to_eap7_export"]
    project = application_data["path"]
    migration_target = application_data["targets"]

    vscode.open_mta_perspective()
    vscode.run_simple_analysis(project, migration_target)
    assert vscode.is_analysis_complete()

    # Assert *.csv files are generated after analysis
    assert_valid_csv_file(os.path.join(output_path, 'AllIssues.csv'))
    assert_valid_csv_file(os.path.join(output_path, 'ApplicationFileTechnologies.csv'))
