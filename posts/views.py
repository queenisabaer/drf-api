# from django.http import Http404
# from rest_framework import status, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Post
# from .serializers import PostSerializer
# from drf_api.permissions import IsOwnerOrReadOnly

from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count = Count('comment', distinct=True),
        likes_count = Count('likes', distinct=True)
    ).order_by('created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner_profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at'
    ]

    def perform_create(self, serializers):
        serializers.save (owner=self.request.user)


    # serializer_class = PostSerializer
    # # to create a post only if you are logged need permission: 
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly
    # ]

    # def get(self, request):
    #     posts = Post.objects.all()
    #     serializer = PostSerializer(
    #         posts, many=True, context={'request': request}
    #     )
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = PostSerializer(
    #         data=request.data, context={'request': request}
    #     )
    #     if serializer.is_valid():
    #         serializer.save(owner=request.user)
    #         return Response(
    #             serializer.data, status=status.HTTP_201_CREATED
    #         )
    #     return Response(
    #         serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #     )


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count = Count('comment', distinct=True),
        likes_count = Count('likes', distinct=True)
    ).order_by('created_at')
    
    # serializer_class = PostSerializer
    # permission_classes = [
    #     IsOwnerOrReadOnly
    # ]
    # def get_object(self, pk):
    #     try:
    #         post = Post.objects.get(pk=pk)
    #         self.check_object_permissions(self.request, post)
    #         return post
    #     except Post.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk):
    #     post= self.get_object(pk)
    #     serializer = PostSerializer(post, context={'request': request})
    #     return Response(serializer.data)
    
    # def put(self, request, pk):
    #     post=self.get_object(pk)
    #     serializer = PostSerializer(post, data=request.data, context={'request':request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(
    #         serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #     )
    
    # def delete(self, request, pk):
    #     post=self.get_object(pk)
    #     post.delete()
    #     return Response(
    #         status=status.HTTP_204_NO_CONTENT
    #     )