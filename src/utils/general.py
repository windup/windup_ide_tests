import uuid


def generate_project_input_paths(project_path, sources, targets):
    paths = []

    for source, target in zip(sources, targets):
        paths.append(f"{project_path}/rules/rules-reviewed/{target}/{source}/tests/data")
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
