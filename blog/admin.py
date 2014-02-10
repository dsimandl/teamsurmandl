from django.contrib import admin
from blog.models import Post, PostComment


class PostAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_at'
    fields = ('published', 'title', 'slug', 'content', 'author', 'photo', 'tags')
    list_display = ['published', 'title', 'updated_at']
    list_display_links = ['title']
    list_editable = ['published']
    list_filter = ['published', 'updated_at', 'author']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']

admin.site.register(Post, PostAdmin)


class PostCommentAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_at'
    fields = ('post', 'author', 'comment')

admin.site.register(PostComment, PostCommentAdmin)