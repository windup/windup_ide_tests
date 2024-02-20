import pytest

from src.utils.general import file_exists


@pytest.mark.parametrize("app_name", ["report generated"])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            "report generated": {"options": {"target": ["eap8"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_report_generated(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-510

    vscode = setup_vscode
    vscode.set_focus()
    vscode.refresh_configuration()
    vscode.run_simple_analysis(app_name)
    vscode.is_analysis_complete()

    _, report_file_path, _ = configurations
    assert file_exists(report_file_path)
