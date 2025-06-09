from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
import unicodedata
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db.models import Avg
from ckeditor_uploader.fields import RichTextUploadingField

def vn_slugify(value):
    """
    Convert Vietnamese text to slug
    Example: "Sản phẩm mới" -> "san-pham-moi"
    """
    value = str(value)
    # Convert to ASCII
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    # Convert to lowercase
    value = value.lower()
    # Replace spaces with hyphens
    value = value.replace(' ', '-')
    # Remove special characters
    value = ''.join(c for c in value if c.isalnum() or c == '-')
    # Remove multiple hyphens
    while '--' in value:
        value = value.replace('--', '-')
    # Remove leading/trailing hyphens
    value = value.strip('-')
    return value

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    show_on_home = models.BooleanField(default=False, verbose_name='Hiển thị trang chủ')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Nhập các từ khóa, phân cách bằng dấu phẩy")
    meta_description = models.TextField(max_length=160, blank=True, help_text="Mô tả ngắn cho SEO (tối đa 160 ký tự)")

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = vn_slugify(self.name)
        super().save(*args, **kwargs)

    def get_tags_list(self):
        """Trả về danh sách các tags đã được tách"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/%Y/%m/%d', blank=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = vn_slugify(self.name)
        super().save(*args, **kwargs)

class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class, ví dụ: fa-wifi")
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Tính năng'
        verbose_name_plural = 'Các tính năng'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    short_description = models.TextField(blank=True)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    featured = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # New fields for filtering
    has_wifi = models.BooleanField(default=False, verbose_name='Có Wifi')
    has_night_vision = models.BooleanField(default=False, verbose_name='Có hồng ngoại')
    is_waterproof = models.BooleanField(default=False, verbose_name='Chống nước')
    
    features = models.ManyToManyField('Feature', blank=True, related_name='products')
    accessories = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='accessory_for', verbose_name='Sản phẩm bán kèm')
    
    tags = models.CharField(max_length=500, blank=True, help_text="Nhập các từ khóa, phân cách bằng dấu phẩy")
    meta_description = models.TextField(max_length=160, blank=True, help_text="Mô tả ngắn cho SEO (tối đa 160 ký tự)")
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'category_slug': self.category.slug, 'slug': self.slug})
        
    def get_discount_percentage(self):
        if self.sale_price and self.price:
            discount = ((self.price - self.sale_price) / self.price) * 100
            return round(discount)
        return 0

    @property
    def average_rating(self):
        return self.ratings.aggregate(avg=Avg('rating'))['avg'] or 0

    @property
    def ratings_count(self):
        return self.ratings.count()

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='hero/%Y/%m/%d')
    link = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order',)
        verbose_name = 'hero slide'
        verbose_name_plural = 'hero slides'

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')
    replied = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    def __str__(self):
        return f"{self.name} - {self.subject}"

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order',)
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question

class Promotion(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=0)
    type = models.CharField(max_length=20, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed')], default='percentage')
    start_date = models.DateField()
    end_date = models.DateField()
    min_purchase = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    max_discount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    uses_per_customer = models.PositiveIntegerField(null=True, blank=True)
    total_uses = models.PositiveIntegerField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'promotion'
        verbose_name_plural = 'promotions'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = vn_slugify(self.name)
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name or self.user.username

class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_admin_reply = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Bình luận của {self.user} cho {self.product}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created']

    def __str__(self):
        return f"{self.user} - {self.product} ({self.rating} sao)"

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
