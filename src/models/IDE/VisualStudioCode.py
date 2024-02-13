import subprocess
import time

from src.models.application import Application
from src.models.configuration.configuration import Configuration
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
        self.configurations: [Configuration] = []
        super().__init__()

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

    def image_locator(self, locator):
        return f"image:{self.IMG_DIR}/vscode/{locator}"

    def close_ide(self):
        """
        Closes the IDE
        """
        self.press_keys("ctrl", "q")

    def delete_configuration(self, configuration_name: str):
        """
        Deletes a configuration by its name
        """
        self.cmd_palette_exec_command(VSCodeCommandEnum.DELETE_CONFIGURATIONS)
        self.type_text(configuration_name)
        self.press_keys("enter")
        self.configurations = [config for config in self.configurations if config.name != configuration_name]

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
        terminal_lines = self.copy_terminal_output()
        log_map = parse_log_string(terminal_lines[1])

        assert is_date_today(log_map["time"])
        assert log_map["msg"] == "running source code analysis"

    def is_analysis_complete(self, timeout=180):
        """
        Checks if run analysis has been completed successfully ot not by checking the terminal output

        Returns:
            (bool): True if analysis was completed, False if analysis failed, or timeout with 3 minutes default reached
        """

        start_time = time.time()

        while True:
            output_log_lines = self.copy_terminal_output()
            if output_log_lines[-1:][0] == "Analysis completed successfully":
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
        return self.get_chrome_focused_tab_url()

    def set_focus(self):
        """
        Bring vscode into focus
        """
        subprocess.run('wmctrl -R "Visual Studio Code"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def refresh_configuration(self):
        """
        Refresh the configuration tree
        """
        self.open_mta_perspective()
        self.cmd_palette_exec_command(VSCodeCommandEnum.REFRESH_CONFIGURATIONS)

    def open_plugin_info(self, plugin):
        """
        Open the MTA plugin info
        """
        self.press_keys("ctrl", "shift", "x")
        self.type_text(f"migration toolkit for {plugin}")
        time.sleep(5)
        self.press_keys("tab")
        self.press_keys("down")
        self.press_keys("enter")

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
        # todo: implement console.log("analysis canceled") in the plugin
        #  so the cancellation can be asserted more properly

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
