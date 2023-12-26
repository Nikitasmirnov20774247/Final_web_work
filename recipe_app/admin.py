from django.contrib import admin
from . import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'make_time', 'author', 'create_date', 'update_date', 'is_public', 'is_active']
    list_filter = ['create_date', 'update_date']
    ordering = ['-update_date']
    readonly_fields = ['create_date', 'update_date']

    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['title', 'description']
            }
        ),
        (
            'О рецепте',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['products', 'steps', 'make_time', 'image', 'author']
            }
        ),
        (
            'Статус',
            {
                'classes': ['wide'],
                'fields': ['create_date', 'update_date', 'is_public', 'is_active']
            }
        )
    ]
