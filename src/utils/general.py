import csv
import uuid


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
        Asserts that the given CSV file is valid.
        A CSV file is considered valid if it exists and all of its rows have the same number of columns.

        Args:
            file_path (str): The file path of the CSV file to validate.
            **kwargs: Optional keyword arguments.
                delimiter (str): The delimiter used in the CSV file. Defaults to ','.

        Raises:
            AssertionError: If the CSV file does not exist or if its rows have different numbers of columns.

        Returns:
            None.
    """
    assert os.path.exists(csv_file_path) is True
    delimiter = kwargs.get('delimiter', ',')

    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        columns_number = len(next(csv_reader))
        assert all(len(row) == columns_number for row in csv_reader) is True