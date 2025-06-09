from django.shortcuts import get_object_or_404, render
from .models import SinglePage
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from products.models import Contact, ProductComment
from posts.models import Comment as PostComment
from consultations.models import Consultation, Contact
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta

# Create your views here.

def single_page(request, slug):
    page = get_object_or_404(SinglePage, slug=slug, is_published=True)
    return render(request, 'pages/single_page.html', {
        'page': page
    })

@staff_member_required
def dashboard_admin(request):
    # Đơn hàng mới nhất
    orders = Order.objects.all().order_by('-created')[:10]
    # Liên hệ mới nhất (lấy từ consultations.Contact, dùng created_at)
    contacts = Contact.objects.all().order_by('-created_at')[:10]
    # Bình luận bài viết mới nhất
    post_comments = PostComment.objects.all().order_by('-created')[:10]
    # Bình luận sản phẩm mới nhất
    product_comments = ProductComment.objects.all().order_by('-created')[:10]
    
    # Tính doanh số hôm nay
    today = timezone.localtime(timezone.now()).date()
    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    
    revenue_today = Order.objects.filter(
        created__gte=start_of_day,
        created__lte=end_of_day
    ).aggregate(total=Sum('total_cost'))['total'] or 0
    
    # Thống kê
    stats = {
        'orders_total': Order.objects.count(),
        'contacts_total': Contact.objects.count(),
        'consultations_total': Consultation.objects.count(),
        'post_comments_total': PostComment.objects.count(),
        'product_comments_total': ProductComment.objects.count(),
        'orders_today': Order.objects.filter(
            created__gte=start_of_day,
            created__lte=end_of_day
        ).count(),
        'contacts_today': Contact.objects.filter(
            created_at__gte=start_of_day,
            created_at__lte=end_of_day
        ).count(),
        'consultations_today': Consultation.objects.filter(
            created_at__gte=start_of_day,
            created_at__lte=end_of_day
        ).count(),
        'post_comments_today': PostComment.objects.filter(
            created__gte=start_of_day,
            created__lte=end_of_day
        ).count(),
        'product_comments_today': ProductComment.objects.filter(
            created__gte=start_of_day,
            created__lte=end_of_day
        ).count(),
        'revenue_today': revenue_today,
        'revenue_today_million': round(revenue_today / 1000000, 1)  # Chuyển sang triệu đồng
    }
    return render(request, 'dashboard_admin.html', {
        'orders': orders,
        'contacts': contacts,
        'post_comments': post_comments,
        'product_comments': product_comments,
        'stats': stats,
    })
