from django.db import models

# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='Tên website')
    slogan = models.CharField(max_length=200, blank=True, verbose_name='Slogan')
    description = models.TextField(blank=True, verbose_name='Mô tả ngắn')
    address = models.CharField(max_length=255, blank=True, verbose_name='Địa chỉ')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Điện thoại')
    email = models.EmailField(blank=True, verbose_name='Email')
    logo = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='Logo')
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='Favicon')
    meta_title = models.CharField(max_length=255, blank=True, verbose_name='Meta Title')
    meta_description = models.TextField(max_length=255, blank=True, verbose_name='Meta Description')
    meta_keywords = models.CharField(max_length=500, blank=True, verbose_name='Meta Keywords')
    tags = models.CharField(max_length=500, blank=True, help_text='Nhập các từ khóa, phân cách bằng dấu phẩy')
    google_analytics_code = models.TextField(blank=True, verbose_name='Google Analytics Code', help_text='Dán toàn bộ mã script Analytics')
    google_search_console_code = models.TextField(blank=True, verbose_name='Google Search Console Code', help_text='Dán toàn bộ meta tag xác minh')
    facebook_url = models.URLField(blank=True, verbose_name='Facebook')
    youtube_url = models.URLField(blank=True, verbose_name='Youtube')
    instagram_url = models.URLField(blank=True, verbose_name='Instagram')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cài đặt website'
        verbose_name_plural = 'Cài đặt website'

    def __str__(self):
        return self.site_name or 'Cài đặt website'

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
