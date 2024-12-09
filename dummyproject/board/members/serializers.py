from rest_framework import serializers
from members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"
        read_only_fields = ('password', 'created_at', 'updated_at')
