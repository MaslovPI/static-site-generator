from fileoperations import copy_all_directory, generate_pages_recursive


def main():
    copy_all_directory("static/", "public/")
    generate_pages_recursive("content/", "template.html", "public/")


if __name__ == "__main__":
    main()
