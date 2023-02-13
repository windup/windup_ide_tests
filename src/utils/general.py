import requests
import os
import zipfile
import shutil

def download_file(url, save_path, file_name):
    response = requests.get(url)
    print(f"file path: {os.path.join(save_path, file_name)}")
    open(os.path.join(save_path, file_name), "wb").write(response.content)


def unzip_file(file_path, directory):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
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
                print('Failed to delete %s. Reason: %s' % (file_path, e))
