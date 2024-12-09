from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from posts.models import Board, Post
from posts.serializers import BoardSerializer, PostSerializer


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class PostAPIView(APIView):
    queryset = Post.objects.all().select_related("owner", "board")

    def get(self, request):
        posts = self.queryset
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
