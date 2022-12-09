from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from posts.models import Post, Group, Follow, Comment
from .serializers import PostSerializer, GroupSerializer, FollowSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly, IsOwner
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: PostSerializer):
        serializer.save(author=self.request.user)


class GroupVievSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    permission_classes = (IsAuthenticated, IsOwner,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer: FollowSerializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.user.username == request.data.get('following'):
            return Response("Subscribe to yourself is prohbited!",
                            status=status.HTTP_400_BAD_REQUEST)

        if (Follow.
            objects.
            filter(user=request.user).
            filter(following__username=request.data.get('following')).
                exists()):
            return Response("Follow already exists!",
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    search_fields = ('following__username',)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post=post_id).all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
