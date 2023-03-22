import logging
import os
import re
import time

from src.models.application import Application


class Intellij(Application):
    """
    Class for managing IntelliJ application
    """

    def get_ide_version(self, ide_directory):
        pattern = re.compile(r"\d{3}\.\d{4}\.\d{2}")
        return [name for name in os.listdir(ide_directory) if pattern.search(name) is not None][0]

    def close_ide(self):
        """
        Closes the IDE
        """
        self.click_element(locator_type="image", locator="file_menu.png")
        self.press_keys("up")
        self.press_keys("enter")
        time.sleep(1)
        self.press_keys("enter")

    def image_locator(self, locator):
        return f"image:{self.IMG_DIR}/intellij/{locator}"

    def is_open_mta_perspective(self):
        """
        Checks if MTA perspective is already opened in IntelliJ

        Returns:
            (bool): True or False
        """
        try:
            self.wait_find_element(locator_type="image", locator="mta_perspective_active.png")
            return True
        except Exception as exc:
            try:
                self.wait_find_element(
                    locator_type="image",
                    locator="mta_perspective_active_alt.png",
                )
                return True
            except Exception:
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
        Opens MTA perspective in IntelliJ
        """
        if self.is_open_mta_perspective():
            logging.info("MTA perspective is already opened !")
            return
        else:
            # Click on the MTA tab in left sidebar
            self.click_element(locator_type="image", locator="mta_tab.png")

    def run_simple_analysis(self, app_name):

        config_run_region = self.two_coordinate_locator(
            locator_type="point",
            x_coordinate=110,
            y_coordinate=870,
        )
        self.click(config_run_region)
        # Search for configuration name that has to be run
        self.type_text(app_name)
        self.press_keys("enter")
        # Find config name highlighted and select correct config if multiple matches are found
        self.wait_find_element(locator_type="image", locator="config_name_highlighted.png")
        self.click(action="right_click")
        self.press_keys("up")
        self.press_keys("enter")
        # Wait for analysis to be completed in IDE terminal
        self.wait_find_element(
            locator_type="image",
            locator="analysis_complete_terminal.png",
            timeout=120.0,
        )

    def open_report_page(self, app_name):

        try:
            self.click_element(locator_type="image", locator="mta_perspective_active.png")
        except Exception:
            self.click_element(locator_type="image", locator="mta_perspective_active_alt.png")
        self.type_text(app_name)
        self.press_keys("up")
        self.click_element(locator_type="image", locator="open_details_toggle.png")
        self.click_element(locator_type="image", locator="report_selector.png")
        # Verify the report page is opened
        self.wait_find_element(locator_type="image", locator="report_page_header.png")
