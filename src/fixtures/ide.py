import json
import os
import time

import pytest

from src.models.IDE.Intellij import Intellij
from src.models.IDE.VisualStudioCode import VisualStudioCode
from src.models.web import EclipseChe

CONF_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/config/"
DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


@pytest.fixture(scope="session")
def intellij_config():
    """
    Fixture to configure IDE path
    """
    with open(CONF_DIR + "intellij_config.json") as config:
        intellij_config_data = json.load(config)
    return intellij_config_data


@pytest.fixture(scope="session")
def vscode_config():
    """
    Fixture to configure IDE path
    """
    with open(CONF_DIR + "vscode_config.json") as config:
        vscode_config_data = json.load(config)
    return vscode_config_data


@pytest.fixture(scope="session")
def config():
    """
    Fixture to configure IDE path
    """
    with open(CONF_DIR + "ide_config.json") as config:
        config_data = json.load(config)
    return config_data


@pytest.fixture(scope="session")
def analysis_data():
    with open(DATA_DIR + "analysis.json", "r") as file:
        json_list = json.load(file)
    return json_list


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
    yield vscode
    vscode.close_ide()


@pytest.fixture(scope="function")
def setup_eclipse_che():
    """
    Fixture to setup eclipse che workspace
    """
    eclipse_che = EclipseChe("chrome")
    eclipse_che.open_workspace()
    yield eclipse_che
    eclipse_che.delete_configuration(eclipse_che.configuration_name)
    eclipse_che.close_browser()


@pytest.fixture(scope="session")
def setup_intellij(intellij_config, config):
    """
    Fixture to setup intellij application
    """
    intellij = Intellij()
    ide_path = intellij_config["ide_path"]
    ide_version = intellij.get_ide_version(ide_path)
    path = ide_path + f"/{ide_version}/bin/idea.sh"
    intellij.open_application(path)
    intellij.set_default_timeout(timeout=config["timeout_in_seconds"])
    time.sleep(5)
    intellij.open_mta_perspective()

    yield intellij

    intellij.set_focus()
    intellij.close_ide()
    time.sleep(5)
