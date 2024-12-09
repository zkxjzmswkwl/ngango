import argparse
from core import DjangoProject
from tsgen.typescript import ClassNode

# -n "project-name" --path "path_to_project_root" -v "views"


def main():
    p = argparse.ArgumentParser(
        description="Generate frontend using a DRF project as a schema.")

    p.add_argument("-n", "--name", type=str, help="The Django project name")
    p.add_argument("-p",
                   "--path",
                   type=str,
                   help="The path to the Django project")
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
        print(app.name)
        print("Views")
        for view in app.views:
            print(f"\t{view.name}")
            for method in view.methods:
                print(f"\t\t{method.name}")

        print("Models")
        for model in app.models:
            print(f"\t{model.name}")
            for field in model.fields:
                print(f"\t\t{field.name}")

    user_service = ClassNode("UserService") \
        .add_decorator("Injectable()") \
        .add_property("users", "User[]", "private", "[]") \
        .add_method("addUser", "void", [("user", "User")], "this.users.push(user);") \
        .add_method("getUserById", "User | undefined", [("id", "number")], "return this.users.find(user => user.id === id);")

    with open("../tsgen-output/user.service.ts", "w", encoding="utf8") as f:
        f.write(user_service.to_ts())


if __name__ == "__main__":
    main()
