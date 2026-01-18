import shutil
import os


def copy_all_directory(from_path, to_path):
    if not os.path.exists(from_path):
        raise ValueError(f"From path {from_path} does not exist")

    if os.path.exists(to_path):
        print(f"Clearing destination directory {to_path}")
        shutil.rmtree(to_path)

    os.mkdir(to_path)

    content = os.listdir(from_path)
    for entry in content:
        full_path = os.path.join(from_path, entry)
        full_path_to = os.path.join(to_path, entry)
        if os.path.isfile(full_path):
            print(f"Copying file {full_path} to {full_path_to}")
            shutil.copy(full_path, full_path_to)
            print(f"File {entry} copied successfuly")
        else:
            print(f"Copying directory {full_path} to {full_path_to}")
            os.mkdir(full_path_to)
            copy_all_directory(full_path, full_path_to)
            print(f"Directory {entry} copied successfuly")
