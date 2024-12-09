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
        self.properties.append({
            "name": name,
            "type": type_,
            "optional": optional
        })
        return self

    def to_ts(self) -> str:
        properties_str = "\n".join(
            f"  {prop['name']}{'?' if prop['optional'] else ''}: {prop['type']};"
            for prop in self.properties)
        return f"export interface {self.name} {{\n{properties_str}\n}}"


class ClassNode(TSNode):

    def __init__(self, name):
        super().__init__(name)
        self.properties = []
        self.methods = []

    def add_property(self, name, type_, visibility="public", initializer=None):
        self.properties.append({
            "name": name,
            "type": type_,
            "visibility": visibility,
            "initializer": initializer,
        })
        return self

    def add_method(self, name, return_type, parameters=None, body=""):
        parameters = parameters or []
        self.methods.append({
            "name": name,
            "return_type": return_type,
            "parameters": parameters,
            "body": body,
        })
        return self

    def to_ts(self) -> str:
        properties_str = "\n".join(
            f"  {prop['visibility']} {prop['name']}: {prop['type']}{f' = {prop['initializer']}' if prop['initializer'] else ''};"
            for prop in self.properties)
        methods_str = "\n".join(
            f"  {method['name']}({', '.join([f'{param[0]}: {param[1]}' for param in method['parameters']])}): {method['return_type']} {{\n    {method['body']}\n  }}"
            for method in self.methods)
        return f"export class {self.name} {{\n{properties_str}\n\n{methods_str}\n}}"
