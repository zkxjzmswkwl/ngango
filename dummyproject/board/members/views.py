from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from members.models import Member
from members.serializers import MemberSerializer

# Need both ModelViewSet & APIView for testing the tooling.


class MemberViewSet(ModelViewSet):
    """
    {
        "ngango": {
            "service": "Members",
            "actions": [
                "list",
                "create",
                "retrieve",
                "update",
                "destroy"
            ]
        }
    }
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberProfile(APIView):
    queryset = Member.objects.all()
    """
    {
        "ngango": {
            "service": "Members",
            "actions": [
            ]
        }
    }
    """
    def get(self, request):
        member = Member.objects.get(id=request.user.id)
        serializer = MemberSerializer(member)
        return Response(serializer.data)
