from django.contrib import admin
from .models import Profile, Artwork, Comment, Like


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_owner', 'created_at']
    list_filter = ('created_at', 'gallery')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

    def get_owner(self, obj):
        if obj.gallery and obj.gallery.owner:
            return obj.gallery.owner.username
        return "No Owner"

    get_owner.short_description = "Owner"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'artwork', 'created_at')
    search_fields = ('text',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'artwork')