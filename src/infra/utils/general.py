import os
import shutil
import uuid
import zipfile

import requests


def download_file(url, save_path, file_name):
    response = requests.get(url)
    print(f"file path: {os.path.join(save_path, file_name)}")
    open(os.path.join(save_path, file_name), "wb").write(response.content)


def unzip_file(file_path, directory):
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(directory)


def clear_directory_by_name(directory, name_contains):
    for filename in os.listdir(directory):
        if name_contains in filename:
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, ignore_errors=True)
            except Exception as e:
                print("Failed to delete {}. Reason: {}".format(file_path, e))


def generate_project_input_paths(project_path, targets_sources):
    paths = []

    for target, source in targets_sources:
        paths.append(f"{project_path}/{target}/{source}/tests/data")
        # todo: make sure path exists before adding

    return paths


def generate_uuid():
    return uuid.uuid4()


def write_data_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


def read_file(filename):
    with open(filename, "r") as file:
        contents = file.read()
    return contents
