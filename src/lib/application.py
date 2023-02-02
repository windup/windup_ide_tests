import logging
import os
import re

from RPA.Desktop import Desktop

from src.lib.IDE.CodeReadyStudio import CodeReadyStudio
from src.lib.IDE.Eclipse import Eclipse
from src.lib.IDE.Intellij import Intellij
from src.lib.IDE.VisualStudioCode import VisualStudioCode


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
        return 'ocr:"{}"'.format(locator)

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
        self,
        locator_type,
        locator=None,
        coordinates=[],
        timeout=15.0,
        interval=0.5,
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

    def close_report_tab(self):
        """
        Closes the current browser tab having report opened in it
        """
        pass
        # Need to write logic to handle browser window, when single tab is only open
        # self.press_keys("ctrl", "w")

    def switch_tab(self):
        """
        Switch context between apps using home+tab buttons
        """
        self.press_keys("alt", "tab")

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

    def run_simple_analysis(self, project, migration_target, packages=[]):
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
            5) Select the target technology
            6) Confirm analysis has started
        """
        self.click_element(locator_type="image", locator="mta_run.png")
        self.click_element(locator_type="image", locator="run_conf_header.png")
        # Get the multiple Add Project Buttons and select first one
        add_button_locator = self.image_locator("add_button.png")
        add_buttons = self.find_elements(add_button_locator)
        self.click(locator=add_buttons[0])
        self.click_element(locator_type="image", locator="projects_header.png")
        self.type_text(text=project, enter=True)
        # Ensure that Anything to EAP 7 is selected in migration path
        self.click_element(locator_type="image", locator="target_dropdown.png")
        self.click()
        for i in range(0, 15):
            self.press_keys("up")
        # Select target, by opening options
        self.click_element(locator_type="text", locator="Options")
        self.click_element(locator_type="image", locator="add_button.png")
        self.click_element(locator_type="image", locator="target_dropdown.png")
        # Select "target" option from dropdown as key
        self.click_element(locator_type="text", locator="target")
        # Select the target based on its position in dropdown
        self.click_element(locator_type="image", locator="target_value_dropdown.png")
        self.click()
        target_position = 0
        try:
            if migration_target == "eap7":
                target_position = 6
            elif migration_target == "eapxp":
                target_position = 7
            elif migration_target == "quarkus1":
                target_position = 18
            else:
                logging.debug("Unknown migration target selected !")
                raise Exception()
            self.select_target(target_position)
        except Exception as exc:
            logging.debug(str(exc))
            raise Exception(exc)
        self.click_element(locator_type="image", locator="ok_button.png")
        self.click_element(locator_type="image", locator="run_config_button.png")
        try:
            self.wait_find_element(locator_type="image", locator="generating_report.png")
        except Exception as exc:
            if re.match(r"Found [0-9] matches+", str(exc)):
                logging.debug("Detected the start of analysis")
            else:
                raise Exception(exc)
        self.wait_find_element(
            locator_type="image",
            locator="report_page_header.png",
            timeout=120.0,
            interval=1.0,
        )

    def is_analysis_complete(self):
        """
        Checks if run analysis has been completed

        Returns:
            (bool): True if analysis was completed
        """
        try:
            self.wait_find_element(
                locator_type="image",
                locator="report_page_header.png",
                timeout=120.0,
                interval=5.0,
            )
            return True
        except Exception:
            return False

    def verify_story_points(self, target):
        """
        Verifies the story points in report after analysis

        Returns:
            (bool): True if story points were accurate
        """
        if target == "eap7":
            story_point_locator = "eap7_story_points.png"
        elif target == "quarkus":
            story_point_locator = "quarkus_story_points.png"
        elif target == "eapxp":
            story_point_locator = "eapxp_story_points.png"
        else:
            logging.debug("Unknown target provided !")
            raise Exception()
        try:
            self.wait_find_element(locator_type="image", locator=story_point_locator)
            return True
        except Exception as exc:
            logging.debug(str(exc))
            return False
        finally:
            self.switch_tab()

    def select_target(self, position):
        """
        Press down arrow key to select appropriate migration target from dropdown

        Args:
            position(int): The position of target in drop down
        """
        for i in range(0, position):
            self.press_keys("down")
