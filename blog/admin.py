from django.contrib import admin


from django_summernote.admin import SummernoteModelAdmin

from blog.models import Post, PostComment

class PostAdmin(SummernoteModelAdmin):
    """
    Model admin for the post model
    """

    date_hierarchy = 'created_at'
    fields = ('published', 'title', 'author', 'content', 'tags', 'slug')
    list_display = ['published', 'title', 'updated_at']
    list_display_links = ['title']
    list_editable = ['published']
    list_filter = ['published', 'updated_at', 'author']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']

admin.site.register(Post, PostAdmin)


class PostCommentAdmin(admin.ModelAdmin):
    """
    Model admin for the post comment model
    """

    date_hierarchy = 'created_at'
    fields = ('post', 'author', 'comment')

admin.site.register(PostComment, PostCommentAdmin)