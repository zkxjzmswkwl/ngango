import os
import argparse
from core import DjangoProject
from config import Config
from tsgen.translator import ModelTranslator, ServiceTranslator
from tsgen.typescript import ClassNode

# -n "project-name" --path "path_to_project_root" -v "views"


def main():
    p = argparse.ArgumentParser(
        description="Generate frontend using a DRF project as a schema."
    )

    p.add_argument("-n", "--name", type=str, help="The Django project name")
    p.add_argument("-p", "--path", type=str, help="The path to the Django project")
    p.add_argument("-v",
                   "--viewsfilename",
                   type=str,
                   help="The name of the file in which you keep views, no extension",)
    p.add_argument("-c",
                   "--config",
                   type=str,
                   help="The path to the config file")
    args = p.parse_args()

    config = Config(args.config)
    project = DjangoProject(args.name, args.path, args.viewsfilename)
    project.propegate_apps()

    # crude testing
    for app in project.apps:
        to_write = ""
        for model in app.models:
            translator = ModelTranslator(model)
            to_write += translator.translate() + "\n"

        # e.g src/app/models
        relative_folder = config.output_destinations.get("models")
        # Check if folder exists
        if not os.path.isdir(f"{config.frontend_path}/{relative_folder}"):
            os.makedirs(f"{config.frontend_path}/{relative_folder}")

        if relative_folder:
            with open(
                f"{config.frontend_path}/{relative_folder}/{app.name.lower()}.struct.ts",
                "w",
                encoding="utf8"
            ) as f:
                f.write(to_write)

        to_write = ""

        service_translator = ServiceTranslator(app,
                                               injectable=True,
                                               use_store=False)
        to_write += service_translator.translate() + "\n"
        # e.g src/app/services
        relative_folder = config.output_destinations.get("services")
        # Check if folder exists
        if not os.path.isdir(f"{config.frontend_path}/{relative_folder}"):
            os.makedirs(f"{config.frontend_path}/{relative_folder}")

        if relative_folder:
            with open(
                f"{config.frontend_path}/{relative_folder}/{app.name.lower()}.service.ts",
                "w",
                encoding="utf8"
            ) as f:
                f.write(to_write)

        # with open(
        #     f"../tsgen-output/{app.name.lower()}.service.ts", "w",
        #     encoding="utf8"
        # ) as f:
        #     f.write(to_write)


if __name__ == "__main__":
    main()
