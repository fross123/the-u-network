from django.contrib import admin

from .models import Post, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("following",)

class PostAdmin(admin.ModelAdmin):
    list_display = ("date", "content", "user", "likes")

admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
