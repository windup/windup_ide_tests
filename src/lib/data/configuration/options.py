from typing import Any
from typing import List
from typing import Optional

from src.utils.data_control import from_list
from src.utils.data_control import from_none
from src.utils.data_control import from_str
from src.utils.data_control import from_stringified_bool
from src.utils.data_control import from_union
from src.utils.data_control import is_type


class Options:
    exclude_tags: Optional[List[str]]
    source_mode: bool
    user_rules_directory: Optional[List[str]]
    disable_tattletale: Optional[bool]
    additional_classpath: Optional[List[str]]
    include_tags: Optional[List[str]]
    source: Optional[List[str]]
    enable_transaction_analysis: Optional[bool]
    packages: Optional[List[str]]
    enable_compatible_files_report: Optional[bool]
    target: List[str]
    output: str
    enable_class_not_found_analysis: Optional[bool]
    input: Optional[List[str]]
    user_ignore_path: Optional[List[str]]
    exclude_packages: Optional[List[str]]
    mavenize: Optional[bool]
    exploded_app: Optional[bool]
    keep_work_dirs: Optional[bool]
    online: Optional[bool]
    windup_cli: str
    skip_reports: Optional[bool]
    overwrite: Optional[bool]
    export_csv: Optional[bool]

    def __init__(
        self,
        exclude_tags: Optional[List[str]] = None,
        source_mode: bool = None,
        user_rules_directory: Optional[List[str]] = None,
        disable_tattletale: Optional[bool] = None,
        additional_classpath: Optional[List[str]] = None,
        include_tags: Optional[List[str]] = None,
        source: Optional[List[str]] = None,
        enable_transaction_analysis: Optional[bool] = None,
        packages: Optional[List[str]] = None,
        enable_compatible_files_report: Optional[bool] = None,
        target: List[str] = None,
        output: str = None,
        enable_class_not_found_analysis: Optional[bool] = None,
        input: Optional[List[str]] = None,
        user_ignore_path: Optional[List[str]] = None,
        exclude_packages: Optional[List[str]] = None,
        mavenize: Optional[bool] = None,
        exploded_app: Optional[bool] = None,
        keep_work_dirs: Optional[bool] = None,
        online: Optional[bool] = None,
        windup_cli: str = None,
        skip_reports: Optional[bool] = None,
        overwrite: Optional[bool] = None,
        export_csv: Optional[bool] = None,
    ) -> None:
        self.exclude_tags = exclude_tags
        self.source_mode = source_mode
        self.user_rules_directory = user_rules_directory
        self.disable_tattletale = disable_tattletale
        self.additional_classpath = additional_classpath
        self.include_tags = include_tags
        self.source = source
        self.enable_transaction_analysis = enable_transaction_analysis
        self.packages = packages
        self.enable_compatible_files_report = enable_compatible_files_report
        self.target = target
        self.output = output
        self.enable_class_not_found_analysis = enable_class_not_found_analysis
        self.input = input
        self.user_ignore_path = user_ignore_path
        self.exclude_packages = exclude_packages
        self.mavenize = mavenize
        self.exploded_app = exploded_app
        self.keep_work_dirs = keep_work_dirs
        self.online = online
        self.windup_cli = windup_cli
        self.skip_reports = skip_reports
        self.overwrite = overwrite
        self.export_csv = export_csv

    @staticmethod
    def from_dict(obj: Any) -> "Options":
        assert isinstance(obj, dict)
        exclude_tags = from_union(
            [lambda x: from_list(from_str, x), from_none],
            obj.get("excludeTags"),
        )
        source_mode = from_stringified_bool(from_str(obj.get("sourceMode")))
        user_rules_directory = from_union(
            [lambda x: from_list(from_str, x), from_none],
            obj.get("userRulesDirectory"),
        )
        disable_tattletale = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("disableTattletale"),
        )
        additional_classpath = from_union(
            [lambda x: from_list(from_str, x), from_none],
            obj.get("additionalClasspath"),
        )
        include_tags = from_union(
            [lambda x: from_list(from_str, x), from_none],
            obj.get("includeTags"),
        )
        source = from_union([lambda x: from_list(from_str, x), from_none], obj.get("source"))
        enable_transaction_analysis = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("enableTransactionAnalysis"),
        )
        packages = from_union([lambda x: from_list(from_str, x), from_none], obj.get("packages"))
        enable_compatible_files_report = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("enableCompatibleFilesReport"),
        )
        target = from_list(from_str, obj.get("target"))
        output = from_str(obj.get("output"))
        enable_class_not_found_analysis = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("enableClassNotFoundAnalysis"),
        )
        input = from_union([lambda x: from_list(from_str, x), from_none], obj.get("input"))
        user_ignore_path = from_union(
            [lambda x: from_list(from_str, x), from_none],
            obj.get("userIgnorePath"),
        )
        exclude_packages = from_union(
            [lambda x: from_list(from_str, x), from_none],
            obj.get("excludePackages"),
        )
        mavenize = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("mavenize"),
        )
        exploded_app = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("explodedApp"),
        )
        keep_work_dirs = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("keepWorkDirs"),
        )
        online = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("online"),
        )
        windup_cli = from_str(obj.get("windup-cli"))
        skip_reports = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("skipReports"),
        )
        overwrite = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("overwrite"),
        )
        export_csv = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("exportCSV"),
        )
        return Options(
            exclude_tags,
            source_mode,
            user_rules_directory,
            disable_tattletale,
            additional_classpath,
            include_tags,
            source,
            enable_transaction_analysis,
            packages,
            enable_compatible_files_report,
            target,
            output,
            enable_class_not_found_analysis,
            input,
            user_ignore_path,
            exclude_packages,
            mavenize,
            exploded_app,
            keep_work_dirs,
            online,
            windup_cli,
            skip_reports,
            overwrite,
            export_csv,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.exclude_tags is not None:
            result["excludeTags"] = from_union(
                [lambda x: from_list(from_str, x), from_none],
                self.exclude_tags,
            )
        result["sourceMode"] = from_str(str(self.source_mode).lower())
        if self.user_rules_directory is not None:
            result["userRulesDirectory"] = from_union(
                [lambda x: from_list(from_str, x), from_none],
                self.user_rules_directory,
            )
        if self.disable_tattletale is not None:
            result["disableTattletale"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.disable_tattletale,
            )
        if self.additional_classpath is not None:
            result["additionalClasspath"] = from_union(
                [lambda x: from_list(from_str, x), from_none],
                self.additional_classpath,
            )
        if self.include_tags is not None:
            result["includeTags"] = from_union(
                [lambda x: from_list(from_str, x), from_none],
                self.include_tags,
            )
        if self.source is not None:
            result["source"] = from_union(
                [lambda x: from_list(from_str, x), from_none],
                self.source,
            )
        if self.enable_transaction_analysis is not None:
            result["enableTransactionAnalysis"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.enable_transaction_analysis,
            )
        if self.packages is not None:
            result["packages"] = from_union(
                [lambda x: from_list(from_str, x), from_none],
                self.packages,
            )
        if self.enable_compatible_files_report is not None:
            result["enableCompatibleFilesReport"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.enable_compatible_files_report,
            )
        result["target"] = from_list(from_str, self.target)
        result["output"] = from_str(self.output)
        if self.enable_class_not_found_analysis is not None:
            result["enableClassNotFoundAnalysis"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.enable_class_not_found_analysis,
            )
        if self.input is not None:
            result["input"] = from_union([lambda x: from_list(from_str, x), from_none], self.input)
        if self.user_ignore_path is not None:
            result["userIgnorePath"] = from_union(
                [lambda x: from_list(from_str, x), from_none],
                self.user_ignore_path,
            )
        if self.exclude_packages is not None:
            result["excludePackages"] = from_union(
                [lambda x: from_list(from_str, x), from_none],
                self.exclude_packages,
            )
        if self.mavenize is not None:
            result["mavenize"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.mavenize,
            )
        if self.exploded_app is not None:
            result["explodedApp"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.exploded_app,
            )
        if self.keep_work_dirs is not None:
            result["keepWorkDirs"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.keep_work_dirs,
            )
        if self.online is not None:
            result["online"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.online,
            )
        result["windup-cli"] = from_str(self.windup_cli)
        if self.skip_reports is not None:
            result["skipReports"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.skip_reports,
            )
        if self.overwrite is not None:
            result["overwrite"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.overwrite,
            )
        if self.export_csv is not None:
            result["exportCSV"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)),
                ],
                self.export_csv,
            )
        return result