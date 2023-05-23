import os
import subprocess
import uuid

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
