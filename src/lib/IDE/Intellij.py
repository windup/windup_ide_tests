import json
import logging
import os
import re
import time

from src.lib.application import Application
from src.lib.data.configuration.configurations_object import ConfigurationsObject
from src.utils.general import generate_project_input_paths
from src.utils.general import generate_uuid
from src.utils.general import write_data_to_file


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

    def setup_configuration(
            self,
            configuration_name,
            configuration_data,
            project_path,
            windup_cli_path,
            plugin_cache_path,
    ):

        configuration_object = ConfigurationsObject()

        configuration_object.name = configuration_name
        configuration_object.options.windup_cli = windup_cli_path

        inputs = [conf]

        input_paths = generate_project_input_paths(project_path, input_tuple)

        configuration_object.options.target = [
            target for target, _ in input_tuple
        ]

        configuration_object.add_options(options)

        configuration_object.options.input = input_paths
        uuid = generate_uuid()
        output = f"{plugin_cache_path}/{uuid}"

        configuration_object.id = uuid
        configuration_object.options.source_mode = "true"
        configuration_object.options.output = output

        final_configuration_json = json.dumps(configuration_object.to_dict())

        write_data_to_file(f"{plugin_cache_path}/model.json", final_configuration_json)

    def run_simple_analysis(self, configuration_name):
        """
        Runs analysis by adding the project and/or packages passed as argument
        """

        config_run_region = self.two_coordinate_locator(
            locator_type="point",
            x_coordinate=110,
            y_coordinate=870,
        )
        self.click(config_run_region)
        # Search for configuration name that has to be run
        self.type_text(configuration_name)
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
        self.type_text(configuration_name)
        self.press_keys("up")
        self.click_element(locator_type="image", locator="open_details_toggle.png")
        self.click_element(locator_type="image", locator="report_selector.png")
        # Verify the report page is opened
        self.wait_find_element(locator_type="image", locator="report_page_header.png")
