from django.db import models
from django.utils import timezone


# Create your models here.
class IngredientToRecipe(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    ingredient = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50, blank=True, null=True)  # 400
    unit = models.CharField(max_length=50, blank=True, null=True)  # pounds, lbs, oz ,grams, etc
    instructions = models.CharField(max_length=50, blank=True, null=True)  # chopped, diced etc

class RecipeImg(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/', null=True, blank=True)

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
