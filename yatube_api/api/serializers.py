from rest_framework.serializers import (ModelSerializer,
                                        ImageField,
                                        SlugRelatedField)
from rest_framework.relations import SlugRelatedField
import base64
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from posts.models import Comment, Post, Group, Follow
from rest_framework.serializers import ValidationError

User = get_user_model()


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = '__all__'

    def validate_following(self, following: User):
        user: User = self.context.get('request').user
        if user == following:
            raise ValidationError("Subscribe to yourself is prohbited!")

        if (Follow.
            objects.
            filter(user=user).
                filter(following=following).exists()):
            raise ValidationError("Follow already exists!")
        return following
