from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, GroupVievSet, FollowViewSet

router = DefaultRouter()

router.register('posts', PostViewSet)
router.register('groups', GroupVievSet)
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls))
]
