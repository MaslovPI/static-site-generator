import os
import shutil

from mdoperations import extract_title, markdown_to_html_node


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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = get_file_content(from_path)
    template = get_file_content(template_path)
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    content = template.replace("{{ Title }}", title)
    content = content.replace("{{ Content }}", html)
    update_file_content(dest_path, content)


def get_file_content(path):
    with open(path) as f:
        return f.read()


def update_file_content(path, content):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
