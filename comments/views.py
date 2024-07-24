from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Instead of specifying only the model to use, in DRF we set the queryset attribute
    # This way, it is possible to filter out some of the model instances.(e.g. sensible data)
    queryset = Comment.objects.all()

    def perform_create(self, serializers):
        serializers.save (owner=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class=CommentDetailSerializer
    queryset = Comment.objects.all()
