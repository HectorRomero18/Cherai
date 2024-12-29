from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from django.urls import reverse

# Create your models here.
class Post_Published(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
class Post(models.Model):
    
    class Status(models.TextChoices):
        PUBLISHED = 'PB', 'Published'
        DRAFT = 'DF', 'Draft'

    title = models.CharField(max_length=250)
    body = models.TextField(max_length=550)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='blog_name')
    publish = models.DateTimeField(default=timezone.now) 
    created = models.DateTimeField(auto_now_add = True) #Cuando se cree un Post automaticamente se guardara la fecha en la que se creo el Post
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=2,
                                choices= Status.choices, 
                                default=Status.DRAFT)
    
    objects = models.Manager()
    published = Post_Published()

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(
                    fields=['-publish'])]

    def __str__(self):
        return (f"Title: {self.title}")
    
    def get_absolute_url(self):
        return reverse('blog:detalle', args=[
                        self.publish.year, 
                        self.publish.month, 
                        self.publish.day, 
                        self.slug])

class User(AbstractUser):
    image_profile = models.ImageField(upload_to='image_profile/', blank=True, null=True)

    def __str__(self):
        return f"{self.username}"