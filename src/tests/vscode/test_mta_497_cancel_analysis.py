import time

import pytest

APP_NAME = "cancel analysis"


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
def test_mta_497_delete_configuration(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-497

    vscode = setup_vscode
    vscode.set_focus()
    vscode.refresh_configuration()
    vscode.run_simple_analysis(app_name)
    time.sleep(2)
    vscode.cancel_analysis()
    terminal_output_lines = vscode.copy_terminal_output()
    assert terminal_output_lines[-1:][0] == "Analysis canceled", "Failed to cancel analysis"
