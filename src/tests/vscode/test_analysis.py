import json
import os

import pytest

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/data/"
MIN = 60


@pytest.mark.parametrize("app_name", json.load(open(DATA_DIR + "analysis.json")))
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
@pytest.mark.sanity
def test_analysis_vscode(setup_vscode, configurations, app_name, ide):
    # Automates polarion MTA-475, MTA-476, MTA-477, MTA-478, MTA-479, MTA-480, MTA-492, MTA-491, MTA-490
    vscode = setup_vscode
    vscode.set_focus()
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(app_name)
    status, message = vscode.is_analysis_complete(timeout=(10 * MIN))
    assert status, message
