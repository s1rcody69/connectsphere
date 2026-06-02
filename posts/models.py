from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """
    Core content model for ConnectSphere.
    A post belongs to one author and can contain text, an image, and hashtags.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField(max_length=2000)
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True
    )
    hashtags = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username}: {self.content[:50]}'

    def total_likes(self):
        try:
           return self.likes.count()
        except Exception:
           return 0
   
    def total_comments(self):
        try:
            return self.comments.count()
        except Exception:
             return 0