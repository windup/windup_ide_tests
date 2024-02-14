from typing import Any
from typing import Dict
from typing import Optional

from src.utils.data_control import from_bool
from src.utils.data_control import from_int
from src.utils.data_control import from_none
from src.utils.data_control import from_str
from src.utils.data_control import from_union


class Summary:
    skipped_reports: Optional[bool]
    output_location: Optional[str]
    executed_timestamp: Optional[str]
    executable: Optional[str]
    executed_timestamp_raw: Optional[str]
    active: Optional[bool]
    quickfixes: Optional[Dict[str, Any]]
    hint_count: Optional[int]
    classification_count: Optional[int]

    def __init__(
        self,
        skipped_reports: Optional[bool] = False,
        output_location: Optional[str] = "",
        executed_timestamp: Optional[str] = "",
        executable: Optional[str] = "",
        executed_timestamp_raw: Optional[str] = "",
        active: Optional[bool] = False,
        quickfixes=None,
        hint_count: Optional[int] = 0,
        classification_count: Optional[int] = 0,
    ) -> None:
        if quickfixes is None:
            quickfixes = {}
        self.skipped_reports = skipped_reports
        self.output_location = output_location
        self.executed_timestamp = executed_timestamp
        self.executable = executable
        self.executed_timestamp_raw = executed_timestamp_raw
        self.active = active
        self.quickfixes = quickfixes
        self.hint_count = hint_count
        self.classification_count = classification_count

    @staticmethod
    def from_dict(obj: Any, from_int=None) -> "Summary":
        assert isinstance(obj, dict)
        skipped_reports = from_union([from_bool, from_none], obj.get("skippedReports"))
        output_location = from_union([from_str, from_none], obj.get("outputLocation"))
        executed_timestamp = from_union([from_str, from_none], obj.get("executedTimestamp"))
        executable = from_union([from_str, from_none], obj.get("executable"))
        executed_timestamp_raw = from_union([from_str, from_none], obj.get("executedTimestampRaw"))
        active = from_union([from_bool, from_none], obj.get("active"))
        quickfixes = from_union([lambda x: x, from_none], obj.get("quickfixes"))
        hint_count = from_union([from_int, from_none], obj.get("hintCount"))
        classification_count = from_union([from_int, from_none], obj.get("classificationCount"))
        return Summary(skipped_reports, output_location, executed_timestamp, executable, executed_timestamp_raw, active, quickfixes, hint_count, classification_count)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.skipped_reports is not None:
            result["skippedReports"] = from_union([from_bool, from_none], self.skipped_reports)
        if self.output_location is not None:
            result["outputLocation"] = from_union([from_str, from_none], self.output_location)
        if self.executed_timestamp is not None:
            result["executedTimestamp"] = from_union([from_str, from_none], self.executed_timestamp)
        if self.executable is not None:
            result["executable"] = from_union([from_str, from_none], self.executable)
        if self.executed_timestamp_raw is not None:
            result["executedTimestampRaw"] = from_union([from_str, from_none], self.executed_timestamp_raw)
        if self.active is not None:
            result["active"] = from_union([from_bool, from_none], self.active)
        if self.quickfixes is not None:
            result["quickfixes"] = from_union([lambda x: x, from_none], self.quickfixes)
        if self.hint_count is not None:
            result["hintCount"] = from_union([from_int, from_none], self.hint_count)
        if self.classification_count is not None:
            result["classificationCount"] = from_union([from_int, from_none], self.classification_count)
        return result
