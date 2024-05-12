import json
import os
import time

import pytest

from src.models.chrome import Chrome

chrome = Chrome()
DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/data/"


@pytest.mark.parametrize("app_name", json.load(open(DATA_DIR + "analysis.json")))
@pytest.mark.parametrize("ide", ["intellij"])
@pytest.mark.intellij
def test_analysis_intellij(configurations, setup_intellij, app_name, analysis_data, ide, intellij_config):
    """
    Analysis tests for intellij using various migration paths
    """
    intellij = setup_intellij
    # TODO: add story point verification and report opening
    time.sleep(3)
    intellij.run_simple_analysis(app_name)
    _, report_file_path, id = configurations
    intellij.open_report_page()
    chrome.focus_tab(id)
    active_url = chrome.get_chrome_focused_tab_url()
    assert id in active_url, "The report that was opened is not for this analysis run"
    chrome.close_tab(id)
    intellij.set_focus()
