from core import DjangoApp, DjangoModel, DjangoView
from tsgen.typescript import ClassNode, InterfaceNode

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
API_URL = "http://localhost:8000/api"


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


class ServiceTranslator:
    # TODO: hold_observable?
    def __init__(
        self,
        app: DjangoApp,
        injectable=True,
        use_store=False
    ):
        self._app = app
        self._node = ClassNode(app.name.capitalize() + "Service")
        self._injectable = injectable
        self._use_store = use_store

    @property
    def app(self):
        return self._app

    @property
    def node(self):
        return self._node

    @property
    def injectable(self) -> bool:
        return self._injectable

    @property
    def use_store(self) -> bool:
        return self._use_store

    def _translate_model_viewset_impl(self, view: DjangoView):
        self._node.add_method(
            "list",
            "Observable<" + view.queryset_model + "[]>",
            [],
            f"return this.http.get<{view.queryset_model}[]>" +
            "(`${{this.url}}/{self.app.name.lower()}`);"
        )

    def _translate_generic_viewset_impl(self, view: DjangoView):
        pass

    def _translate_api_view_impl(self, view: DjangoView):
        pass

    def _generate_methods(self, view: DjangoView):
        print(view.parent_class)
        if view.parent_class == "ModelViewSet":
            self._translate_model_viewset_impl(view)
        elif view.parent_class == "GenericViewSet":
            self._translate_generic_viewset_impl(view)
        elif view.parent_class == "APIView":
            self._translate_api_view_impl(view)

    def _insert_imports(self):
        if self._injectable:
            self._node.add_import("inject, Injectable", "@angular/core")
        if self._use_store:
            self._node.add_import("Store", "@ngrx/store")
        self._node.add_import("HttpClient", "@angular/common/http")
        self._node.add_import("Observable", "rxjs")

    def translate(self):
        self._insert_imports()
        if self._injectable:
            self._node.add_decorator("Injectable()")

        self._node.add_property("url",
                                "string",
                                "private",
                                # TODO: This isn't ideal
                                f"'{API_URL}'")

        self._node.add_property("http",
                                "HttpClient",
                                "private",
                                "inject(HttpClient)")
        self._node.add_property("store", "Store", "private", "inject(Store)")

        for view in self._app.views:
            self._generate_methods(view)
        return self._node.to_ts()
