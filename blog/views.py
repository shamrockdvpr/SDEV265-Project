from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from .forms import PostForm, CommentForm, IngredientToRecipeFormSet, IngredientToRecipe
from .models import Post, Comment


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    ingredients = IngredientToRecipe.objects.filter(post=post)
    return render(request, 'blog/post_detail.html', {'post': post, 'ingredients': ingredients,})


@staff_member_required()
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        formset = IngredientToRecipeFormSet(request.POST, instance=form.instance)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            formset.instance = post
            formset.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        formset = IngredientToRecipeFormSet()
    return render(request, 'blog/post_edit.html', {'form': form,
                                                   'formset': formset,
                                                   })


@staff_member_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@staff_member_required()
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@staff_member_required()
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.publish()
    return redirect('post_detail', pk=pk)


@staff_member_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
    return redirect('post_list')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@staff_member_required()
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@staff_member_required()
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
