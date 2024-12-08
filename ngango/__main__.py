import argparse


def main():
    p = argparse.ArgumentParser(
        description="Generate frontend using a Django project as a schema.")

    p.add_argument(
        "-n",
        "--name",
        type=str,
        help="The Django project name"
    )
    p.add_argument(
        "-p",
        "--path",
        type=str,
        help="The path to the Django project"
    )

    args = p.parse_args()
    print(args.name, " : ", args.path)


if __name__ == "__main__":
    main()
