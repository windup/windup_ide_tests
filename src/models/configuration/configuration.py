from typing import Any

from src.models.configuration.options import Options
from src.models.configuration.summery import Summary
from src.utils.data_control import from_none
from src.utils.data_control import from_str
from src.utils.data_control import from_union
from src.utils.data_control import to_class


class Configuration:
    name: str
    options: Options
    id: str
    summary: Summary

    def __init__(self, name: str = None, options: Options = Options(), id: str = None, summary=Summary()) -> None:
        self.name = name
        self.options = options
        self.id = id
        self.summary = summary

    @staticmethod
    def from_dict(obj: Any) -> "Configuration":
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        options = Options.from_dict(obj.get("options"))
        id = obj.get("id")
        summary = from_union([Summary.from_dict, from_none], obj.get("summary"))
        return Configuration(name, options, id, summary)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["options"] = to_class(Options, self.options)
        result["id"] = str(self.id)
        if self.summary is not None:
            result["summary"] = from_union([lambda x: to_class(Summary, x), from_none], self.summary)
        return result

    def add_options(self, options: []):
        for option, value in options:
            self.options.__setattr__(option, value)

    def update_summery(self, summery: Summary):
        self.summary = summery
