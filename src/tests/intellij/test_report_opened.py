import time

import pytest

from src.models.chrome import Chrome

APP_NAME = "report opened"

chrome = Chrome()


@pytest.mark.parametrize("app_name", [APP_NAME])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            APP_NAME: {"options": {"target": ["eap8"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["intellij"])
@pytest.mark.intellij
def test_report_opened(configurations, setup_intellij, app_name, analysis_data, ide, intellij_config):
    intellij = setup_intellij
    time.sleep(3)
    intellij.run_simple_analysis(app_name)
    _, report_file_path, id = configurations
    intellij.open_report_page()
    chrome.focus_tab(id)
    active_url = chrome.get_chrome_focused_tab_url()
    assert id in active_url, "The report that was opened is not for this analysis run"
    chrome.close_tab(id)
    intellij.set_focus()
