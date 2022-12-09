from rest_framework.permissions import BasePermission, SAFE_METHODS
from posts.models import Post, Comment
from typing import Union
from rest_framework.viewsets import ModelViewSet


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self,
                              request,
                              view: ModelViewSet,
                              obj: Union[Post, Comment]):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user
