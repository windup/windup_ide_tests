import time

import pytest

from src.utils.general import assert_valid_csv_file


@pytest.mark.parametrize("app_name", ["weblogic_to_eap7"])
@pytest.mark.parametrize("ide", ["intellij"])
def test_csv_report_intellij(configurations, setup_intellij, app_name, analysis_data, ide):
    """Analysis tests for IntelliJ using various advanced options"""
    intellij = setup_intellij
    conf_object = configurations
    output_path = conf_object.configurations[0].options.output
    # Intellij freezes without this sleep
    time.sleep(3)
    intellij.run_simple_analysis(app_name)
    intellij.open_report_page(app_name)

    assert intellij.is_analysis_complete()

    # Assert *.csv files are generated after analysis
    assert_valid_csv_file(output_path, "AllIssues.csv")
    assert_valid_csv_file(output_path, "ApplicationFileTechnologies.csv")
    assert_valid_csv_file(output_path, "data.csv")
