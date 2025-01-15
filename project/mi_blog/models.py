from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
import random
import string

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
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='blog_name')
    publish = models.DateTimeField(default=timezone.now) 
    created = models.DateTimeField(auto_now_add = True) #Cuando se cree un Post automaticamente se guardara la fecha en la que se creo el Post
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=2,
                                choices= Status.choices, 
                                default=Status.DRAFT)
    tags = TaggableManager()
    
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


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postLike')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userLike')

    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Like de {self.user} a {self.post}"

    class Meta():
        unique_together = ('post', 'user')
    
    @classmethod
    def remove_like(cls, post, user):
        like = cls.objects.filter(post=post, user=user).first()
        if like:
            like.delete()
            return True
        return False



def generate_unique_slug(base_slug):
    # Genera un slug único, añadiendo un sufijo aleatorio si el slug ya existe
    unique_slug = base_slug
    while User.objects.filter(slug=unique_slug).exists():
        # Generar un sufijo aleatorio
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        unique_slug = f"{base_slug}-{random_suffix}"
    return unique_slug

class User(AbstractUser):
    image_profile = models.ImageField(upload_to='image_profile/', blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)
    preferences = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(blank=True, null=True)


    class Meta:
        ordering = ['-username']
        indexes = [models.Index(fields=['-username'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)  # O algún otro valor que te convenga
        super(User, self).save(*args, **kwargs)


    def get_absolute_url(self):
        # Generar el slug basado en el first_name o username
        base_slug = slugify(self.first_name) if self.first_name else slugify(self.username)
        
        # Asegurar que el slug sea único
        unique_slug = generate_unique_slug(base_slug)

        return reverse('mi_blog:perfilOne', kwargs={
            'username': self.username,
            'slug': unique_slug,
        })



    def __str__(self):
        return f"{self.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, 
                            on_delete=models.CASCADE, 
                            related_name='comments')
    content = models.TextField()
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios2')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta():
        ordering = ['-created']
        indexes = [models.Index
                    (fields=['-created'])]
    def __str__(self):
        return f"Name: {self.name}"