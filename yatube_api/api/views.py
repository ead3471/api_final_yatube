from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from posts.models import Post, Group, Follow, Comment
from .serializers import (PostSerializer,
                          GroupSerializer,
                          FollowSerializer,
                          CommentSerializer)
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


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


class FollowViewSet(CreateModelMixin,
                    ListModelMixin,
                    GenericViewSet):
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    permission_classes = (IsAuthenticated,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer: FollowSerializer):
        serializer.save(user=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post=post_id).all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
