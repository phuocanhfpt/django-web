from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Consultation, Newsletter
import re
import logging
from .forms import ContactForm
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q

logger = logging.getLogger(__name__)

# Create your views here.

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def newsletter_subscription(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email', '').strip()
            logger.info(f"Received newsletter subscription request for email: {email}")
            
            if not email:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Vui lòng nhập địa chỉ email'
                })
            
            if not validate_email(email):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Địa chỉ email không hợp lệ'
                })
            
            # Kiểm tra email đã tồn tại chưa
            if Newsletter.objects.filter(email=email).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email này đã được đăng ký trước đó'
                })
            
            # Tạo đăng ký mới
            Newsletter.objects.create(email=email)
            logger.info(f"Successfully created newsletter subscription for email: {email}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Đăng ký nhận tin thành công!'
            })
        except Exception as e:
            logger.error(f"Error in newsletter subscription: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Có lỗi xảy ra. Vui lòng thử lại sau!'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Phương thức không được hỗ trợ'
    })

def submit_consultation(request):
    if request.method == 'POST':
        # Xử lý form đăng ký tư vấn
        if 'full_name' in request.POST:
            full_name = request.POST.get('full_name', '').strip()
            phone = request.POST.get('phone', '').strip()
            address = request.POST.get('address', '').strip()
            content = request.POST.get('content', '').strip()
            
            errors = {}
            
            # Validate full name
            if not full_name:
                errors['full_name'] = 'Vui lòng nhập họ và tên'
                
            # Validate phone number (10 digits)
            if not phone:
                errors['phone'] = 'Vui lòng nhập số điện thoại'
            elif not re.match(r'^\d{10}$', phone):
                errors['phone'] = 'Số điện thoại phải có 10 chữ số'
                
            # Validate address
            if not address:
                errors['address'] = 'Vui lòng nhập địa chỉ lắp đặt'
                
            # Validate content
            if not content:
                errors['content'] = 'Vui lòng nhập nội dung yêu cầu'
                
            if errors:
                return JsonResponse({
                    'status': 'error',
                    'errors': errors
                })
                
            try:
                consultation = Consultation.objects.create(
                    full_name=full_name,
                    address=address,
                    phone=phone,
                    content=content
                )
                return JsonResponse({
                    'status': 'success',
                    'message': 'Cảm ơn bạn đã đăng ký tư vấn. Chúng tôi sẽ liên hệ với bạn trong thời gian sớm nhất!'
                })
            except Exception as e:
                logger.error(f"Error creating consultation: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Có lỗi xảy ra. Vui lòng thử lại sau!'
                })
        
        # Xử lý form đăng ký nhận tin
        elif 'newsletter_email' in request.POST:
            try:
                email = request.POST.get('email', '').strip()
                logger.info(f"Received newsletter subscription request for email: {email}")
                
                if not email:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Vui lòng nhập địa chỉ email'
                    })
                
                if not validate_email(email):
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Địa chỉ email không hợp lệ'
                    })
                
                # Kiểm tra email đã tồn tại chưa
                if Newsletter.objects.filter(email=email).exists():
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Email này đã được đăng ký trước đó'
                    })
                
                # Tạo đăng ký mới
                Newsletter.objects.create(email=email)
                logger.info(f"Successfully created newsletter subscription for email: {email}")
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Đăng ký nhận tin thành công!'
                })
            except Exception as e:
                logger.error(f"Error in newsletter subscription: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Có lỗi xảy ra. Vui lòng thử lại sau!'
                })
    
    return redirect('home')

def contact_view(request):
    initial = {}
    if request.user.is_authenticated:
        # Lấy thông tin từ user và userprofile nếu có
        initial['full_name'] = getattr(request.user, 'userprofile', None) and request.user.userprofile.full_name or request.user.get_full_name() or request.user.username
        initial['email'] = request.user.email or ''
        initial['phone'] = getattr(request.user, 'userprofile', None) and request.user.userprofile.phone or ''
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gửi liên hệ thành công! Chúng tôi sẽ phản hồi sớm nhất.')
            return redirect('consultations:contact')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin.')
    else:
        form = ContactForm(initial=initial)
    return render(request, 'consultations/contact.html', {'form': form})

@require_GET
@staff_member_required
def unread_consultation_count(request):
    count = Consultation.objects.filter(status='pending').count()
    return JsonResponse({'unread': count})

@staff_member_required
def admin_consultation_list(request):
    status = request.GET.get('status', '')
    q = request.GET.get('q', '').strip()
    page = request.GET.get('page', 1)
    consultations = Consultation.objects.all()
    if status:
        consultations = consultations.filter(status=status)
    if q:
        consultations = consultations.filter(
            Q(full_name__icontains=q) |
            Q(phone__icontains=q) |
            Q(address__icontains=q) |
            Q(content__icontains=q)
        )
    consultations = consultations.order_by('-created_at')
    paginator = Paginator(consultations, 10)
    page_obj = paginator.get_page(page)
    return render(request, 'consultations/admin_consultation_list.html', {
        'consultations': page_obj.object_list,
        'page_obj': page_obj,
        'status': status,
        'q': q,
    })

@staff_member_required
def admin_consultation_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        if status in dict(Consultation.STATUS_CHOICES):
            consultation.status = status
        consultation.notes = notes
        consultation.save()
        return render(request, 'consultations/admin_consultation_detail.html', {
            'consultation': consultation,
            'success': True
        })
    return render(request, 'consultations/admin_consultation_detail.html', {
        'consultation': consultation
    })
