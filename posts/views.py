from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, PostCategory, Comment
from django.db.models import Count, Q
from taggit.models import Tag

# Create your views here.

def post_list(request):
    categories = PostCategory.objects.all()
    posts = Post.objects.filter(status='published').select_related('category')\
        .annotate(comments_count=Count('comments', filter=Q(comments__approved=True)))
    paginator = Paginator(posts, 9)  # 9 bài/1 trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    recent_posts = Post.objects.filter(status='published').order_by('-created')[:5]
    return render(request, 'posts/post_list.html', {
        'categories': categories,
        'category': None,
        'posts': page_obj,
        'recent_posts': recent_posts,
    })

def post_list_by_category(request, slug):
    categories = PostCategory.objects.all()
    category = get_object_or_404(PostCategory, slug=slug)
    posts = Post.objects.filter(status='published', category=category).select_related('category')\
        .annotate(comments_count=Count('comments', filter=Q(comments__approved=True)))
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    recent_posts = Post.objects.filter(status='published').order_by('-created')[:5]
    return render(request, 'posts/post_list.html', {
        'categories': categories,
        'category': category,
        'posts': page_obj,
        'recent_posts': recent_posts,
    })

def post_list_by_tag(request, tag_slug):
    categories = PostCategory.objects.all()
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(status='published', tags__in=[tag]).select_related('category')\
        .annotate(comments_count=Count('comments', filter=Q(comments__approved=True)))
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    recent_posts = Post.objects.filter(status='published').order_by('-created')[:5]
    return render(request, 'posts/post_list.html', {
        'categories': categories,
        'category': None,
        'tag': tag,
        'posts': page_obj,
        'recent_posts': recent_posts,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(approved=True)
    related_posts = Post.objects.filter(status='published', category=post.category).exclude(id=post.id)[:5]

    if request.method == 'POST':
        if request.user.is_authenticated:
            content = request.POST.get('content')
            parent_id = request.POST.get('parent_id')
            is_admin_reply = request.POST.get('is_admin_reply')
            if content:
                if parent_id and is_admin_reply and request.user.is_staff:
                    # Trả lời admin
                    parent_comment = post.comments.filter(id=parent_id, parent__isnull=True).first()
                    if parent_comment:
                        Comment.objects.create(
                            post=post,
                            user=request.user,
                            content=content,
                            parent=parent_comment,
                            is_admin_reply=True
                        )
                        messages.success(request, 'Đã trả lời bình luận!')
                        return redirect(post.get_absolute_url() + f"#reply-form-{parent_id}")
                else:
                    # Bình luận thường
                    Comment.objects.create(post=post, user=request.user, content=content)
                    messages.success(request, 'Bình luận của bạn đã được gửi!')
                    return redirect(post.get_absolute_url())
            else:
                messages.error(request, 'Vui lòng nhập nội dung bình luận.')
        else:
            messages.error(request, 'Bạn cần đăng nhập để bình luận.')

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
    })
