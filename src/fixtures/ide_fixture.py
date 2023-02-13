import json
import os
import time

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.config import Config

from src.lib.IDE.Intellij import Intellij
from src.lib.IDE.VisualStudioCode import VisualStudioCode
from src.lib.web import EclipseChe

CONF_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/conf/"


@pytest.fixture(scope="session")
def config():
    """
    Fixture to configure IDE path
    """
    with open(CONF_DIR + "config.json") as config:
        config_data = json.load(config)
    return config_data


@pytest.fixture(scope="session")
def pytestconfig(request: FixtureRequest) -> Config:
    return request.config


@pytest.fixture(scope="session")
def setup_vscode(config):
    """
    Fixture to setup vs code application
    """
    vscode = VisualStudioCode()
    path = config["ide"]["vs_code"]
    vscode.open_application(path)
    vscode.set_default_timeout(timeout=config["timeout_in_seconds"])
    vscode.delete_config_files()
    yield vscode, config
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
def setup_intellij(config, pytestconfig):
    """
    Fixture to setup intellij application
    """
    intellij = Intellij()

    plugin_url = config["ide"]["intellij"]["plugins"][0]["plugin_url"]
    ide_path = config["ide"]["intellij"]["ide_path"]
    plugin_file_name = config["ide"]["intellij"]["plugins"][0]["name"]

    ide_version = intellij.get_ide_version(ide_path)
    intellij.install_plugin(plugin_url, ide_path, f"{plugin_file_name}.zip")

    path = ide_path + f"/{ide_version}/bin/idea.sh"
    intellij.open_application(path)
    intellij.set_default_timeout(timeout=config["timeout_in_seconds"])
    yield intellij
    intellij.close_ide()
    intellij.uninstall_plugin(f"{ide_path}/{ide_version}.plugins", plugin_file_name)
    time.sleep(5)
