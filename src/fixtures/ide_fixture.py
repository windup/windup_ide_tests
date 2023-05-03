import json
import os
import time

import pytest

from src.models.configuration.configuration import Configuration
from src.models.configuration.configurations_object import ConfigurationsObject
from src.models.configuration.options import Options
from src.models.IDE.Intellij import Intellij
from src.models.IDE.VisualStudioCode import VisualStudioCode
from src.models.web import EclipseChe
from src.utils.general import generate_uuid
from src.utils.general import write_data_to_file

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


@pytest.fixture(scope="function")
def configurations(config, intellij_config, vscode_config, app_name, analysis_data, ide):
    # region construct configuration object and fill it from the data json

    application_config = intellij_config if ide == "intellij" else vscode_config

    configurations_object = ConfigurationsObject()

    application_data = analysis_data[app_name]
    model_json_path = f"{application_config['plugin_cache_path']}/model.json"
    project_path = config["project_path"]
    uuid = generate_uuid()

    options = (
        application_data["options"]
        if "options" in application_data
        else Options(
            target=application_data["targets"],
            input=[os.path.join(project_path, application_data["path"])],
            cli=config["windup_cli_path"],
            source_mode=True,
            output=f"{application_config['plugin_cache_path']}/{uuid}",
        )
    )

    configuration = Configuration(name=app_name, id=uuid, options=options)

    configurations_object.configurations.append(configuration)

    # endregion

    # convert the object to json and write to the model.json file
    final_configuration_json = json.dumps(configurations_object.to_dict())
    write_data_to_file(model_json_path, final_configuration_json)

    yield configurations_object

    if ide == 'intellij':
        Intellij().set_focus()
    else:
        VisualStudioCode().set_focus()

    # Empty the model.json file
    write_data_to_file(model_json_path, "")
