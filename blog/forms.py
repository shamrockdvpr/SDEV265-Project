from django import forms
from django.forms import inlineformset_factory
from .models import Post, Comment, IngredientToRecipe


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'description', 'picture')


# FormSet for managing ingredients linked through IngredientToRecipe
IngredientToRecipeFormSet = inlineformset_factory(
    Post,  # Parent model
    IngredientToRecipe,  # Child model
    fields=('ingredient', 'quantity', 'unit', 'instructions'),  # Fields to expose
    extra=5,  # Number of blank ingredient rows to show initially
    can_delete=True  # Allow deletion of ingredients
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
