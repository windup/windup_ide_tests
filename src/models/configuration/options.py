from typing import Any
from typing import List
from typing import Optional

from src.utils.data_control import from_bool
from src.utils.data_control import from_list
from src.utils.data_control import from_none
from src.utils.data_control import from_str
from src.utils.data_control import from_stringified_bool
from src.utils.data_control import from_union
from src.utils.data_control import is_type


class Options:
    source_mode: bool
    output: Optional[str]
    input: Optional[List[str]]
    cli: Optional[str]
    cloning: List[Any]
    target: Optional[List[str]]
    legacy_reports: bool
    mode: str
    overwrite: Optional[bool]
    analyze_known_libraries: Optional[bool]
    source: Optional[List[str]]

    def __init__(
        self,
        output: str = "",
        input: List[str] = "",
        cli: str = "",
        target: Optional[List[str]] = [],
        overwrite: Optional[bool] = False,
        source: Optional[List[str]] = [],
        analyze_known_libraries: Optional[bool] = False,
    ) -> None:
        self.source_mode = True
        self.output = output
        self.input = input
        self.cli = cli
        self.cloning = []
        self.target = target
        self.legacy_reports = True
        self.mode = "source-only"
        self.overwrite = overwrite
        self.source = source
        self.analyze_known_libraries = analyze_known_libraries

    @staticmethod
    def from_dict(obj: Any) -> "Options":
        assert isinstance(obj, dict)
        output = from_union([from_str, from_none], obj.get("output"))
        input = from_union([lambda x: from_list(from_str, x), from_none], obj.get("input"))
        cli = from_union([from_str, from_none], obj.get("cli"))
        target = from_union([lambda x: from_list(from_str, x), from_none], obj.get("target"))
        overwrite = from_union([from_none, from_bool, lambda x: from_stringified_bool(from_str(x)) if isinstance(x, str) else x], obj.get("overwrite"))
        analyze_known_libraries = from_union([from_none, from_bool, lambda x: from_stringified_bool(from_str(x)) if isinstance(x, str) else x], obj.get("analyze-known-libraries"))
        source = from_union([lambda x: from_list(from_str, x), from_none], obj.get("source"))
        return Options(output, input, cli, target, overwrite, source, analyze_known_libraries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sourceMode"] = from_bool(self.source_mode)
        result["output"] = from_str(self.output)
        result["input"] = from_list(from_str, self.input)
        result["cli"] = from_str(self.cli)
        result["cloning"] = from_list(lambda x: x, self.cloning)
        if self.target is not None:
            result["target"] = from_union([lambda x: from_list(from_str, x), from_none], self.target)
        if self.legacy_reports is not None:
            result["legacyReports"] = from_union([from_bool, from_none], self.legacy_reports)
        if self.mode is not None:
            result["mode"] = from_union([from_str, from_none], self.mode)
        if self.overwrite is not None:
            result["overwrite"] = from_union(
                [lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))],
                self.overwrite,
            )
        if self.source is not None:
            result["source"] = from_union([lambda x: from_list(from_str, x), from_none], self.source)
        if self.analyze_known_libraries is not None:
            result["analyze-known-libraries"] = from_union(
                [lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))],
                self.analyze_known_libraries,
            )
        return result
