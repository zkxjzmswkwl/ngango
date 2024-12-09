from ngango.core import DjangoProject


class TSGenerator:
    def __init__(self, django_project: DjangoProject):
        pass

    def generate(self):
        """
        1 - Generate one interface per model
          - Each interface must have the same name as the model
          - Remember to account for nullability.
        * - If relationships present, check serializer
        * - for foreign serializer inclusion? Seems like a lot of work.
        * - ceebs for now.

        2 - Generate one service per app

        3 - TODO: Parse @ngango docstring for service name and actions.
        Example:

            class MemberViewSet(ModelViewSet):
            \"""
            @ngango {
                service: Members,
                actions: {
                    list,
                    create,
                    retrieve,
                    update,
                    destroy
                }
            }
            \"""
            queryset = Member.objects.all()
            serializer_class = MemberSerializer
        """
        pass
