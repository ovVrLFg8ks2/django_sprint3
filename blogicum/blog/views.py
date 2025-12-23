from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.utils import timezone


def get_published_posts():
    return Post.published.select_related('category', 'author', 'location')


def index(request):
    template = 'blog/index.html'
    posts = get_published_posts()[:5]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    matched_post = get_object_or_404(
        get_published_posts(),
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
    posts = category.category_posts.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).select_related('category', 'author', 'location')
    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, template, context)
