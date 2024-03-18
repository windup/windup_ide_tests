import csv
import os
import random
import re
import shlex
import string
import subprocess
import uuid
from collections import defaultdict
from datetime import datetime
from datetime import timezone

import pyperclip
from lxml import html


def generate_vscode_id(part_length=9):
    chars = string.ascii_lowercase + string.digits
    part1 = "".join(random.choices(chars, k=part_length))
    part2 = "".join(random.choices(chars, k=part_length))
    custom_id = f"{part1}-{part2}"
    return custom_id


def generate_uuid():
    return str(uuid.uuid4())


def write_data_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


def read_file(filename):
    try:
        with open(filename, "r") as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None


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
    Parse the kantra cli string and returns a dictionary with keys as command flags.
    Flags without associated values are categorized under 'advanced_options'.
    """
    command_items = shlex.split(command)
    command_items = command_items[1:]
    cmd_map = defaultdict(list)
    last_was_flag = False
    checked_advanced_options = []
    current_flag = ""

    for item in command_items:
        if item.startswith("--"):
            if last_was_flag:
                checked_advanced_options.append(current_flag)
            current_flag = item[2:]
            last_was_flag = True
        else:
            if last_was_flag:
                cmd_map[current_flag].append(item)
                last_was_flag = False

    if last_was_flag:
        checked_advanced_options.append(current_flag)

    for key, value in list(cmd_map.items()):
        if isinstance(value, list) and len(value) == 1:
            cmd_map[key] = value[0]

    if checked_advanced_options:
        cmd_map["advanced_options"] = checked_advanced_options

    return dict(cmd_map)


def is_date_today(date: str):
    date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
    extracted_date = date_object.astimezone(timezone.utc).replace(tzinfo=None)
    today = datetime.now(timezone.utc).date()

    return extracted_date.date() == today


def file_exists(file_path):
    """
    Checks if a file exists at the given path.
    """
    return os.path.exists(file_path)


def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)

    if result.returncode != 0:
        raise Exception(f"failed to run command {command},\n {result.stderr}")

    return result.stdout
