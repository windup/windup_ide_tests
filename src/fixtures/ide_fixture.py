import json
import os

import pytest

from src.lib.application import CodeReadyStudio
from src.lib.application import Eclipse


CONF_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/conf/"


@pytest.fixture(scope="session")
def config():
    """
    Fixture to configure IDE path
    """
    with open(CONF_DIR + "config.json") as config:
        config_data = json.load(config)
    return config_data


@pytest.fixture(scope="function")
def setup_codereadystudio(config):
    """
    Fixture to setup codereadystudio application
    """
    codereadystudio = CodeReadyStudio()
    path = config["ide_paths"]["rh_code_ready_studio"]
    codereadystudio.open_application(path)
    codereadystudio.set_default_timeout(timeout=config["timeout_in_seconds"])
    yield codereadystudio
    # codereadystudio.close_application(codereadystudio_app)
    codereadystudio.close_ide()


@pytest.fixture(scope="function")
def setup_eclipse(config):
    """
    Fixture to setup eclipse application
    """
    eclipse = Eclipse()
    path = config["ide_paths"]["eclipse"]
    eclipse.open_application(path)
    eclipse.set_default_timeout(timeout=config["timeout_in_seconds"])
    yield eclipse
    eclipse.close_ide()
