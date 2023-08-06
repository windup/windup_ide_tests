import pyautogui
from PIL import Image
import pytesseract
from pytesseract import Output
import pandas as pd


def find_all_string_occurrences(string_to_find):
    """
    Take a screenshot and search for a string in it, and return all the occurrences as a list of locations
    """

    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')

    data = pytesseract.image_to_data(Image.open('screenshot.png'), output_type=Output.DICT)

    df = pd.DataFrame(data)

    occurrences = df[df.text.str.contains(string_to_find, case=False, na=False)]

    return [{"x": occurrence.left, "y": occurrence.top} for index, occurrence in occurrences.iterrows()]

