import time
import uuid

import cv2
import numpy
import pytesseract
from PIL import ImageGrab


def generate_uuid():
    return str(uuid.uuid4())


def write_data_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


def read_file(filename):
    with open(filename, "r") as file:
        contents = file.read()
    return contents

def extract_string_location(search_string):

    screenshot = ImageGrab.grab()

    screenshot_np = numpy.array(screenshot)
    gray_image = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    text_objects = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT)

    index = [index for index in range(len(text_objects['text'])) if text_objects['text'][index].lower() == search_string.lower()][0]
    x, y, w, h = text_objects['left'][index], text_objects['top'][index], text_objects['width'][index], text_objects['height'][index]
    return (x,y,w,h)


# def wait_extract_string_location(search_string, timeout=20, interval=2):
#
#     start_time = time.time()
#
#     while time.time() - start_time < timeout:
#         location = extract_string_location(search_string)
#         time.sleep(interval)


def search_sentence_on_screen(target_sentence):

    screenshot = ImageGrab.grab()
    screenshot_np = numpy.array(screenshot)
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    text_data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, config='--psm 6')

    current_line = 0

    for i in range(len(text_data['text'])):

        line_num = text_data['line_num'][i]

        if line_num < current_line:
            continue

        line_strings = [ text_data['text'][index] for index in range(len(text_data['text'])) if text_data['line_num'][index] == current_line]
        line_sentence = " ".join(line_strings)
        if target_sentence.lower() in line_sentence.lower():
            return True

        current_line += 1


def wait_for_sentence(target_sentence, timeout=20, interval=2):
    start_time = time.time()

    while time.time() - start_time < timeout:
        found = search_sentence_on_screen(target_sentence)
        if found:
            return
        time.sleep(interval)

    raise Exception (f"Time out, sentence [{target_sentence}] not found")