from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower')  # подписки юзера
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following')  # подписчики юзера

    def __str__(self):
        return (f"{self.user.username}({self.user.id})->"
                f"{self.author.username}({self.author.id})")

    class Meta:
        unique_together = ('author', 'user',)


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(Group,
                              related_name='posts',
                              null=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Группа',
                              help_text=("Группа, "
                                         "к которой будет относиться пост"))

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
