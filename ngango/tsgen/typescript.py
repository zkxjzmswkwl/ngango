class TSNode:

    def __init__(self, name):
        self.name = name

    def to_ts(self) -> str:
        raise NotImplementedError("Subclasses must implement this method.")


class InterfaceNode(TSNode):

    def __init__(self, name):
        super().__init__(name)
        self._properties = []

    @property
    def properties(self):
        return self._properties

    def add_property(self, name, type_, optional=False):
        self._properties.append({
            "name": name,
            "type": type_,
            "optional": optional
        })
        return self

    def to_ts(self) -> str:
        properties_str = "\n".join(
            f"  {prop['name']}{'?' if prop['optional'] else ''}: {prop['type']};"
            for prop in self._properties
        )
        return f"export interface {self.name} {{\n{properties_str}\n}}"


class ClassNode(TSNode):
    def __init__(self, name):
        super().__init__(name)
        self._decorators = []
        self._properties = []
        self._methods = []
        self._imports = []

    @property
    def decorators(self):
        return self._decorators

    @property
    def properties(self):
        return self._properties

    @property
    def methods(self):
        return self._methods

    @property
    def imports(self):
        return self._imports

    def add_decorator(self, decorator):
        self._decorators.append(decorator)
        return self

    def add_import(self, module, path):
        self.imports.append({module, path})

    def add_property(self, name, type_, visibility="public", initializer=None):
        self.properties.append(
            {
                "name": name,
                "type": type_,
                "visibility": visibility,
                "initializer": initializer,
            }
        )
        return self

    def add_method(self, name, return_type, parameters=None, body=""):
        parameters = parameters or []
        self.methods.append(
            {
                "name": name,
                "return_type": return_type,
                "parameters": parameters,
                "body": body,
            }
        )
        return self

    def _generate_decorators(self) -> str:
        return "\n".join(f"@{decorator}" for decorator in self._decorators)

    def _generate_properties(self) -> str:
        return "\n".join(
            f"  {prop['visibility']} {prop['name']}: {prop['type']}"
            + (f" = {prop['initializer']};" if prop["initializer"] else ";")
            for prop in self.properties
        ) + "\n"

    def _generate_methods(self) -> str:
        return "\n\n".join(
            f"  {method['name']}("
            + ", ".join(f"{param[0]}: {param[1]}" for param in method["parameters"])
            + f"): {method['return_type']} {{\n    {method['body']}\n  }}"
            for method in self.methods
        )

    def _generate_imports(self) -> str:
        return "\n".join(
            f"import {{ {module} }} from '{path}';" for
            module, path in self.imports
        )

    def to_ts(self) -> str:
        decorators_str = self._generate_decorators()
        properties_str = self._generate_properties()
        methods_str = self._generate_methods()
        imports_str = self._generate_imports()
        print(imports_str)

        class_body = "\n".join(filter(None, [properties_str, methods_str]))
        return "\n".join(
            filter(
                None,
                [
                    imports_str,
                    "\n",
                    decorators_str,
                    f"export class {self.name} {{", class_body, "}",
                ]
            )
        )
