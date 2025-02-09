from django.contrib import admin

from .models import Post, Comment, IngredientToRecipe


class IngredientToRecipeInline(admin.TabularInline):  # Use TabularInline or StackedInline
    model = IngredientToRecipe
    extra = 1  # Number of empty rows to display
    # Optionally set fields to display
    fields = ('ingredient', 'quantity', 'unit', 'instructions')


class PostAdmin(admin.ModelAdmin):
    inlines = [IngredientToRecipeInline]


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
