import argparse
from core import DjangoProject
from tsgen.translator import ModelTranslator
from tsgen.typescript import ClassNode

# -n "project-name" --path "path_to_project_root" -v "views"


def main():
    p = argparse.ArgumentParser(
        description="Generate frontend using a DRF project as a schema."
    )

    p.add_argument("-n", "--name", type=str, help="The Django project name")
    p.add_argument("-p", "--path", type=str, help="The path to the Django project")
    p.add_argument(
        "-v",
        "--viewsfilename",
        type=str,
        help="The name of the file in which you keep views, no extension",
    )
    args = p.parse_args()

    project = DjangoProject(args.name, args.path, args.viewsfilename)
    project.propegate_apps()

    for app in project.apps:
        to_write = ""
        for model in app.models:
            translator = ModelTranslator(model)
            to_write += translator.translate() + "\n\n"

        file_path = f"../tsgen-output/{app.name.lower()}.struct.ts"
        with open(file_path, "w", encoding="utf8") as f:
            f.write(to_write)


if __name__ == "__main__":
    main()
