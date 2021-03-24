from RPA.Desktop import Desktop
import os
import src.lib.codereadystudio as codereadystudio


class BaseDesktop(Desktop):
    """
        Library for customizing the basic Desktop class
        functionalities adapted for generic usage
    """

    IMG_DIR = os.path.dirname(os.path.dirname(
        os.path.realpath(__file__)))+'/images'

    def image_locator(self, locator):
        """
        Forms image locator string

        Args:
            locator (str): Image name

        Returns:
            (str): Image locator string
        """
        if isinstance(self, codereadystudio.CodeReadyStudio):
            return f'image:{self.IMG_DIR}/codereadystudio/{locator}'

    def text_locator(self, locator):
        """
        Forms text locator string (ocr)

        Args:
            locator (str): Text name

        Returns:
            (str): Text locator string
        """
        return 'ocr:{}'.format(locator)

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
        return 'region:{},{},{},{}'.format(left, top, right, bottom)

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
        return '{}:{},{}'.format(locator_type, x_coordinate, y_coordinate)

    def _get_locator(self, locator_type, locator=None, coordinates=[]):
        """
        Forms and returns the actual locator based on type

        Args:
            locator_type (str): The type of locator
                                supported types-
                                text, image, offset, region, point, size
            locator (str): Locator string containing text or image name
            coordinates (list): List of integers

        Returns:
            formed_locator (str): Fully formed and formatted locator
        """
        valid_locator_types = ['text', 'image', 'offset',
                               'point', 'size', 'region']
        locator_type = locator_type.lower()
        if locator_type not in valid_locator_types:
            raise ValueError('Invalid locator type provided.\
                Must be one of {}'.format(valid_locator_types))

        if locator and coordinates:
            raise ValueError('Only one value out of locator or coordinates \
                must be provided !')

        if locator is None and len(coordinates) == 0:
            raise ValueError('Atleast one value out of locator \
                or coordinate must be provided !')

        if locator_type in ['offset', 'size', 'point', 'region']:
            if len(coordinates) == 0 or len(coordinates) == 1:
                raise ValueError('Atleast two integers must be provided to use \
                    offset, size or point locator')
            elif len(coordinates) == 2:
                return self.two_coordinate_locator(locator_type=locator_type,
                                                   x_coordinate=coordinates[0],
                                                   y_coordinate=coordinates[1])
            elif len(coordinates) == 4:
                return self.region_locator(left=coordinates[0],
                                           top=coordinates[1],
                                           right=coordinates[2],
                                           bottom=coordinates[3])
            else:
                raise ValueError('Invalid number of integers provided in \
                    coordinates list ! Either 2 or 4 values must be present.')

        if locator_type == 'image':
            return self.image_locator(locator)

        if locator_type == 'text':
            return self.text_locator(locator)

    def click_element(self, locator_type, locator=None,
                      coordinates=[], timeout=5.0):
        """
        Click an element after waiting for visibility
        of element located by image or text or any locator

        Args:
            locator_type (str): The type of locator
                                supported types-
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

    def wait_find_element(self, locator_type, locator=None,
                          coordinates=[], timeout=15.0, interval=0.5):
        """
        Wait untill timeout and find element based on locator

        Args:
            locator_type (str): The type of locator
                                supported types-
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
        self.wait_for_element(locator=formed_locator,
                              timeout=timeout, interval=interval)
        element_position = self.find_element(locator=formed_locator)
        return element_position
