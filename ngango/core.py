import ast
import os
from typing import List, Optional
import file_service as fs


class DjangoViewMethod:

    def __init__(
        self,
        name: str,
        arguments: List[str],
        line_number: int,
        status_codes=None,
        decorators=None,
    ):
        self._name = name
        self._arguments = arguments
        self._line_number = line_number
        self._status_codes = status_codes
        self._decorators = decorators

    @property
    def name(self) -> str:
        return self._name

    @property
    def arguments(self) -> List:
        return self._arguments

    @property
    def line_number(self) -> int:
        return self._line_number

    @property
    def status_codes(self) -> List:
        return self._status_codes

    @property
    def decorators(self) -> List:
        return self._decorators


class DjangoView:

    def __init__(
        self,
        name: str,
        parent_class: str,
        line_number: int,
        methods=None,
        decorators=None,
    ):
        self._name = name
        self._parent_class = parent_class
        self._line_number = line_number
        self._methods = methods or []
        self._decorators = decorators or []

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent_class(self) -> str:
        return self._parent_class

    @property
    def line_number(self) -> int:
        return self._line_number

    @property
    def methods(self) -> List:
        return self._methods

    @property
    def decorators(self) -> List:
        return self._decorators

    def __str__(self):
        return f"{self._name} | {self._methods}"

    def scan_methods(self, node: ast.ClassDef):
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                method_name = child.name
                arguments = [arg.arg for arg in child.args.args]
                status_codes = []

                for stmt in ast.walk(child):
                    if isinstance(stmt, ast.Assign) and isinstance(
                            stmt.value, ast.Constant):
                        if (hasattr(stmt.targets[0], "id")
                                and stmt.targets[0].id == "status"):
                            status_codes.append(stmt.value.value)

                method = DjangoViewMethod(method_name, arguments, child.lineno,
                                          status_codes)
                self._methods.append(method)

    @staticmethod
    def from_ast(node: ast.ClassDef):
        if not any((isinstance(base, ast.Name) and base.id == "APIView") or
                   (isinstance(base, ast.Attribute) and base.attr == "APIView")
                   for base in node.bases):
            return None

        # Unused for now
        # methods = []
        decorators = []

        for child in node.decorator_list:
            if isinstance(child, ast.Name):
                decorators.append(child.id)
            elif isinstance(child, ast.Call) and hasattr(child.func, "id"):
                decorators.append(child.func.id)

        if isinstance(node.bases[0], ast.Name):
            view = DjangoView(node.name,
                              node.bases[0].id,
                              node.lineno,
                              decorators=decorators)
            view.scan_methods(node)
            return view


class DjangoModelField:

    def __init__(self, name: str, field_type: str, params=None):
        self._name = name
        self._field_type = field_type
        self._params = params

    @property
    def name(self) -> str:
        return self._name

    @property
    def field_type(self) -> str:
        return self._field_type

    @property
    def params(self) -> List:
        return self._params

    @staticmethod
    def from_line(line: str) -> Optional["DjangoModelField"]:
        """
        TODO: Very naive approach for now. Revisit.
        """

        def is_multiline(stripped_line: str) -> bool:
            return (stripped_line.endswith("(") or stripped_line.endswith("[")
                    or stripped_line.endswith("{")
                    or stripped_line.endswith(",")
                    or stripped_line.endswith("\\"))

        def is_comment(line: str) -> bool:
            return line.startswith("#") or line.startswith('"""')

        stripped_line = line.strip()
        # * This means if you aren't `from django.db import models`,
        # * you're fucked. Revisit? Not sure if I care.
        if is_comment(stripped_line) or "models." not in line:
            return None

        # * multiline = is_multiline(line.strip())
        # TODO: Let's only handle non multiline for now. Feeling a bit lazy.
        # TODO: Also, again, I don't like the hacky splitting.
        # * Very error prone. Revisit.
        name = stripped_line.split("=")[0]
        field_type = stripped_line.split("=")[1].split("(")[0].strip()
        params = stripped_line.split("(")[1].split(")")[0].split(",")
        return DjangoModelField(name, field_type, params)

    def __str__(self):
        return f"{self._name} | {self._field_type} | {self._params}"


class DjangoModel:

    def __init__(
        self,
        name: str,
        line_number: int,
        fields: List[DjangoModelField],
        methods=None,
        properties=None,
        inherits_from="models.Model",
    ):
        self._name = name
        self._line_number = line_number
        self._fields = fields
        self._methods = methods
        self._properties = properties
        self._inherits_from = inherits_from

    @property
    def name(self) -> str:
        return self._name

    @property
    def line_number(self) -> int:
        return self._line_number

    @property
    def fields(self) -> List:
        # TODO: -> List[Field]
        return self._fields

    @property
    def methods(self) -> List:
        return self._methods

    @property
    def properties(self) -> List:
        return self._properties

    @property
    def inherits_from(self) -> str:
        return self._inherits_from

    def __str__(self):
        return f"{self._name} | {self._fields}"


class DjangoApp:
    """
    Likely broken.
    """

    def __init__(self, name, path):
        self._name = name
        self._path = path
        self._models = []
        self._views = []

    @property
    def name(self) -> str:
        """
        App name.
        """
        return self._name

    @property
    def path(self) -> str:
        """
        The path to this app's folder.
        """
        return self._path

    @property
    def models(self) -> List[DjangoModel]:
        """
        List of DjangoModel objects.
        """
        return self._models

    @property
    def views(self) -> List[DjangoView]:
        """
        List of DjangoView objects.
        """
        return self._views

    def _extract_models(self, tree):
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            if any(
                (isinstance(base, ast.Name) and base.id == "models.Model") or (
                    isinstance(base, ast.Attribute) and base.attr == "Model")
                    for base in node.bases):
                fields = [
                    DjangoModelField(child.targets[0].id,
                                     child.value.func.attr)
                    for child in node.body if isinstance(child, ast.Assign)
                    and isinstance(child.value, ast.Call)
                    and hasattr(child.value.func, "attr")
                ]
                self._models.append(DjangoModel(node.name,
                                                node.lineno,
                                                fields))

    def _extract_views(self, tree: ast.Module):
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            view = DjangoView.from_ast(node)
            if view:
                self._views.append(view)

    def _scan_file(self, filename, extractor):
        full_path = os.path.join(self._path, filename)
        try:
            with open(full_path) as f:
                tree = ast.parse(f.read())
                extractor(tree)
        except FileNotFoundError:
            print(f"[!] {filename} not found for {self._name}")

    def scan_models(self):
        self._scan_file("models.py", self._extract_models)

    def scan_views(self, views_filename):
        self._scan_file(f"{views_filename}.py", self._extract_views)


class DjangoProject:

    def __init__(self, project_name: str, path: str, views_filename="views"):
        self._project_name = project_name
        self._path = path
        self._app_names = fs.folders_containing_file(self.path, "models.py")
        self._apps: List[DjangoApp] = []
        self._views_filename = views_filename

    @property
    def project_name(self):
        return self._project_name

    @property
    def path(self):
        return self._path

    @property
    def app_names(self) -> List[str]:
        return self._app_names

    @property
    def apps(self) -> List[DjangoApp]:
        return self._apps

    def get_settings(self):
        settings_path = os.path.join(self.path, "settings.py")
        with open(settings_path) as f:
            return f.read()

    def propegate_apps(self):
        for app_name in self.app_names:
            dj_app = DjangoApp(app_name, os.path.join(self.path, app_name))
            self._apps.append(dj_app)

        # ! Scan for models
        [app.scan_models() for app in self._apps]

        # ! Scan for endpoints
        [app.scan_views(self._views_filename) for app in self._apps]

        # ! Link endpoints -> urls

        # ! Scan for serializers (fuck)
