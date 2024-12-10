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

OPERATION_MAPPINGS = {
    "list": "get",
    "create": "post",
    "update": "put",
    "destroy": "delete",
}