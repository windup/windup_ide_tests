import os

import pytest

from src.utils.general import read_file

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/data/"


@pytest.mark.vscode
def test_mta_511_plugin_info(setup_vscode):
    # Automates Polarion MTA-511

    vscode = setup_vscode
    vscode.set_focus()
    fetched_vscode_plugin_info = vscode.get_plugin_text()
    expected_vscode_plugin_info = read_file(DATA_DIR + "vscode_plugin_info.txt").split("\n")
    vscode.close_active_tab()

    assert set(expected_vscode_plugin_info) == set(fetched_vscode_plugin_info)
