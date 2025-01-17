from django.db import models
from django.conf import settings
from mi_blog.models import Post

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE, 
                            related_name='notfs')
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    post = models.ForeignKey(Post, 
                            on_delete=models.CASCADE, 
                            related_name='post_notfs', 
                            null=True, 
                            blank=True)
    
    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return f"Notification: {self.message} by {self.user}"

