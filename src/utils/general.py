import os
import shutil


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
