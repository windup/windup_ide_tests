import re
import subprocess
import time

from src.models.application import Application
from src.models.IDE.VSCodeCommandEnum import VSCodeCommandEnum
from src.utils.general import get_clipboard_text


class VisualStudioCode(Application):
    """
    Class for managing VSCode application
    """

    def __init__(self):
        self.configurations = []
        super().__init__()

    def cmd_palette_exec_command(self, command: VSCodeCommandEnum):
        self.press_keys("ctrl", "shift", "p")
        self.type_text(command.value)
        self.press_keys("enter")

    def image_locator(self, locator):
        return f"image:{self.IMG_DIR}/vscode/{locator}"

    def close_ide(self):
        """
        Closes the IDE
        """
        self.press_keys("ctrl", "q")

    def delete_config_files(self):
        try:
            self.click_element(locator_type="image", locator="config_name_region.png")
        except Exception as exc:
            if re.match(r"Found [0-9] matches+", str(exc)):
                config_region = self.image_locator("config_name_region.png")
                config_region_circles = self.find_elements(config_region)
                self.click(config_region_circles[0])
                for i in config_region_circles:
                    time.sleep(3)
                    self.click_element(locator_type="image", locator="delete_analysis_config.png")

    def open_mta_perspective(self):
        """
        Opens MTA perspective in VSCode IDE
        """
        self.run_command_in_cmd_palette(VSCodeCommandEnum.FOCUS_ON_EXPLORER_VIEW)

    def run_simple_analysis(self):
        """
        Runs analysis after creating an analysis configuration

        Args:
            None

        Returns:
            None

        Steps:
            1) Wait for configuration to be created through fixture
            2) Click on config name and run analysis
            3) Confirm analysis has started
        """
        # Wait for new configuration' to become visible
        time.sleep(5)
        self.refresh_configuration()

        # Run analysis after clicking on config name
        try:
            self.click_element(locator_type="image", locator="config_name_region.png")
        except Exception as exc:
            if re.match(r"Found [0-9] matches+", str(exc)):
                config_region = self.image_locator("config_name_region.png")
                config_region_circles = self.find_elements(config_region)
                self.click(config_region_circles[-1])
        self.click_element(locator_type="image", locator="run_analysis.png")

        # Verify analysis has started
        self.wait_find_element(locator_type="image", locator="analysis_progress.png", timeout=240.0)

    def clear_all_notifications(self):
        self.run_command_in_cmd_palette(VSCodeCommandEnum.CLEAR_ALL_NOTIFICATIONS)

    def focus_notification_in_progress(self):
        self.run_command_in_cmd_palette(VSCodeCommandEnum.FOCUS_NOTIFICATIONS)

    def focus_terminal_output_panel(self):
        self.run_command_in_cmd_palette(VSCodeCommandEnum.FOCUS_ON_OUTPUT_VIEW)

    def copy_terminal_output(self):
        self.focus_terminal_output_panel()
        self.press_keys("ctrl", "a")
        self.press_keys("ctrl", "c")
        self.press_keys("esc")
        return get_clipboard_text(True)

    def is_analysis_complete(self):
        """
        Checks if run analysis has been completed

        Returns:
            (bool): True if analysis was completed
        """
        try:
            self.wait_find_element(
                locator_type="image",
                locator="analysis_complete.png",
                timeout=120.0,
            )
            return True
        except Exception:
            return False

    def open_report_page(self):
        self.click_element(locator_type="image", locator="open_report_button.png")
        self.wait_find_element(locator_type="image", locator="report_page_header.png")

    def set_focus(self):
        # instead of blindly clicking on alt+tab, this brings the intellij into focus
        subprocess.run("wmctrl -R code", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def refresh_configuration(self):
        # Refresh configuration via command prompt
        self.open_mta_perspective()
        self.run_command_in_cmd_palette(VSCodeCommandEnum.REFRESH_CONFIGURATIONS)

    def open_plugin_info(self, plugin):
        self.press_keys("ctrl", "shift", "x")
        self.type_text(f"migration toolkit for {plugin}")
        time.sleep(5)
        self.press_keys("tab")
        self.press_keys("down")
        self.press_keys("enter")

    def focus_problems_panel(self):
        self.run_command_in_cmd_palette(VSCodeCommandEnum.FOCUS_ON_PROBLEMS_VIEW)

    def copy_problems_list(self):
        self.focus_problems_panel()
        self.press_keys("ctrl", "a")
        self.press_keys("ctrl", "c")
        return get_clipboard_text()
