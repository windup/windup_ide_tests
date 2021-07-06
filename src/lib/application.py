import logging
import os
import re

from RPA.Desktop import Desktop
from src.lib.config import config_data


class Application(Desktop):
    """
        Library for customizing the basic Desktop class
        functionalities adapted for generic usage
    """

    IMG_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/images"

    def image_locator(self, locator):
        """
        Forms image locator string

        Args:
            locator (str): Image name

        Returns:
            (str): Image locator string
        """
        if isinstance(self, CodeReadyStudio) or isinstance(self, Eclipse):
            return f"image:{self.IMG_DIR}/codeready_eclipse_common/{locator}"

        if isinstance(self, VisualStudioCode):
            return f"image:{self.IMG_DIR}/vscode/{locator}"

        if isinstance(self, Intellij):
            return f"image:{self.IMG_DIR}/intellij/{locator}"

    def text_locator(self, locator):
        """
        Forms text locator string (ocr)

        Args:
            locator (str): Text name

        Returns:
            (str): Text locator string
        """
        return "ocr:{}".format(locator)

    def region_locator(self, left, top, right, bottom):
        """
        Forms region locator string

        Args:
            left (int): left coordinate
            top (int): top coordinate
            right (int): right coordinate
            bottom (int): bottom coordinate

        Returns:
            (str): Region locator string
        """
        return "region:{},{},{},{}".format(left, top, right, bottom)

    def two_coordinate_locator(self, locator_type, x_coordinate, y_coordinate):
        """
        Forms locator string for size/pointer/offset

        Args:
            locator_type (str): Type of locator among
                                size, point, offset
            x_coordinate (int): pixel coordinate as position
            y_coordinate (int): pixel coordinate as position

        Returns:
            (str): Size/point/offset locator string
        """
        return "{}:{},{}".format(locator_type, x_coordinate, y_coordinate)

    def _get_locator(self, locator_type, locator=None, coordinates=[]):
        """
        Forms and returns the actual locator based on type

        Args:
            locator_type (str): Valid values for locator_type -
                                text, image, offset, region, point, size
            locator (str): Locator string containing text or image name
            coordinates (list): List of integers

        Returns:
            formed_locator (str): Fully formed and formatted locator
        """
        valid_locator_types = [
            "text",
            "image",
            "offset",
            "point",
            "size",
            "region",
        ]
        locator_type = locator_type.lower()
        if locator_type not in valid_locator_types:
            raise ValueError(
                "Invalid locator type provided.\
                Must be one of {}".format(
                    valid_locator_types,
                ),
            )

        if locator and coordinates:
            raise ValueError(
                "Only one value out of locator or coordinates \
                must be provided !",
            )

        if locator is None and len(coordinates) == 0:
            raise ValueError(
                "Atleast one value out of locator \
                or coordinate must be provided !",
            )

        if locator_type in ["offset", "size", "point", "region"]:
            if len(coordinates) == 0 or len(coordinates) == 1:
                raise ValueError(
                    "Atleast two integers must be provided to use \
                    offset, size or point locator",
                )
            elif len(coordinates) == 2:
                return self.two_coordinate_locator(
                    locator_type=locator_type,
                    x_coordinate=coordinates[0],
                    y_coordinate=coordinates[1],
                )
            elif len(coordinates) == 4:
                return self.region_locator(
                    left=coordinates[0],
                    top=coordinates[1],
                    right=coordinates[2],
                    bottom=coordinates[3],
                )
            else:
                raise ValueError(
                    "Invalid number of integers provided in \
                    coordinates list ! Either 2 or 4 values must be present.",
                )

        if locator_type == "image":
            return self.image_locator(locator)

        if locator_type == "text":
            return self.text_locator(locator)

    def click_element(self, locator_type, locator=None, coordinates=[], timeout=5.0):
        """
        Click an element after waiting for visibility
        of element located by image or text or any locator

        Args:
            locator_type (str): Valid values for locator_type -
                                text, image, offset, region, point, size
            locator (str): Locator string containing text or image name
            coordinates (list): List of integers provided as
                                x and y coordinates for point or offset locator
                                width and height for size locator
                                left, top, right, bottom for region locator
            timeout (float): Timeout in seconds

        Returns:
            None
        """
        formed_locator = self._get_locator(locator_type, locator, coordinates)
        self.wait_for_element(locator=formed_locator, timeout=timeout)
        self.click(locator=formed_locator)

    def wait_find_element(
        self, locator_type, locator=None, coordinates=[], timeout=15.0, interval=0.5,
    ):
        """
        Wait untill timeout and find element based on locator

        Args:
            locator_type (str): Valid values for locator_type -
                                text, image, offset, region, point, size
            locator (str): Locator string containing text or image name
            coordinates (list): List of integers provided as
                                x and y coordinates for point or offset locator
                                width and height for size locator
                                left, top, right, bottom for region locator
            timeout (float): Timeout value in seconds
            interval (float): Periodic interval in seconds

        Returns:
            element_position (str): Coordinates of element position on screen
        """
        formed_locator = self._get_locator(locator_type, locator, coordinates)
        self.wait_for_element(locator=formed_locator, timeout=timeout, interval=interval)
        element_position = self.find_element(locator=formed_locator)
        return element_position

    def close_ide(self):
        """
        Closes the IDE
        """
        self.click_element(locator_type="text", locator="File")
        self.click_element(locator_type="text", locator="Exit")

    def is_open_mta_perspective(self):
        """
        Checks if MTA perspective is already opened in IDE

        Returns:
            (bool): True or False
        """
        try:
            self.wait_find_element(locator_type="image", locator="mta_perspective.png")
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
        Opens MTA perspective in IDE

        Steps:
            1) Click on Window menu item
            2) Click Perspective from dropdown menu
            3) Click on Open Perspective
            4) Select Other and then click MTA
            5) Click on Open button
        """
        if self.is_open_mta_perspective():
            logging.info("MTA perspective is already opened !")
            return
        else:
            self.click_element(locator_type="text", locator="Window")
            self.click_element(locator_type="text", locator="Perspective")
            self.click_element(locator_type="image", locator="open_perspective.png")
            try:
                self.click_element(locator_type="text", locator="Other...")
            except Exception as exc:
                # Re-attempt to click 'Other' using image locator
                if "No matches found" in str(exc):
                    self.click_element(locator_type="image", locator="other_alt.png")
                else:
                    raise Exception(exc)
            self.click_element(locator_type="image", locator="open_perspective_header.png")
            self.type_text(text="mta")
            open_perspective_button = self.image_locator("open_button.png")
            self.move_mouse(open_perspective_button)
            self.click(action="double_click")

    def run_simple_analysis(self, project, packages=[]):
        """
        Runs analysis by adding the project and/or packages passed as argument

        Args:
            project (str): Full name of project to be analysed
            packages (list): List of packages to be added to analysis

        Returns:
            None

        Steps:
            1) Click on Run MTA Configuration icon
            2) Click Add Project button
            3) Type Project name
            4) Click on OK button
            5) Confirm analysis has started
        """
        self.click_element(locator_type="image", locator="mta_run.png")
        self.click_element(locator_type="image", locator="run_conf_header.png")
        # Get the multiple Add Project Buttons and select first one
        add_button_locator = self.image_locator("add_button.png")
        add_buttons = self.find_elements(add_button_locator)
        self.click(locator=add_buttons[0])
        self.click_element(locator_type="image", locator="projects_header.png")
        self.type_text(text=project, enter=True)
        # Disable generate report from options
        self.click_element(locator_type="text", locator="Options")
        self.click_element(locator_type="image", locator="generate_report_checkbox.png")
        self.click_element(locator_type="image", locator="run_config_button.png")
        self.wait_find_element(locator_type="image", locator="generating_report.png")
        self.wait_find_element(
            locator_type="image", locator="run_complete.png", timeout=120.0, interval=5.0,
        )

    def is_analysis_complete(self):
        """
        Checks if run analysis has been completed

        Returns:
            (bool): True if analysis was completed
        """
        self.wait_find_element(
            locator_type="image", locator="run_complete.png", timeout=120.0, interval=5.0,
        )
        return True


class CodeReadyStudio(Application):
    """
    Class for managing RH Code Ready Studio application
    """

    pass


class Eclipse(Application):
    """
    Class for managing Eclipse application
    """

    pass


class VisualStudioCode(Application):
    """
    Class for managing VSCode application
    """

    def close_ide(self):
        """
        Closes the IDE
        """
        self.press_keys("ctrl", "q")

    def is_open_mta_perspective(self):
        """
        Checks if MTA perspective is already opened in VS Code

        Returns:
            (bool): True or False
        """
        try:
            self.wait_find_element(locator_type="image", locator="mta_config_active.png")
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
            self.click_element(locator_type="image", locator="mta_config_view.png")

    def run_simple_analysis(self, project, packages=[]):
        """
        Runs analysis by adding the project and/or packages passed as argument

        Args:
            project (str): Full name of project to be analysed
            packages (list): List of packages to be added to analysis

        Returns:
            None

        Steps:
            1) Click on MTA Configuration icon
            2) Click new config(+) icon
            3) Type project name in source
            4) Right click on config name and run
            5) Confirm analysis has started
        """
        self.wait_find_element(locator_type="image", locator="create_new_config.png")
        self.click_element(locator_type="image", locator="create_new_config.png")
        self.wait_find_element(locator_type="image", locator="config_screen.png")
        # Region defining the configuration name
        config_name_region = self.define_region(707, 222, 1167, 271)
        config_name = self.read_text(locator=config_name_region, invert=True)
        add_project_locator = self.image_locator("add_project_button.png")
        add_project_buttons = self.find_elements(add_project_locator)
        # Click the first match out of the two same buttons found
        self.click(add_project_buttons[0])
        self.type_text(text=project, enter=True)
        config_run_region = self.two_coordinate_locator(
            locator_type="point", x_coordinate=110, y_coordinate=870,
        )
        self.click(config_run_region)
        self.type_text(config_name)
        run_config_locator = self.image_locator("run_config_highlighter.png")
        # Find config name highlighted and select correct config if multiple matches are found
        try:
            self.wait_find_element(locator_type="image", locator="run_config_highlighter.png")
            self.move_mouse(run_config_locator)
        except Exception as exc:
            if re.match(r"Found [0-9] matches+", str(exc)):
                run_config_matches = self.find_elements(run_config_locator)
                self.move_mouse(run_config_matches[-1])
            else:
                raise Exception(exc)
        self.click(action="right_click")
        self.press_keys("up")
        self.press_keys("enter")
        self.wait_find_element(locator_type="image", locator="analysis_progress.png", timeout=90.0)
        self.wait_find_element(locator_type="image", locator="analysis_complete.png", timeout=120.0)

    def is_analysis_complete(self):
        """
        Checks if run analysis has been completed

        Returns:
            (bool): True if analysis was completed
        """
        self.wait_find_element(locator_type="image", locator="analysis_complete.png", timeout=120.0)
        return True


class Intellij(Application):
    """
    Class for managing IntelliJ application
    """

    def close_ide(self):
        """
        Closes the IDE
        """
        self.click_element(locator_type="image", locator="file_menu.png")
        self.click_element(locator_type="text", locator="Exit")
        try:
            self.wait_find_element(locator_type="image", locator="confirm_exit.png", timeout=5.0)
            self.click_element(locator_type="image", locator="exit_button.png")
        except Exception:
            logging.info("No exit confirmation dialog found !")

    def is_open_mta_perspective(self):
        """
        Checks if MTA perspective is already opened in Intellij

        Returns:
            (bool): True or False
        """
        try:
            self.wait_find_element(locator_type="image", locator="mta_perspective_active.png")
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
        Opens MTA perspective in Intellij
        """
        if self.is_open_mta_perspective():
            logging.info("MTA perspective is already opened !")
            return
        else:
            # Click on the MTA tab in left sidebar
            self.click_element(locator_type="image", locator="mta_tab.png")

    def run_simple_analysis(self, project, packages=[]):
        """
        Runs analysis by adding the project and/or packages passed as argument

        Args:
            project (str): Full name of project to be analysed
            packages (list): List of packages to be added to analysis

        Returns:
            None

        Steps:
            1) Click on MTA Configuration icon
            2) Click new config(+) icon
            3) Type project name in source
            4) Right click on config name and run
            5) Confirm analysis has started
        """
        config_create_region = self.two_coordinate_locator(
            locator_type="point", x_coordinate=110, y_coordinate=370,
        )
        self.click(config_create_region)
        self.click(action="right_click")
        self.press_keys("down")
        self.press_keys("enter")
        self.wait_find_element(locator_type="image", locator="mta_config_page_opened.png")
        # Region defining the configuration name
        config_name_region = self.define_region(705, 222, 1167, 271)
        config_name = self.read_text(locator=config_name_region, invert=True)
        self.click_element(locator_type="image", locator="mta_cli_input.png")
        self.type_text(config_data["mta_cli_path"])
        self.press_keys("page_down")
        add_project_locator = self.image_locator("add_project_button.png")
        add_project_buttons = self.find_elements(add_project_locator)
        # Click the first match out of the two same buttons found
        self.click(add_project_buttons[1])
        self.type_text(text=project, enter=True)
        self.click_element(locator_type="image", locator="add_project_button.png")
        self.type_text(text="eap", enter=True)
        config_run_region = self.two_coordinate_locator(
            locator_type="point", x_coordinate=110, y_coordinate=870,
        )
        self.click(config_run_region)
        self.type_text(config_name)

        # run_config_locator = self.image_locator("run_config_highlighter.png")
        # # Find config name highlighted and select correct config if multiple matches are found
        # try:
        #     self.wait_find_element(locator_type="image", locator="run_config_highlighter.png")
        #     self.move_mouse(run_config_locator)
        # except Exception as exc:
        #     if re.match(r"Found [0-9] matches+", str(exc)):
        #         run_config_matches = self.find_elements(run_config_locator)
        #         self.move_mouse(run_config_matches[-1])
        #     else:
        #         raise Exception(exc)
        # self.click(action="right_click")
        # self.press_keys("up")
        # self.press_keys("enter")
        # self.wait_find_element(locator_type="image", locator="analysis_progress.png", timeout=90.0)
        # self.wait_find_element(locator_type="image", locator="analysis_complete.png", timeout=120.0)
