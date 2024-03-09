
# Register your models here.
from django.contrib import admin
from .models import Note


# Customizing the appearance of Note model in admin interface
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')  # Display these fields in the list view
    search_fields = ('title', 'body')  # Enable searching by title and body
    list_filter = ('user',)  # Enable filtering by user


# Register your models with custom admin options
admin.site.register(Note, NoteAdmin)
