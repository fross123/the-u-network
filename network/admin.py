from django.contrib import admin

from .models import Post, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("following",)

admin.site.register(Post)
admin.site.register(User, UserAdmin)
