import csv
import os
import re
import shlex
import subprocess
import uuid
from collections import defaultdict

import pyperclip
from lxml import html


def generate_uuid():
    return str(uuid.uuid4())


def write_data_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


def read_file(filename):
    with open(filename, "r") as file:
        contents = file.read()
    return contents


def assert_valid_csv_file(file_path, **kwargs):
    """
    Asserts that the given .csv file is valid.
    A CSV file is considered valid if  all of its rows have the same number of columns.
    """
    assert os.path.exists(file_path) is True
    delimiter = kwargs.get("delimiter", ",")

    with open(file_path, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        columns_number = len(next(csv_reader))
        assert all(len(row) == columns_number for row in csv_reader) is True


def find_elements_in_html_file(html_file_path, xpath):
    if not os.path.exists(html_file_path):
        raise Exception(f"File [{html_file_path}] does not exist!")

    with open(html_file_path, "r", encoding="utf-8") as html_file:
        content = html_file.read()

    tree = html.fromstring(content)

    elements = tree.xpath(xpath)

    if elements is None:
        raise Exception(f"No element found with xpath: [{xpath}]")

    return elements


def delete_directory(file_name):
    subprocess.run(
        f"rm -rf {file_name}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def get_screen_size():
    output = subprocess.check_output("xdpyinfo | grep dimensions", shell=True).decode()
    m = re.search(r"dimensions:\s+(\d+x\d+)", output)
    if m:
        return m.group(1)
    else:
        raise RuntimeError("Could not get screen size")


def get_clipboard_text(split=False):
    """Returns the text currently copied in the clipboard."""
    try:
        text = pyperclip.paste().split("\n") if split else pyperclip.paste()
        return text
    except pyperclip.PyperclipException as e:
        print(f"Error accessing clipboard: {e}")
        return []


def parse_log_string(log_string):
    pattern = re.compile(r'(\w+)=("[^"]*"|\S+)')
    match_list = pattern.findall(log_string)
    log_map = {key: value.strip('"') for key, value in match_list}

    return log_map


def parse_kantra_cli_command(command):
    """
    Parses a command string and returns a dictionary with keys as command flags
    and values as the flag's arguments. Flags that appear multiple times are aggregated into a list.

    Args:
    - command (str): The command string to parse.

    Returns:
    - dict: A dictionary with command flags as keys and their arguments as values.
    """
    # Split the command into parts using shlex to properly handle spaces
    parts = shlex.split(command)

    # Skip the first part (command itself)
    parts = parts[1:]

    cmd_map = defaultdict(list)

    # Track whether the last part was a flag to handle flags without values
    last_was_flag = False

    for part in parts:
        if part.startswith('--'):
            # Current part is a flag; strip '--' and prepare to collect its value(s)
            current_flag = part[2:]
            last_was_flag = True
        else:
            if last_was_flag:
                # Current part is a value for the last flag
                cmd_map[current_flag].append(part)
                last_was_flag = False
            # If the part is not a flag and last_was_flag is False,
            # it's a continuation of values, so already handled above

    # Convert lists to single values where appropriate
    for key, value in cmd_map.items():
        if len(value) == 1:
            cmd_map[key] = value[0]

    return dict(cmd_map)
