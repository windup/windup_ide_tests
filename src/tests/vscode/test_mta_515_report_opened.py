import pytest

from src.models.chrome import Chrome

chrome = Chrome()

APP_NAME = "report opened"


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
def test_mta_515_report_opened(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-515

    vscode = setup_vscode
    vscode.set_focus()
    vscode.refresh_configuration()
    vscode.run_simple_analysis(app_name)
    vscode.is_analysis_complete()

    _, report_file_path, id = configurations
    vscode.open_report_page()
    chrome.focus_tab(id)
    active_url = chrome.get_chrome_focused_tab_url()
    assert id in active_url, "The report that was opened is not for this analysis run"
    chrome.close_tab(id)
    vscode.set_focus()
