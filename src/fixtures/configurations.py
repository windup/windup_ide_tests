import os

import pytest

from src.models.configuration.configurations_object import ConfigurationsObject
from src.models.IDE.Intellij import Intellij
from src.models.IDE.VisualStudioCode import VisualStudioCode
from src.utils.general import delete_directory
from src.utils.general import generate_uuid
from src.utils.general import write_data_to_file

CONF_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/config/"
DATA_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"


@pytest.fixture(scope="function")
def configurations(
    config,
    intellij_config,
    vscode_config,
    app_name,
    analysis_data,
    ide,
    setup_intellij,
    setup_vscode,
):
    # region construct configuration object and fill it from the data json

    uuid = generate_uuid()

    application = setup_intellij if ide == "intellij" else setup_vscode
    application_config = intellij_config if ide == "intellij" else vscode_config
    html_file_location = f"{application_config['plugin_cache_path']}/{uuid}/index.html"
    model_json_path = f"{application_config['plugin_cache_path']}/model.json"

    configurations_object = ConfigurationsObject()
    configuration = configurations_object.create(
        analysis_data,
        app_name,
        application_config,
        config,
        uuid,
    )
    application.configurations.append(configuration)

    # endregion

    yield configurations_object, html_file_location

    if ide == "intellij":
        Intellij().set_focus()
    else:
        VisualStudioCode().set_focus()

    # delete the directory containing all the analysis details
    delete_directory(os.path.join(application_config["plugin_cache_path"], uuid))

    # Empty the model.json file
    write_data_to_file(model_json_path, "")
