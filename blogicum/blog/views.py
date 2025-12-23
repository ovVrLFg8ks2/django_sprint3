from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    posts = Post.published.select_related(
        'category', 'author', 'location'
    ).order_by('-pub_date')[:5]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    matched_post = get_object_or_404(
        Post.published.select_related('category', 'author', 'location'),
        id=pk
    )
    context = {'post': matched_post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.published.select_related(
        'category', 'author', 'location'
    ).filter(
        category=category
    )
    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, template, context)
