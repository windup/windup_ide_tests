from typing import Any

from src.lib.data.configuration.options import Options
from src.utils.data_control import from_str
from src.utils.data_control import to_class


class Configuration:
    name: str
    options: Options
    id: str

    def __init__(self, name: str = None, options: Options = Options(), id: str = None) -> None:
        self.name = name
        self.options = options
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "Configuration":
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        options = Options.from_dict(obj.get("options"))
        id = obj.get("id")
        return Configuration(name, options, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["options"] = to_class(Options, self.options)
        result["id"] = str(self.id)
        return result

    def add_options(self, options: []):
        for option, value in options:
            self.options.__setattr__(option, value)
