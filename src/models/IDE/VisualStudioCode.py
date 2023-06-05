import logging
import re
import subprocess
import time

from src.models.application import Application


class VisualStudioCode(Application):
    """
    Class for managing VSCode application
    """

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

    def is_open_mta_perspective(self):
        """
        Checks if MTA perspective is already opened in VS Code

        Returns:
            (bool): True or False
        """
        try:
            self.wait_find_element(locator_type="image", locator="create_new_config.png")
            return True
        except Exception as exc:
            logging.debug(
                "An error occured while finding \
                MTA perspective tab ! {}".format(
                    str(exc),
                ),
            )
            if "No matches found" in str(exc):
                return False
            else:
                raise Exception(exc)

    def open_mta_perspective(self):
        """
        Opens MTA perspective in VSCode IDE
        """
        if self.is_open_mta_perspective():
            logging.info("MTA perspective is already opened !")
            return
        else:
            # Click on the MTA icon in left sidebar
            time.sleep(10)
            self.click_element(locator_type="image", locator="mta_config_inactive.png")

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
        # Click 'Refresh configurations' button
        self.wait_find_element(locator_type="image", locator="refresh_configurations.png")
        self.click_element(locator_type="image", locator="refresh_configurations.png")
