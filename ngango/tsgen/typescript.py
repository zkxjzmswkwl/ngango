class TSNode:

    def __init__(self, name):
        self.name = name

    def to_ts(self) -> str:
        raise NotImplementedError("Subclasses must implement this method.")


class InterfaceNode(TSNode):

    def __init__(self, name):
        super().__init__(name)
        self.properties = []

    def add_property(self, name, type_, optional=False):
        self.properties.append({"name": name, "type": type_, "optional": optional})
        return self

    def to_ts(self) -> str:
        properties_str = "\n".join(
            f"  {prop['name']}{'?' if prop['optional'] else ''}: {prop['type']};"
            for prop in self.properties
        )
        return f"export interface {self.name} {{\n{properties_str}\n}}"


class ClassNode(TSNode):
    def __init__(self, name):
        super().__init__(name)
        self.decorators = []
        self.properties = []
        self.methods = []

    def add_decorator(self, decorator):
        self.decorators.append(decorator)
        return self

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
        return "\n".join(f"@{decorator}" for decorator in self.decorators)

    def _generate_properties(self) -> str:
        return "\n".join(
            f"  {prop['visibility']} {prop['name']}: {prop['type']}"
            + (f" = {prop['initializer']};" if prop["initializer"] else ";")
            for prop in self.properties
        )

    def _generate_methods(self) -> str:
        return "\n\n".join(
            f"  {method['name']}("
            + ", ".join(f"{param[0]}: {param[1]}" for param in method["parameters"])
            + f"): {method['return_type']} {{\n    {method['body']}\n  }}"
            for method in self.methods
        )

    def to_ts(self) -> str:
        decorators_str = self._generate_decorators()
        properties_str = self._generate_properties()
        methods_str = self._generate_methods()

        class_body = "\n\n".join(filter(None, [properties_str, methods_str]))
        return "\n".join(
            filter(
                None, [decorators_str, f"export class {self.name} {{", class_body, "}"]
            )
        )


def generate_service(name: str, django_app):
    """
    Notes

    - add_method("addUser", "void", [("user", "User")], "this.users.push(user)")
      - For ModelViewSets, this should almost always return `Observable<T>`.
    """
    user_service = (
        ClassNode(name)
        .add_decorator("Injectable()")
        .add_property("users", "User[]", "private", "[]")
        .add_method("addUser", "void", [("user", "User")], "this.users.push(user);")
        .add_method(
            "getUserById",
            "User | undefined",
            [("id", "number")],
            "return this.users.find(user => user.id === id);",
        )
    )

    return user_service.to_ts()
