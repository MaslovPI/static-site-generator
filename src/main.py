from fileoperations import copy_all_directory, generate_page


def main():
    copy_all_directory("static/", "public/")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
