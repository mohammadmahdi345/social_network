from django.contrib import admin

from .models import Post, PostProfile



class PostProfileAdmin(admin.StackedInline):
    model = PostProfile
    fields = ('file',)
    extra = 0
    can_delete = False



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','location', 'is_active', 'created_time')
    inlines = (PostProfileAdmin,)
    readonly_fields = ['caption']



