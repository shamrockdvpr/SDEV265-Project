from django import forms
from django.forms import inlineformset_factory
from .models import Post, Comment, IngredientToRecipe, RecipeImg


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'description')

class RecipeImgForm(forms.ModelForm):
    class Meta:
        model = RecipeImg
        fields = ('img',)

# FormSet for managing ingredients linked through IngredientToRecipe
IngredientToRecipeFormSet = inlineformset_factory(
    Post,  # Parent model
    IngredientToRecipe,  # Child model
    fields=('ingredient', 'quantity', 'unit', 'instructions'),
    extra=5,  # Number of blank ingredient rows to show initially
    # can_delete=True  # Allow deletion of ingredients. Unused right now
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
