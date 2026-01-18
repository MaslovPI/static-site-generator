import sys
from fileoperations import copy_all_directory, generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1 and sys.argv[1]:
        basepath = sys.argv[1]

    copy_all_directory("static/", "docs/")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)


if __name__ == "__main__":
    main()
