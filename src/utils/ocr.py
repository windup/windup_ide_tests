# import re
#
# import cv2
# import numpy as np
# import pyautogui
# import pytesseract


def find_all_string_occurrences(string):
    """
    Extract all occurrences of the string from the current screen content.
    """
    # screenshot = pyautogui.screenshot()
    #
    # # Convert the screenshot to a numpy array and then to a format suitable for OpenCV
    # screenshot_np = np.array(screenshot)
    # screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    #
    # # Preprocess the image
    # processed_img = preprocess_image(screenshot_bgr)
    # # Use pytesseract to extract text from the screenshot
    # extracted_text = pytesseract.image_to_string(processed_img, config="--psm 6 -l eng")
    #
    # # Use a regular expression to find all occurrences of the substring
    # return re.findall(re.escape(string), extracted_text)
    return 1


def find_all_sentence_occurrences(sentence):
    # screenshot = pyautogui.screenshot()
    #
    # # Convert the screenshot to a numpy array and then to a format suitable for OpenCV
    # screenshot_np = np.array(screenshot)
    # screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    #
    # # Preprocess the image
    # processed_img = preprocess_image(screenshot_bgr)
    #
    # extracted_text = pytesseract.image_to_string(processed_img, config="--psm 6 -l eng")
    #
    # lines = extracted_text.split("\n")
    #
    # found_occurrences = [line for line in lines if sentence in line]
    #
    # return found_occurrences

    return 1


def preprocess_image(img):
    """
    process the image to it becomes easier to extract text from
    """

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #
    # kernel = np.ones((1, 1), np.uint8)
    # processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
    #
    # processed = cv2.resize(processed, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    #
    # return processed

    return 1
