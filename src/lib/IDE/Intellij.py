import logging
import os
import re
import time

from src.lib.application import Application
from src.lib.config import config_data
from src.utils.general import clear_directory_by_name
from src.utils.general import download_file
from src.utils.general import unzip_file


class Intellij(Application):
    """
    Class for managing IntelliJ application
    """

    def get_ide_version(self, ide_directory):
        pattern = re.compile(r"\d{3}\.\d{4}\.\d{2}")
        return [name for name in os.listdir(ide_directory) if pattern.search(name) is not None][0]

    def install_plugin(self, url, ide_directory, plugin_file_name):

        ide_version = self.get_ide_version(ide_directory)
        plugin_file_path = f"{ide_directory}/{ide_version}.plugins/{plugin_file_name}"
        download_file(url, f"{ide_directory}/{ide_version}.plugins", plugin_file_name)
        unzip_file(plugin_file_path, f"{ide_directory}/{ide_version}.plugins/")

    def uninstall_plugin(self, plugins_directory, plugin):
        clear_directory_by_name(plugins_directory, plugin)

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

    def run_simple_analysis(self, project, migration_target, packages=[]):
        """
        Runs analysis by adding the project and/or packages passed as argument

        Args:
            project (str): Full name of project to be analysed
            migration_target (str): Target technology for migration
            packages (list): List of packages to be added to analysis

        Returns:
            None

        Steps:
            1) Click on MTA Configuration tab
            2) Right click anywhere and create new configuration
            3) Type project name in source
            4) Provide mta cli path, if not present
            5) Select the target technology
            6) Right click on config name and run
            7) Confirm analysis has started
        """
        try:
            self.click_element(locator_type="image", locator="console_opened.png")
            self.press_keys("shift", "esc")
        except Exception as exc:
            try:
                self.click_element(locator_type="image", locator="console_opened_alt.png")
                self.press_keys("shift", "esc")
            except Exception:
                logging.debug("Console is already closed !")
            logging.debug("Console is not opened ! {}".format(str(exc)))
        config_create_region = self.two_coordinate_locator(
            locator_type="point",
            x_coordinate=110,
            y_coordinate=370,
        )
        self.click(config_create_region)
        self.click(action="right_click")
        self.press_keys("down")
        self.press_keys("enter")
        time.sleep(3)
        self.wait_find_element(locator_type="image", locator="mta_config_page_opened.png")
        # Region defining the configuration name
        config_name_region = self.define_region(778, 248, 1125, 284)
        add_project_locator = self.image_locator("add_project_button.png")
        add_project_buttons = self.find_elements(add_project_locator)
        # Provide mta cli path
        try:
            self.click(add_project_buttons[0])
            time.sleep(2)
            for letter in config_data["mta_cli_path"]:
                self.type_text(letter)
            self.press_keys("enter")
        except Exception as exc:
            logging.debug("MTA cli path is already present ! {}".format(exc))
        if migration_target != "eap7":
            try:
                self.wait_find_element(locator_type="image", locator="eap7_checked.png")
                self.click_element(locator_type="image", locator="eap7_checked.png")
            except Exception as exc:
                logging.debug("Default target eap7 is not checked ! {}".format(str(exc)))

        # Click the first match out of the two same buttons found
        self.click(add_project_buttons[1])
        self.type_text(text=project, enter=True)
        self.click(config_name_region)
        print(f"buttons found: {str(len(add_project_buttons))}")
        if len(add_project_buttons) != 3:
            self.press_keys("page_down")
        self.click_element(locator_type="image", locator="add_project_button.png")
        self.type_text(text=migration_target, enter=True)
        config_run_region = self.two_coordinate_locator(
            locator_type="point",
            x_coordinate=110,
            y_coordinate=870,
        )
        self.click(config_run_region)
        # Search for configuration name that has to be run
        self.type_text("configuration1")
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
        # Select the run configuration and open report page in browser
        try:
            self.click_element(locator_type="image", locator="mta_perspective_active.png")
        except Exception:
            self.click_element(locator_type="image", locator="mta_perspective_active_alt.png")
        self.type_text("configuration1")
        self.press_keys("up")
        self.click_element(locator_type="image", locator="open_details_toggle.png")
        self.click_element(locator_type="image", locator="report_selector.png")
        # Verify the report page is opened
        self.wait_find_element(locator_type="image", locator="report_page_header.png")
