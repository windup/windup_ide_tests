import os

import pytest

from src.utils.general import find_mta_directory
from src.utils.general import read_file

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/data/"


@pytest.mark.vscode
def test_mta_511_plugin_info(setup_vscode, vscode_config):
    # Automates Polarion MTA-511
    vscode = setup_vscode
    vscode.set_focus()

    extensions_path = vscode_config["extensions_path"]
    readme_path = os.path.join(find_mta_directory(extensions_path), "README.md")
    fetched_vscode_plugin_info = vscode.get_plugin_details_text_from_file(readme_path)
    expected_vscode_plugin_info = read_file(DATA_DIR + "vscode_plugin_info.txt")
    vscode.close_active_tab()

    assert expected_vscode_plugin_info == fetched_vscode_plugin_info
