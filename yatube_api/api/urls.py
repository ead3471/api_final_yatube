from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, GroupVievSet, FollowViewSet, CommentViewSet

router = DefaultRouter()

router.register('posts', PostViewSet)
router.register('groups', GroupVievSet)
router.register('follow', FollowViewSet, basename='follow')
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls))
]
