import uuid
import subprocess
import re


def generate_uuid():
    return str(uuid.uuid4())


def write_data_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


def read_file(filename):
    with open(filename, "r") as file:
        contents = file.read()
    return contents

def get_screen_size():
    output = subprocess.check_output("xdpyinfo | grep dimensions", shell=True).decode()
    m = re.search(r"dimensions:\s+(\d+x\d+)", output)
    if m:
        return m.group(1)
    else:
        raise RuntimeError("Could not get screen size")