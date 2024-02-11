import json
import os

import pytest

from src.models.configuration.configurations_object import ConfigurationsObject
from src.models.IDE.Intellij import Intellij
from src.models.IDE.VisualStudioCode import VisualStudioCode
from src.utils.general import delete_directory
from src.utils.general import generate_uuid
from src.utils.general import generate_vscode_id
from src.utils.general import write_data_to_file

CONF_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/config/"
DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


@pytest.fixture(scope="function")
def configurations(config, intellij_config, vscode_config, app_name, analysis_data, ide):
    # region construct configuration object and fill it from the data json

    uuid = generate_uuid() if ide == "intellij" else generate_vscode_id()
    application = Intellij() if ide == "intellij" else VisualStudioCode()
    application_config = intellij_config if ide == "intellij" else vscode_config

    html_file_location = f"{application_config['plugin_cache_path']}/{uuid}/static-report/index.html"
    model_json_path = f"{application_config['plugin_cache_path']}/model.json"

    configurations_object = ConfigurationsObject()
    configuration = configurations_object.create(
        analysis_data,
        app_name,
        application_config,
        config,
        uuid,
    )

    # convert the object to json and write to the model.json file
    final_configuration_json = json.dumps(configurations_object.to_dict())
    write_data_to_file(model_json_path, final_configuration_json)

    # append the configuration to the object
    application.configurations.append(configuration)

    # endregion

    yield configurations_object, html_file_location, uuid

    # delete the directory containing all the analysis details
    delete_directory(os.path.join(application_config["plugin_cache_path"], uuid))

    # Empty the model.json file
    write_data_to_file(model_json_path, "")
