from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["-created"]

    title = models.CharField("заголовок", max_length=128)
    text = models.TextField("текст")
    created = models.DateTimeField("создано", auto_now_add=True)
    edited = models.DateTimeField("изменено", auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="автор", related_name="posts"
    )
    likes = models.ManyToManyField(
        User, verbose_name="отметка like", related_name="liked_posts"
    )
    unlikes = models.ManyToManyField(
        User, verbose_name="отметка unlike", related_name="unliked_posts"
    )

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def unlikes_count(self):
        return self.unlikes.count()
