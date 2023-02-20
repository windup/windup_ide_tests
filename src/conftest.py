import json
import os

import pytest

from src.lib.config import config_data
from src.utils.general import read_file

pytest_plugins = ["src.fixtures.ide_fixture"]


def pytest_generate_tests(metafunc):
    configuration_json_file = (
        os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        + config_data["configurations_data"]
    )

    configurations_data: [] = json.loads(read_file(configuration_json_file))["configurations"]

    for configuration in configurations_data:
        target = "_".join(configuration["target"])
        source = "_".join(configuration["source"])
        configuration["name"] = f"{target}_from_{source}"

    configurations_data = [
        pytest.param(configuration["name"], configuration, id=f"{configuration['name']}_analysis")
        for configuration in configurations_data
    ]

    if "configuration_name" and "configuration_data" in metafunc.fixturenames:
        metafunc.parametrize("configuration_name, configuration_data", configurations_data)
