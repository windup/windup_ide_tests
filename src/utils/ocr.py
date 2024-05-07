import logging
import re
import time

import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import ImageGrab


def find_all_string_occurrences(string):
    """
    Extract all occurrences of the string from the current screen content.
    """
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a numpy array and then to a format suitable for OpenCV
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # Preprocess the image
    processed_img = preprocess_image(screenshot_bgr)
    # Use pytesseract to extract text from the screenshot
    extracted_text = pytesseract.image_to_string(processed_img, config="--psm 6 -l eng")

    # Use a regular expression to find all occurrences of the substring
    return re.findall(re.escape(string), extracted_text)


def wait_for_element(image_path, timeout, threshold=0.8):
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        coordinates = find_on_screen(image_path, threshold)
        if coordinates:
            return coordinates
        time.sleep(1)
    logging.warning(f"Timeout reached. Element not found for {image_path}")
    return None


def find_on_screen(image_path, threshold=0.8):
    """
    Uses OpenCV to find the element on the screen based on the provided image path.
    Args:
        image_path (str): The path to the image file used as the template.
        threshold (float): The threshold for the match (default is 0.8).
    Returns:
        Coordinates x,y of the found element
    """
    screen = np.array(ImageGrab.grab())  # Take a screenshot
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        logging.error(f"Template image not loaded: {image_path}")
        return None
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        # Calculate the center of the template match
        top_left = max_loc
        w, h = template.shape[::-1]
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        return (center_x, center_y)
    return None


def find_all_sentence_occurrences(sentence):
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a numpy array and then to a format suitable for OpenCV
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # Preprocess the image
    processed_img = preprocess_image(screenshot_bgr)

    extracted_text = pytesseract.image_to_string(processed_img, config="--psm 6 -l eng")

    lines = extracted_text.split("\n")

    found_occurrences = [line for line in lines if sentence in line]

    return found_occurrences


def preprocess_image(img):
    """
    process the image to it becomes easier to extract text from
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)

    processed = cv2.resize(processed, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    return processed
