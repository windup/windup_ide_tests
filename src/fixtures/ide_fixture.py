import json
import os
import time

import pytest

from src.lib.IDE.Intellij import Intellij
from src.lib.IDE.VisualStudioCode import VisualStudioCode
from src.utils.general import read_file

CONF_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/config/"


@pytest.fixture(scope="session")
def intellij_config():
    """
    Fixture to configure IDE path
    """
    with open(CONF_DIR + "intellij.config.json") as config:
        intellij_config_data = json.load(config)
    return intellij_config_data


@pytest.fixture(scope="session")
def vscode_config():
    """
    Fixture to configure IDE path
    """
    with open(CONF_DIR + "vscode.config.json") as config:
        vscode_config_data = json.load(config)
    return vscode_config_data


@pytest.fixture(scope="session")
def config():
    """
    Fixture to configure IDE path
    """
    with open(CONF_DIR + "config.json") as config:
        config_data = json.load(config)
    return config_data


@pytest.fixture(scope="session")
def setup_vscode(vscode_config, config):
    """
    Fixture to setup vs code application
    """
    vscode = VisualStudioCode()
    path = vscode_config["ide_path"]
    vscode.open_application(path)
    vscode.set_default_timeout(timeout=config["timeout_in_seconds"])
    vscode.delete_config_files()
    yield vscode, config
    vscode.close_ide()


@pytest.fixture(scope="function")
def setup_intellij(intellij_config, config, configuration_data):
    """
    Fixture to setup intellij application
    """

    print(configuration_data)

    intellij = Intellij()

    ide_path = intellij_config["ide_path"]
    project_path = config["project_path"]
    plugin_cache_path = intellij_config["plugin_cache_path"]
    windup_cli_path = config["windup_cli_path"]

    configuration_name = configuration_data["name"]

    intellij.setup_configuration(
        configuration_name,
        configuration_data,
        project_path,
        windup_cli_path,
        plugin_cache_path,
    )

    ide_version = intellij.get_ide_version(ide_path)
    path = ide_path + f"/{ide_version}/bin/idea.sh"
    intellij.open_application(path)
    intellij.set_default_timeout(timeout=config["timeout_in_seconds"])

    yield intellij

    intellij.switch_tab()
    intellij.close_ide()
    time.sleep(5)
