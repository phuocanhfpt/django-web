from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product, HeroSlide, FAQ, Brand, ProductComment, Feature
from posts.models import Post
from .forms import CustomUserCreationForm, UserUpdateForm, UserProfileUpdateForm, NewsletterForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.db.models import Q, F, ExpressionWrapper, FloatField
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.contrib.auth import login, update_session_auth_hash
from pages.models import SinglePage

def home(request):
    hero_slides = HeroSlide.objects.filter(status='active').order_by('order')
    featured_products = Product.objects.filter(featured=True, status=True)[:8]
    categories = Category.objects.filter(status='active', show_on_home=True)[:12]
    posts = Post.objects.filter(status='published').order_by('-created')[:8]
    faqs = FAQ.objects.filter(status=True).order_by('order')[:10]
    new_products = Product.objects.filter(status=True).order_by('-created')[:10]
    hot_sale_products = (
        Product.objects.filter(status=True, sale_price__isnull=False, sale_price__lt=F('price'))
        .annotate(
            discount_percent=ExpressionWrapper(
                100 * (F('price') - F('sale_price')) / F('price'),
                output_field=FloatField()
            )
        )
        .order_by('-discount_percent', '-created')[:12]
    )
    newsletter_message = ''
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            newsletter_message = 'Đăng ký thành công!'
        else:
            newsletter_message = 'Email không hợp lệ hoặc đã tồn tại!'
    else:
        form = NewsletterForm()
    return render(request, 'home.html', {
        'hero_slides': hero_slides,
        'featured_products': featured_products,
        'categories': categories,
        'posts': posts,
        'faqs': faqs,
        'new_products': new_products,
        'hot_sale_products': hot_sale_products,
        'newsletter_form': form,
        'newsletter_message': newsletter_message,
    })

def contact(request):
    return render(request, 'products/contact.html')

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(status='active')
    brands = Brand.objects.filter(status='active')
    features = Feature.objects.all()  # Get all features
    products = Product.objects.filter(status=True)
    price_min_default = 0
    price_max_default = 10000000
    
    # Get filter parameters
    try:
        price_min = int(request.GET.get('price_min', price_min_default))
        price_max = int(request.GET.get('price_max', price_max_default))
        brand_ids = request.GET.getlist('brands[]') or request.GET.getlist('brands') or []
        feature_ids = request.GET.getlist('features[]') or request.GET.getlist('features') or []
        sort = request.GET.get('sort', 'newest')
        page = int(request.GET.get('page', 1))
        display_count = int(request.GET.get('display_count', 12))
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)
    
    # Handle category from URL or AJAX request
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, status='active')
        products = products.filter(category=category)
    # Luôn dùng product_list.html
    template = 'products/product_list.html'
    
    # Apply price filter
    products = products.filter(price__gte=price_min, price__lte=price_max)
    
    # Apply brand filter
    if brand_ids and brand_ids[0]:  # Check if brand_ids is not empty and first element is not empty
        try:
            brand_ids = [int(brand_id) for brand_id in brand_ids if brand_id]
            if brand_ids:  # Only apply filter if we have valid brand IDs
                products = products.filter(brand_id__in=brand_ids)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid brand IDs'}, status=400)
    
    # Apply feature filters
    if feature_ids and feature_ids[0]:  # Check if feature_ids is not empty and first element is not empty
        try:
            feature_ids = [int(feature_id) for feature_id in feature_ids if feature_id]
            if feature_ids:  # Only apply filter if we have valid feature IDs
                products = products.filter(features__id__in=feature_ids).distinct()
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid feature IDs'}, status=400)
    
    # Apply sorting
    if sort == 'price-asc':
        products = products.order_by('price')
    elif sort == 'price-desc':
        products = products.order_by('-price')
    elif sort == 'name-asc':
        products = products.order_by('name')
    elif sort == 'name-desc':
        products = products.order_by('-name')
    else:  # newest
        products = products.order_by('-created')
    
    # Pagination
    paginator = Paginator(products, display_count)
    try:
        products_page = paginator.get_page(page)
    except (EmptyPage, PageNotAnInteger):
        products_page = paginator.get_page(1)
    
    # For API requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            products_data = []
            for product in products_page:
                products_data.append({
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price),
                    'sale_price': float(product.sale_price) if product.sale_price else None,
                    'image': product.image.url if product.image else None,
                    'url': product.get_absolute_url(),
                })
            
            return JsonResponse({
                'products': products_data,
                'has_next': products_page.has_next(),
                'total_pages': paginator.num_pages,
                'current_page': page
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # For regular requests
    context = {
        'categories': categories,
        'brands': brands,
        'features': features,
        'products': products_page,
        'price_min': price_min,
        'price_max': price_max,
        'price_min_default': price_min_default,
        'price_max_default': price_max_default,
        'selected_brands': brand_ids,
        'selected_features': feature_ids,
        'sort': sort,
        'display_count': display_count
    }
    if category:
        context['category'] = category
    return render(request, template, context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, status=True)
    related_products = Product.objects.filter(
        category=product.category,
        status=True
    ).exclude(id=product.id)[:4]
    comments = ProductComment.objects.filter(product=product, approved=True, parent__isnull=True)
    accessories = product.accessories.all()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'comments': comments,
        'accessories': accessories,
    })

class CategoryListView(ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(status='active')

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(status=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug, status='active')
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(status='active')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'], category__slug=self.kwargs['category_slug'], status=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            status=True
        ).exclude(id=self.object.id)[:4]
        context['comments'] = ProductComment.objects.filter(product=self.object, approved=True, parent__isnull=True)
        context['accessories'] = self.object.accessories.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'rating' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, 'Bạn cần đăng nhập để đánh giá sản phẩm.')
                return redirect(self.object.get_absolute_url())
            rating_value = int(request.POST.get('rating', 0))
            if rating_value < 1 or rating_value > 5:
                messages.error(request, 'Vui lòng chọn số sao hợp lệ.')
                return redirect(self.object.get_absolute_url())
            from .models import ProductRating
            rating_obj, created = ProductRating.objects.update_or_create(
                product=self.object, user=request.user,
                defaults={'rating': rating_value}
            )
            messages.success(request, 'Cảm ơn bạn đã đánh giá sản phẩm!')
            return redirect(self.object.get_absolute_url())
        # Xử lý bình luận như cũ
        if request.user.is_authenticated:
            content = request.POST.get('content')
            parent_id = request.POST.get('parent_id')
            is_admin_reply = request.POST.get('is_admin_reply')
            if content:
                if parent_id and is_admin_reply and request.user.is_staff:
                    parent_comment = ProductComment.objects.filter(id=parent_id, parent__isnull=True, product=self.object).first()
                    if parent_comment:
                        ProductComment.objects.create(
                            product=self.object,
                            user=request.user,
                            content=content,
                            parent=parent_comment,
                            is_admin_reply=True
                        )
                        messages.success(request, 'Đã trả lời bình luận!')
                        return redirect(self.object.get_absolute_url() + f"#reply-form-{parent_id}")
                else:
                    ProductComment.objects.create(product=self.object, user=request.user, content=content)
                    messages.success(request, 'Bình luận của bạn đã được gửi!')
                    return redirect(self.object.get_absolute_url())
            else:
                messages.error(request, 'Vui lòng nhập nội dung bình luận.')
        else:
            messages.error(request, 'Bạn cần đăng nhập để bình luận.')
        return redirect(self.object.get_absolute_url())

def category_list(request):
    categories = Category.objects.filter(show_on_home=True)
    return render(request, 'products/category_list.html', {
        'categories': categories
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    brands = Brand.objects.all()
    features = Feature.objects.all()  # Get all features
    price_min_default = 0
    price_max_default = 10000000
    
    # Get filter parameters
    price_min = request.GET.get('price_min', price_min_default)
    price_max = request.GET.get('price_max', price_max_default)
    brand_ids = request.GET.getlist('brands', [])
    feature_ids = request.GET.getlist('features', [])  # Update to use feature_ids
    sort = request.GET.get('sort', 'newest')
    page = int(request.GET.get('page', 1))
    display_count = int(request.GET.get('display_count', 12))
    
    # Base queryset
    products = Product.objects.filter(category=category, status=True)
    
    # Apply price filter
    products = products.filter(price__gte=price_min, price__lte=price_max)
    
    # Apply brand filter
    if brand_ids:
        products = products.filter(brand_id__in=brand_ids)
    
    # Apply feature filters
    if feature_ids:
        products = products.filter(features__id__in=feature_ids).distinct()
    
    # Apply sorting
    if sort == 'price-asc':
        products = products.order_by('price')
    elif sort == 'price-desc':
        products = products.order_by('-price')
    elif sort == 'name-asc':
        products = products.order_by('name')
    elif sort == 'name-desc':
        products = products.order_by('-name')
    else:  # newest
        products = products.order_by('-created')
    
    # Pagination
    paginator = Paginator(products, display_count)
    products_page = paginator.get_page(page)
    
    # For API requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_data = []
        for product in products_page:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'sale_price': float(product.sale_price) if product.sale_price else None,
                'image': product.image.url if product.image else None,
                'url': product.get_absolute_url(),
            })
        
        return JsonResponse({
            'products': products_data,
            'has_next': products_page.has_next(),
            'total_pages': paginator.num_pages,
            'current_page': page
        })
    
    # For regular requests
    return render(request, 'products/category_list.html', {
        'category': category,
        'brands': brands,
        'features': features,  # Add features to context
        'products': products_page,
        'price_min': price_min,
        'price_max': price_max,
        'price_min_default': price_min_default,
        'price_max_default': price_max_default,
        'selected_brands': brand_ids,
        'selected_features': feature_ids,  # Update to use feature_ids
        'sort': sort,
        'display_count': display_count
    })

def search_results(request):
    query = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    per_page = 12
    products_qs = Product.objects.filter(name__icontains=query) if query else Product.objects.none()
    posts = Post.objects.filter(title__icontains=query) if query else Post.objects.none()
    paginator = Paginator(products_qs, per_page)
    products_page = paginator.get_page(page)
    # AJAX request for load more
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_data = []
        for product in products_page:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'sale_price': float(product.sale_price) if product.sale_price else None,
                'image': product.image.url if product.image else None,
                'url': product.get_absolute_url(),
            })
        return JsonResponse({
            'products': products_data,
            'has_next': products_page.has_next(),
        })
    return render(request, 'search_results.html', {
        'query': query,
        'products': products_page,
        'posts': posts,
    })

@login_required
def profile(request):
    user = request.user
    # Tự động tạo UserProfile nếu chưa có
    if not hasattr(user, 'userprofile'):
        from .models import UserProfile
        UserProfile.objects.create(user=user, full_name=user.get_full_name() or user.username)
    orders = Order.objects.filter(user=user).order_by('-created')
    if request.method == 'POST' and 'update_info' in request.POST:
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileUpdateForm(request.POST, instance=user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileUpdateForm(instance=user.userprofile)
    return render(request, 'products/profile.html', {
        'user': user,
        'orders': orders,
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Cập nhật session để không bị logout
            messages.success(request, 'Mật khẩu của bạn đã được thay đổi thành công!')
            return redirect('products:password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })

@login_required
def password_change_done(request):
    return render(request, 'registration/password_change_done.html')

def sitemap_modal(request):
    product_categories = Category.objects.filter(status='active')
    featured_products = Product.objects.filter(featured=True, status=True)[:8]
    latest_posts = Post.objects.filter(status='published').order_by('-created')[:8]
    single_pages = SinglePage.objects.filter(is_published=True).order_by('-created_at')[:8]
    return render(request, 'sitemap_modal.html', {
        'product_categories': product_categories,
        'featured_products': featured_products,
        'latest_posts': latest_posts,
        'single_pages': single_pages,
    })
