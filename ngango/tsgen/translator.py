from core import DjangoModel
from tsgen.typescript import InterfaceNode

TYPE_MAPPINGS = {
    "CharField": "string",
    "TextField": "string",
    "IntegerField": "number",
    "BooleanField": "boolean",
    # DateTimeField is serialized to a string in almost every use case
    "DateTimeField": "string",
    "DateField": "Date",
    "TimeField": "Date",
    # TODO: Depends on the serializer used.
    # TODO: Could be another object entirely.
    "ForeignKey": "number",
}


class ModelTranslator:
    def __init__(self, model: DjangoModel):
        self.model = model
        self._node = InterfaceNode(model.name)

    def translate(self):
        for field in self.model.fields:
            mapped_type = TYPE_MAPPINGS.get(field.field_type, "any")
            self._node.add_property(field.name,
                                    mapped_type,
                                    field.nullable)
        return self._node.to_ts()
