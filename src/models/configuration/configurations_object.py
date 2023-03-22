from typing import Any
from typing import List

from src.models.configuration.configuration import Configuration
from src.utils.data_control import from_list
from src.utils.data_control import to_class


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
