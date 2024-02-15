import json
from typing import Any
from typing import List

from src.models.configuration.configuration import Configuration
from src.models.configuration.options import Options
from src.utils.data_control import from_list
from src.utils.data_control import to_class
from src.utils.general import write_data_to_file


class ConfigurationsObject:
    configurations: List[Configuration]

    def __init__(self, configurations=None) -> None:
        self.configurations = [] if configurations is None else configurations

    @staticmethod
    def from_dict(obj: Any) -> "ConfigurationsObject":
        assert isinstance(obj, dict)
        configurations = from_list(Configuration.from_dict, obj.get("configurations"))
        return ConfigurationsObject(configurations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["configurations"] = from_list(
            lambda x: to_class(Configuration, x),
            self.configurations,
        )
        return result

    def create(self, analysis_data, app_name, application_config, config, uuid):
        application_data = analysis_data[app_name]
        project_path = config["project_path"]

        # Build data for analysis configuration
        options = Options.from_dict(application_data["options"])
        options.input = [project_path]
        options.cli = config["windup_cli_path"]
        options.output = f"{application_config['plugin_cache_path']}/{uuid}"

        configuration = Configuration(name=app_name, id=uuid, options=options)

        self.configurations.append(configuration)

        return configuration

    def update_model_json(self, model_json_path):
        write_data_to_file(model_json_path, json.dumps(self.to_dict()))

    def get_configuration(self, configuration_name) -> Configuration:
        return [config for config in self.configurations if config.name == configuration_name][0]
