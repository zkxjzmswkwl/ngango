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
        decorators=None
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
        decorators=None
    ):
        self._name = name
        self._parent_class = parent_class
        self._line_number = line_number
        self._methods = methods or []
        self._decorators = decorators

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
        return f'{self._name} | {self._methods}'

    def scan_methods(self, content: List[str], start_index: int):
        for i in range(start_index, len(content)):
            focused_line = content[i]
            possible_status_codes = []

            if 'status=' in focused_line:
                if focused_line.endswith(','):
                    code_str = focused_line \
                                .split('status=')[1].split(',')[0].strip()
                else:
                    code_str = focused_line \
                                .split('status=')[1].split(')')[0].strip()

                code = int(''.join(filter(str.isdigit, code_str)))
                possible_status_codes.append(code)

            indent = len(focused_line) - len(focused_line.lstrip())
            if indent == 0:
                continue

            if 'def' not in focused_line or indent != 4:
                continue

            method_name = focused_line.split('def')[1].split('(')[0].strip()
            does_exist = any(
                [method_name in method.name for method in self._methods]
            )
            if does_exist:
                continue

            arguments_str = focused_line.split('(')[1].split(')')[0]
            arguments = arguments_str.split(',')
            view_method = DjangoViewMethod(method_name,
                                           arguments,
                                           i,
                                           possible_status_codes)
            self._methods.append(view_method)


class DjangoModelField:
    def __init__(
        self,
        name: str,
        field_type: str,
        params=None
    ):
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
    def from_line(line: str) -> Optional['DjangoModelField']:
        """
        TODO: Very naive approach for now. Revisit.
        """
        def is_multiline(stripped_line: str) -> bool:
            return (stripped_line.endswith('(') or
                    stripped_line.endswith('[') or
                    stripped_line.endswith('{') or
                    stripped_line.endswith(',') or
                    stripped_line.endswith('\\'))

        def is_comment(line: str) -> bool:
            return line.startswith('#') or line.startswith('"""')

        stripped_line = line.strip()
        # * This means if you aren't `from django.db import models`,
        # * you're fucked. Revisit? Not sure if I care.
        if is_comment(stripped_line) or 'models.' not in line:
            return None

        # * multiline = is_multiline(line.strip())
        # TODO: Let's only handle non multiline for now. Feeling a bit lazy.
        # TODO: Also, again, I don't like the hacky splitting.
        # * Very error prone. Revisit.
        name = stripped_line.split('=')[0]
        field_type = stripped_line.split('=')[1].split('(')[0].strip()
        params = stripped_line.split('(')[1].split(')')[0].split(',')
        return DjangoModelField(name, field_type, params)

    def __str__(self):
        return f'{self._name} | {self._field_type} | {self._params}'


class DjangoModel:
    def __init__(
        self,
        name: str,
        line_number: int,
        fields: List[DjangoModelField],
        methods=None,
        properties=None,
        inherits_from='models.Model'
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
        return f'{self._name} | {self._fields}'


class DjangoApp:
    def __init__(self, name, path):
        self._name = name
        self._path = path
        self._models = []
        self._views = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    @property
    def models(self) -> List[DjangoModel]:
        return self._models

    @property
    def views(self) -> List[DjangoView]:
        return self._views

    def scan_models(self):
        full_path = f'{self.path}/models.py'
        print(f'Scanning {full_path}')

        file_handle = fs.get_file_handle(full_path, 'r')
        if not file_handle:
            print(f'[!] No models file found for {self.name}')
            return

        content = file_handle.readlines()
        for i, line in enumerate(content):
            if 'class' not in line:
                continue

            model_name = line.split(' ')[1].split('(')[0]
            print(f'Class at line {i} with name {model_name}')

            model_fields = []
            while True:
                i += 1
                if i >= len(content):
                    break

                focused_line = content[i]
                indent = len(focused_line) - len(focused_line.lstrip())
                if indent == 0:
                    break

                if model_field := DjangoModelField.from_line(focused_line):
                    model_fields.append(model_field)

            if len(model_fields) < 1:
                print(f'[!] No fields found for model {model_name}')
                continue

            model = DjangoModel(model_name, i, model_fields)
            self._models.append(model)

    def scan_views(self, views_filename: str):
        full_path = f'{self.path}/{views_filename}.py'
        print(f'Scanning {full_path}')

        file_handle = fs.get_file_handle(full_path, 'r')
        if not file_handle:
            print(f'[!] No views file found for {self.name}')
            return

        content = file_handle.readlines()
        for i, line in enumerate(content):
            if 'import' in line or ',' in line or len(line) < 8:
                continue

            is_class = False
            indent_level = len(line) - len(line.lstrip())

            if 'class' in line and indent_level == 0:
                is_class = True

            if is_class:
                view_name = line.split(' ')[1].split('(')[0]
                view_parent_class = line.split('(')[1].split(')')[0]
                if view_parent_class != 'APIView':
                    continue

                view = DjangoView(view_name, view_parent_class, i)
                view.scan_methods(content, i + 1)
                self._views.append(view)

        # ! Check for views in default location as well.
        # ! This behavior isn't ideal for most, should remove.
        if views_filename != 'views':
            new_path = full_path.replace(views_filename, 'views')
            file_handle = fs.get_file_handle(new_path, 'r')
            if file_handle is not None:
                self.scan_views('views')


class DjangoProject:
    def __init__(self, project_name: str, path: str, views_filename='views'):
        self._project_name = project_name
        self._path = path
        self._app_names = fs.folders_containing_file(self.path, 'models.py')
        self._apps = []
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
        settings_path = os.path.join(self.path, 'settings.py')
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
