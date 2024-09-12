import json
import os

import pytest

from src.utils.general import read_file
from src.utils.general import run_command

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/data/"


@pytest.mark.vscode
def test_sources_list(config):
    # Automates Polarion MTA-484
    kantra_cli_path = config["kantra_cli_path"]
    expected_source_list = json.loads(read_file(DATA_DIR + "kantra_sources_targets_list.json"))["sources"]
    command = " analyze --list-sources"
    stdout = run_command(kantra_cli_path + command)
    found_source_list = stdout.split("\n")[1:-1]
    assert sorted(found_source_list) == sorted(expected_source_list), f"Some expected sources are missing {set(found_source_list) - set(expected_source_list)}"
