from .models import Post
from django.contrib.sitemaps import Sitemap

class PostSitemaps(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Post.published.all()
    
    def lastmod(self):
        return obj.updated