import pytest

from src.utils.general import assert_valid_csv_file


@pytest.mark.parametrize("app_name", ["thorntail_to_eapxp"])
@pytest.mark.parametrize("ide", ["vscode"])
def test_csv_report_vscode(configurations, setup_vscode, app_name, analysis_data, ide):
    """Analysis tests for VScode using various advanced options"""
    vscode = setup_vscode
    conf_object = configurations
    output_path = conf_object.configurations[0].options.output
    configuration_data = analysis_data[app_name]
    project = configuration_data["paths"]
    migration_target = configuration_data["targets"]

    vscode.open_mta_perspective()
    vscode.run_simple_analysis(project, migration_target)
    assert vscode.is_analysis_complete()

    # Assert *.csv files are generated after analysis
    assert_valid_csv_file(output_path, "AllIssues.csv")
    assert_valid_csv_file(output_path, "ApplicationFileTechnologies.csv")
    assert_valid_csv_file(output_path, "data.csv")
