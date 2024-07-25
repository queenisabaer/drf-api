from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Instead of specifying only the model to use, in DRF we set the queryset attribute
    # This way, it is possible to filter out some of the model instances.(e.g. sensible data)
    queryset = Comment.objects.all()

    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'post',
    ]

    def perform_create(self, serializers):
        serializers.save (owner=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class=CommentDetailSerializer
    queryset = Comment.objects.all()
