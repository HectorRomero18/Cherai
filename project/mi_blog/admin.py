from django.contrib import admin
from mi_blog.models import Post, User, Comment, PostLike

# Registrar el modelo Post en el panel de administración
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff',]
    search_fields = ['username', 'email']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de posts
    list_display = ['title', 'author', 'publish', 'status', 'slug']
    
    # Permite ordenar los posts por fecha de publicación (descendente)
    ordering = ['-publish']
    
    # Campos que se podrán filtrar en la barra lateral
    list_filter = ['status', 'publish', 'author']
    
    # Campos por los que se podrá buscar en el panel de administración
    search_fields = ['title', 'body', 'author__username']  # Autor por nombre de usuario
    
    # Generar automáticamente el slug a partir del título
    prepopulated_fields = {'slug': ('title',)}
    
    # Agregar un formulario de edición de posts personalizado si lo deseas
    # fields = ('title', 'body', 'author', 'publish', 'status')  # Puedes personalizar el orden de los campos
    
    # Mostrar un filtro más limpio para editar el 'status'
    list_editable = ['status']  # Permite editar el estado de un post directamente desde la lista

@admin.register(Comment)
class CommentRegister(admin.ModelAdmin):
    
    list_display = ['name', 'created', 'active']

    oredering = ['-created']

    list_filter = ['name', 'content', 'created', 'updated']

    search_fields = ['name', 'body']



@admin.register(PostLike)
class PostLikeRegister(admin.ModelAdmin):
    
    list_display = ['post', 'user', 'created_at']

    oredering = ['-post']

    list_filter = ['post', 'user']

    search_fields = ['post', 'user']
    

