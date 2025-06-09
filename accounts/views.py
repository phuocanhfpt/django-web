from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from orders.models import Order
from products.forms import UserUpdateForm, UserProfileUpdateForm
from products.models import ProductComment
from posts.models import Comment
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            form.save_m2m()
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Đăng ký thành công! Chào mừng bạn đến với Camera HCM.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    # Tự động tạo UserProfile nếu chưa có
    if not hasattr(user, 'userprofile'):
        from products.models import UserProfile
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
    return render(request, 'accounts/profile.html', {
        'user': user,
        'orders': orders,
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'accounts/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'accounts/order_detail.html', {'order': order})

@login_required
def product_comments(request):
    comments = ProductComment.objects.filter(user=request.user).order_by('-created')
    return render(request, 'accounts/product_comments.html', {'comments': comments})

@login_required
def post_comments(request):
    comments = Comment.objects.filter(user=request.user).order_by('-created')
    return render(request, 'accounts/post_comments.html', {'comments': comments})

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.txt'
    html_email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done') 