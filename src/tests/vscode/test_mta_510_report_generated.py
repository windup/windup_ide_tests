import pytest

from src.models.chrome import Chrome
from src.utils.general import file_exists

chrome = Chrome()

APP_NAME = "report generated"


@pytest.mark.parametrize("app_name", [APP_NAME])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            APP_NAME: {"options": {"target": ["eap8"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_mta_510_report_generated(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-510

    vscode = setup_vscode
    vscode.set_focus()
    vscode.refresh_configuration()
    vscode.run_simple_analysis(app_name)
    vscode.is_analysis_complete()

    _, report_file_path, _ = configurations
    assert file_exists(report_file_path)
