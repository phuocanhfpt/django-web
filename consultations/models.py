from django.db import models
from django.utils import timezone

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('completed', 'Đã hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    full_name = models.CharField(max_length=100, verbose_name='Họ và tên')
    address = models.CharField(max_length=200, verbose_name='Địa chỉ lắp đặt')
    phone = models.CharField(max_length=20, verbose_name='Điện thoại liên hệ')
    content = models.TextField(verbose_name='Nội dung nhu cầu')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Trạng thái'
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lúc')
    notes = models.TextField(blank=True, null=True, verbose_name='Ghi chú')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Đăng ký tư vấn'
        verbose_name_plural = 'Đăng ký tư vấn'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.phone}"

class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Ngày đăng ký')

    class Meta:
        verbose_name = 'Đăng ký nhận tin'
        verbose_name_plural = 'Đăng ký nhận tin'
        ordering = ['-created_at']

    def __str__(self):
        return self.email

class FooterMenuGroup(models.Model):
    title = models.CharField(max_length=100, verbose_name='Tiêu đề nhóm')
    order = models.PositiveIntegerField(default=0, verbose_name='Thứ tự')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nhóm menu footer'
        verbose_name_plural = 'Nhóm menu footer'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class FooterMenu(models.Model):
    group = models.ForeignKey(FooterMenuGroup, on_delete=models.CASCADE, related_name='menus', verbose_name='Nhóm menu')
    title = models.CharField(max_length=100, verbose_name='Tiêu đề')
    url = models.CharField(max_length=200, verbose_name='Đường dẫn')
    order = models.PositiveIntegerField(default=0, verbose_name='Thứ tự')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Menu footer'
        verbose_name_plural = 'Menu footer'
        ordering = ['group', 'order', 'title']

    def __str__(self):
        return f"{self.group.title} - {self.title}"

class FooterSettings(models.Model):
    company_name = models.CharField(max_length=100, default="LẮP CAMERA HCM")
    description = models.TextField(default="Chuyên cung cấp, lắp đặt camera giám sát, thiết bị an ninh tại TP.HCM và toàn quốc.")
    address = models.CharField(max_length=200, default="C16/4/5D Liên Ấp 234, Vĩnh Lộc A, Bình Chánh, Tp.HCM")
    hotline = models.CharField(max_length=20, default="08.2222.3000")
    technical_support = models.CharField(max_length=20, default="083.660.6699")
    business_phone = models.CharField(max_length=20, default="090.167.1179")
    email = models.EmailField(default="lapcamerahcm.vn@gmail.com")
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    zalo_url = models.URLField(blank=True, verbose_name='Zalo URL')
    working_hours = models.CharField(max_length=100, default="8h - 18h (T2 - CN)")
    copyright_text = models.CharField(max_length=200, default="© 2018 - {} LẮP CAMERA HCM. All rights reserved.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cài đặt Footer"
        verbose_name_plural = "Cài đặt Footer"

    def __str__(self):
        return "Cài đặt Footer"

    def get_copyright_text(self):
        current_year = timezone.now().year
        return self.copyright_text.format(current_year)

class Contact(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='Họ và tên')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
    message = models.TextField(verbose_name='Nội dung liên hệ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày gửi')
    is_read = models.BooleanField(default=False, verbose_name='Đã đọc')

    class Meta:
        verbose_name = 'Liên hệ'
        verbose_name_plural = 'Liên hệ'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.email}"
