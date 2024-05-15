import subprocess
import time

from src.models.application import Application
from src.models.chrome import Chrome
from src.models.configuration.configuration import Configuration
from src.models.configuration.configurations_object import ConfigurationsObject
from src.models.IDE.VSCodeCommandEnum import VSCodeCommandEnum
from src.utils.general import get_clipboard_text
from src.utils.general import is_date_today
from src.utils.general import parse_kantra_cli_command
from src.utils.general import parse_log_string


class VisualStudioCode(Application):
    """
    Class for managing VSCode application
    """

    def __init__(self):
        self.configurations_object = ConfigurationsObject()
        self.chrome = Chrome()
        super().__init__()

    def open_application(self, vscode_path, default_application, trust_workspace=False):
        subprocess.run(f"{vscode_path} {default_application} {'--disable-workspace-trust' if trust_workspace else ''}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def cmd_palette_exec_command(self, command: VSCodeCommandEnum):
        """
        Execute commands in the command palette in vscode
        """
        self.press_keys("ctrl", "shift", "p")
        time.sleep(1)
        self.type_text(command.value)
        time.sleep(1)
        self.press_keys("enter")
        time.sleep(1)

    def cmd_palette_open_file(self, file_name=None):
        """
        Opens a file by its name, or if file_name is None, then it opens recent window focused
        """
        self.press_keys("ctrl", "p")
        time.sleep(1)
        if file_name:
            self.type_text(file_name)
            time.sleep(1)
        self.press_keys("enter")

    def image_locator(self, locator):
        return f"image:{self.IMG_DIR}/vscode/{locator}"

    def close_ide(self):
        """
        Closes the IDE
        """
        self.set_focus()
        self.press_keys("ctrl", "q")

    def delete_configuration(self, configuration_name: str):
        """
        Deletes a configuration by its name
        """
        self.cmd_palette_exec_command(VSCodeCommandEnum.DELETE_CONFIGURATIONS)
        self.type_text(configuration_name)
        self.press_keys("enter")
        self.configurations_object.configurations = [config for config in self.configurations_object.configurations if config.name != configuration_name]
        time.sleep(2)

    def open_mta_perspective(self):
        """
        Opens MTA perspective in VSCode IDE
        """
        self.cmd_palette_exec_command(VSCodeCommandEnum.FOCUS_ON_EXPLORER_VIEW)

    def run_simple_analysis(self, configuration_name: str):
        """
        Runs analysis after creating an analysis configuration
        """
        # Wait for new configuration' to become visible
        self.refresh_configuration()
        self.cmd_palette_exec_command(VSCodeCommandEnum.RUN_ANALYSIS)
        self.type_text(configuration_name)
        self.press_keys("enter")

        # Verify analysis has started
        time.sleep(3)
        terminal_lines = self.copy_terminal_output()
        log_map = parse_log_string(terminal_lines[6])
        print("=====================================================")
        print("terminal lines: ")
        print(terminal_lines)
        print("=====================================================")
        assert is_date_today(log_map["time"])
        assert log_map["msg"] == "running source code analysis"

    def is_analysis_complete(self, timeout=300):
        """
        Checks if run analysis has been completed successfully ot not by checking the terminal output

        Returns:
            (bool): True if analysis was completed, False if analysis failed, or timeout with 3 minutes default reached
        """

        start_time = time.time()

        while True:
            output_log_lines = self.copy_terminal_output()
            if output_log_lines[-1:][0] == "Analysis completed successfully":
                self.update_analysis_summery()
                return True, ""
            elif output_log_lines[-1:][0] == "Analysis failed":
                return False, "Analysis Failed"
            elif time.time() - start_time > timeout:
                return False, "Timeout analysis not complete"
            time.sleep(15)

    def clear_all_notifications(self):
        """
        clean all notifications list from the notification popup
        """
        self.cmd_palette_exec_command(VSCodeCommandEnum.CLEAR_ALL_NOTIFICATIONS)

    def focus_notification_in_progress(self):
        """
        Focus on the notifications popup
        """
        self.cmd_palette_exec_command(VSCodeCommandEnum.FOCUS_NOTIFICATIONS)

    def focus_terminal_output_panel(self):
        """
        Focus on the output panel
        """
        self.cmd_palette_exec_command(VSCodeCommandEnum.FOCUS_ON_OUTPUT_VIEW)

    def copy_terminal_output(self):
        """
        Copy the content of the output panel to the clipboard
        split into lines, and return the list
        """
        self.focus_terminal_output_panel()
        self.press_keys("ctrl", "a")
        self.press_keys("ctrl", "c")
        self.press_keys("esc")
        return get_clipboard_text(True)

    def clear_terminal_output_panel(self):
        """
        Clears the content of the terminal output panel
        """
        self.cmd_palette_exec_command(VSCodeCommandEnum.CLEAR_OUTPUT)

    def open_report_page(self):
        """
        Open the report page and retrieve what is the url for the opened tab in chrome
        """
        self.focus_notification_in_progress()
        self.press_keys("tab")
        self.press_keys("enter")
        return self.chrome.get_chrome_focused_tab_url()

    def set_focus(self, timeout=10):
        """
        Bring vscode into focus, with default timeout of 10 seconds
        """
        subprocess.run('wmctrl -R "Visual Studio Code"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        start_time = time.time()
        while not self.is_focused():
            if time.time() - start_time > timeout:
                raise TimeoutError(f"VS Code did not come into focus within {timeout} seconds.")
            else:
                time.sleep(1)

    def is_focused(self):
        """
        Checks if the vscode is in focus
        """
        active_window_title = subprocess.run("xdotool getactivewindow getwindowname", shell=True, stdout=subprocess.PIPE, text=True).stdout.strip()
        return "Visual Studio Code" in active_window_title

    def refresh_configuration(self):
        """
        Refresh the configuration tree
        """
        self.open_mta_perspective()
        self.cmd_palette_exec_command(VSCodeCommandEnum.REFRESH_CONFIGURATIONS)

    def open_plugin_info(self, refocus=False):
        """
        Open the MTA plugin info
        """
        self.press_keys("ctrl", "shift", "x")
        self.type_text("migration toolkit for Applications")
        time.sleep(5)
        self.press_keys("tab")
        self.press_keys("tab")
        self.press_keys("down")
        self.press_keys("enter")
        if refocus:
            self.cmd_palette_open_file()

    def get_plugin_text(self):
        self.close_all_tabs()
        self.open_plugin_info()
        time.sleep(1)
        self.press_keys("ctrl", "tab")
        time.sleep(2)
        self.press_keys("ctrl", "a")
        time.sleep(2)
        self.press_keys("ctrl", "c")
        time.sleep(2)
        return get_clipboard_text(split=True)

    def focus_problems_panel(self):
        """
        Focus on the problems panel
        """
        self.cmd_palette_exec_command(VSCodeCommandEnum.FOCUS_ON_PROBLEMS_VIEW)

    def copy_problems_list(self):
        """
        Copy the list of problems for the open file
        """
        self.focus_problems_panel()
        self.press_keys("ctrl", "a")
        self.press_keys("ctrl", "c")
        return get_clipboard_text()

    def cancel_analysis(self):
        """
        Cancel running analysis
        """
        self.clear_all_notifications()
        self.focus_notification_in_progress()
        self.press_keys("tab")
        self.press_keys("enter")

    def close_all_tabs(self):
        """
        Close all open tabs
        """
        self.press_keys("ctrl", "k", "w")

    def close_active_tab(self):
        """
        Close only the active tab
        """
        self.press_keys("ctrl", "w")

    def fetch_executed_cli_command_map(self):
        log_lines = self.copy_terminal_output()
        return parse_kantra_cli_command(log_lines[0])

    def update_configuration(self, updated_configuration_object: Configuration):
        """
        This method updates only one configuration in the configurations_list list , not hte whole configurations_list
        remove the old configuration from the configuration_object list
        then append the updated configuration object to the configuration_object list
        then update the model.json file
        Finally, refresh the configuration in UI
        """

        self.configurations_object.configurations = [conf for conf in self.configurations_object.configurations if conf.name != updated_configuration_object.name]
        self.configurations_object.configurations.append(updated_configuration_object)
        model_file_path = self.get_model_file_path()
        self.configurations_object.update_model_json(model_file_path)
        self.refresh_configuration()

    def update_analysis_summery(self):
        """
        Update the configuration analysis summery from the model.json file
        """
        model_file_path = self.get_model_file_path()
        self.configurations_object = self.get_configurations_list_from_model_file(model_file_path)

    def get_model_file_path(self):
        output_path = self.configurations_object.configurations[0].options.output
        return output_path.rsplit("/", 1)[0] + "/model.json"
