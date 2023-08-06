import json
import os

import pytest

from src.models.configuration.configuration import Configuration
from src.models.configuration.configurations_object import ConfigurationsObject
from src.models.configuration.options import Options
from src.models.IDE.Intellij import Intellij
from src.models.IDE.VisualStudioCode import VisualStudioCode
from src.utils.general import delete_directory
from src.utils.general import generate_uuid
from src.utils.general import write_data_to_file

CONF_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/config/"
DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


@pytest.fixture(scope="function")
def configurations(config, intellij_config, vscode_config, app_name, analysis_data, ide):

    # region construct configuration object and fill it from the data json

    uuid = generate_uuid()

    application_config = intellij_config if ide == "intellij" else vscode_config
    html_file_location = f"{application_config['plugin_cache_path']}/{uuid}/index.html"

    configurations_object = ConfigurationsObject()

    application_data = analysis_data[app_name]
    model_json_path = f"{application_config['plugin_cache_path']}/model.json"
    project_path = config["project_path"]

    inputs = [os.path.join(project_path, path) for path in application_data["paths"]]

    # Build data for analysis configuration
    options = Options.from_dict(application_data["options"])
    options.input = inputs
    options.cli = config["windup_cli_path"]
    options.source_mode = True
    options.output = f"{application_config['plugin_cache_path']}/{uuid}"

    configuration = Configuration(name=app_name, id=uuid, options=options)

    configurations_object.configurations.append(configuration)

    # endregion

    # convert the object to json and write to the model.json file
    final_configuration_json = json.dumps(configurations_object.to_dict())
    write_data_to_file(model_json_path, final_configuration_json)

    yield configurations_object, html_file_location

    if ide == "intellij":
        Intellij().set_focus()
    else:
        VisualStudioCode().set_focus()

    # delete the directory containing all the analysis details
    delete_directory(os.path.join(application_config["plugin_cache_path"], uuid))

    # Empty the model.json file
    write_data_to_file(model_json_path, "")