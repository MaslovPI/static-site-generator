from fileoperations import copy_all_directory


def main():
    copy_all_directory("static/", "public/")


if __name__ == "__main__":
    main()
