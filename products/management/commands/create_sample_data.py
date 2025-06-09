from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Brand, Product, HeroSlide, Contact, FAQ, Promotion
from posts.models import PostCategory, Post
from django.utils.text import slugify
from decimal import Decimal
import random
from datetime import datetime, timedelta
from django.core.files.base import ContentFile
from django.conf import settings
import os
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates sample data for the website'

    def handle(self, *args, **kwargs):
        # Đường dẫn ảnh mặc định
        default_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'placeholder.jpg')
        with open(default_image_path, 'rb') as f:
            default_image_content = f.read()

        # Create categories
        categories_data = [
            {
                'name': 'Camera Giám Sát',
                'description': 'Camera giám sát an ninh chuyên nghiệp',
                'featured': True,
                'show_on_home': True
            },
            {
                'name': 'Đầu Ghi Hình',
                'description': 'Đầu ghi hình camera giám sát',
                'featured': True,
                'show_on_home': True
            },
            {
                'name': 'Phụ Kiện Camera',
                'description': 'Phụ kiện lắp đặt camera',
                'featured': False,
                'show_on_home': True
            },
            {
                'name': 'Camera Wifi',
                'description': 'Camera wifi không dây',
                'featured': True,
                'show_on_home': True
            },
            {
                'name': 'Camera IP',
                'description': 'Camera IP công nghệ mới',
                'featured': True,
                'show_on_home': True
            },
            {
                'name': 'Camera Dome',
                'description': 'Camera dome chống phá hoại',
                'featured': False,
                'show_on_home': True
            },
            {
                'name': 'Camera Thân',
                'description': 'Camera thân chuyên nghiệp',
                'featured': False,
                'show_on_home': True
            },
            {
                'name': 'Camera Ẩn',
                'description': 'Camera ẩn mini',
                'featured': False,
                'show_on_home': True
            },
            {
                'name': 'Camera Hồng Ngoại',
                'description': 'Camera hồng ngoại ban đêm',
                'featured': True,
                'show_on_home': True
            },
            {
                'name': 'Camera Ngoài Trời',
                'description': 'Camera ngoài trời chống nước',
                'featured': True,
                'show_on_home': True
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'featured': cat_data['featured'],
                    'show_on_home': cat_data['show_on_home']
                }
            )
            if created or not category.image:
                try:
                    category.image.save('placeholder.jpg', ContentFile(default_image_content), save=True)
                except Exception:
                    pass
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create brands
        brands_data = [
            {
                'name': 'Hikvision',
                'description': 'Thương hiệu camera giám sát số 1 thế giới'
            },
            {
                'name': 'Dahua',
                'description': 'Thương hiệu camera giám sát hàng đầu'
            },
            {
                'name': 'Kbvision',
                'description': 'Thương hiệu camera giám sát chất lượng cao'
            },
            {
                'name': 'Ezviz',
                'description': 'Thương hiệu camera wifi thông minh'
            },
            {
                'name': 'Uniview',
                'description': 'Thương hiệu camera giám sát công nghệ mới'
            }
        ]

        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=brand_data['name'],
                defaults={
                    'description': brand_data['description']
                }
            )
            if created or not brand.logo:
                try:
                    brand.logo.save('placeholder.jpg', ContentFile(default_image_content), save=True)
                except Exception:
                    pass
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created brand: {brand.name}'))

        # Create products
        categories = Category.objects.all()
        brands = Brand.objects.all()
        
        for i in range(1, 501):
            category = random.choice(categories)
            brand = random.choice(brands)
            name = f'Camera {brand.name} {category.name} {i}'
            price = random.randint(500000, 10000000)
            sale_price = price * 0.9 if random.random() < 0.3 else None
            
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'brand': brand,
                    'price': price,
                    'sale_price': sale_price,
                    'short_description': f'Camera {brand.name} {category.name} chất lượng cao',
                    'description': f'''
                    <h2>Thông số kỹ thuật</h2>
                    <ul>
                        <li>Độ phân giải: 2MP/4MP/8MP</li>
                        <li>Góc nhìn: 90°</li>
                        <li>Hồng ngoại: 30m</li>
                        <li>Chống nước: IP67</li>
                        <li>Chống phá hoại: IK10</li>
                        <li>Nguồn điện: DC12V/AC24V</li>
                    </ul>
                    <h2>Tính năng</h2>
                    <ul>
                        <li>Phát hiện chuyển động</li>
                        <li>Phát hiện xâm nhập</li>
                        <li>Phát hiện âm thanh</li>
                        <li>Phát hiện khói</li>
                        <li>Phát hiện nhiệt</li>
                    </ul>
                    ''',
                    'featured': random.random() < 0.2,
                    'status': True
                }
            )
            if created or not product.image:
                try:
                    product.image.save(f'product_{i}_placeholder.jpg', ContentFile(default_image_content), save=True)
                except Exception:
                    pass
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))

        # Create hero slides
        slides_data = [
            {
                'title': 'Lắp Đặt Camera Giám Sát Chuyên Nghiệp',
                'subtitle': 'Bảo vệ an ninh 24/7',
                'description': 'Dịch vụ lắp đặt camera giám sát chuyên nghiệp, uy tín, giá rẻ',
                'button_text': 'Tư Vấn Ngay',
                'button_url': '/contact/',
                'order': 1
            },
            {
                'title': 'Camera Wifi Thông Minh',
                'subtitle': 'Giải pháp an ninh hiện đại',
                'description': 'Camera wifi thông minh, dễ lắp đặt, dễ sử dụng',
                'button_text': 'Xem Thêm',
                'button_url': '/products/camera-wifi/',
                'order': 2
            },
            {
                'title': 'Camera Công Nghệ AI',
                'subtitle': 'Bảo vệ thông minh',
                'description': 'Camera giám sát tích hợp trí tuệ nhân tạo',
                'button_text': 'Tìm Hiểu',
                'button_url': '/products/camera-ai/',
                'order': 3
            }
        ]

        for idx, slide_data in enumerate(slides_data, 1):
            slide, created = HeroSlide.objects.get_or_create(
                title=slide_data['title'],
                defaults=slide_data
            )
            if created or not slide.image:
                try:
                    slide.image.save(f'heroslide_{idx}_placeholder.jpg', ContentFile(default_image_content), save=True)
                except Exception:
                    pass
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created slide: {slide.title}'))

        # Create FAQs
        faqs_data = [
            {
                'question': 'Lắp đặt camera giám sát có cần giấy phép không?',
                'answer': 'Theo quy định hiện hành, việc lắp đặt camera giám sát trong nhà không cần giấy phép. Tuy nhiên, nếu lắp đặt camera giám sát nơi công cộng hoặc khu vực có nhiều người qua lại, bạn cần xin giấy phép từ cơ quan có thẩm quyền.'
            },
            {
                'question': 'Camera giám sát có thể xem qua điện thoại không?',
                'answer': 'Có, hầu hết các camera giám sát hiện nay đều hỗ trợ xem qua điện thoại thông qua ứng dụng di động. Bạn chỉ cần cài đặt ứng dụng tương ứng với thương hiệu camera và kết nối internet là có thể xem camera từ bất kỳ đâu.'
            },
            {
                'question': 'Thời gian lưu trữ hình ảnh là bao lâu?',
                'answer': 'Thời gian lưu trữ hình ảnh phụ thuộc vào dung lượng ổ cứng của đầu ghi hình và số lượng camera. Thông thường, với ổ cứng 1TB và 4 camera, thời gian lưu trữ có thể lên đến 30 ngày.'
            }
        ]

        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created FAQ: {faq.question}'))

        # Create promotions
        promotions_data = [
            {
                'name': 'Khuyến mãi tháng 5',
                'code': 'MAY2024',
                'description': 'Giảm giá 20% cho tất cả sản phẩm camera giám sát',
                'type': 'percentage',
                'discount': 20,
                'min_purchase': 1000000,
                'max_discount': 2000000,
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=30),
                'status': True,
                'total_uses': 100,
                'uses_per_customer': 1
            },
            {
                'name': 'Khuyến mãi combo',
                'code': 'COMBO2024',
                'description': 'Giảm giá 500.000đ khi mua combo camera + đầu ghi hình',
                'type': 'fixed',
                'discount': 500000,
                'min_purchase': 2000000,
                'max_discount': 500000,
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=15),
                'status': True,
                'total_uses': 50,
                'uses_per_customer': 1
            }
        ]

        for promo_data in promotions_data:
            promotion, created = Promotion.objects.get_or_create(
                code=promo_data['code'],
                defaults=promo_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created promotion: {promotion.name}'))

        # Create post categories
        post_categories_data = [
            {
                'name': 'Tin Tức',
                'description': 'Tin tức về camera giám sát',
                'slug': 'tin-tuc'
            },
            {
                'name': 'Hướng Dẫn',
                'description': 'Hướng dẫn lắp đặt và sử dụng camera',
                'slug': 'huong-dan'
            },
            {
                'name': 'Tư Vấn',
                'description': 'Tư vấn chọn mua camera phù hợp',
                'slug': 'tu-van'
            },
            {
                'name': 'Công Nghệ',
                'description': 'Công nghệ camera giám sát mới',
                'slug': 'cong-nghe'
            },
            {
                'name': 'Bảo Mật',
                'description': 'Vấn đề bảo mật camera giám sát',
                'slug': 'bao-mat'
            }
        ]

        for cat_data in post_categories_data:
            category, created = PostCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created post category: {category.name}'))

        # Create posts
        categories = PostCategory.objects.all()
        for i in range(1, 101):
            category = random.choice(categories)
            title = f'Bài viết {i} về {category.name}'
            post, created = Post.objects.get_or_create(
                title=title,
                defaults={
                    'category': category,
                    'short_description': f'Mô tả ngắn cho bài viết {i}',
                    'content': f'''
                    <h2>Nội dung bài viết {i}</h2>
                    <p>Đây là nội dung chi tiết của bài viết {i} về {category.name}.</p>
                    <h3>Phần 1</h3>
                    <p>Nội dung phần 1 của bài viết.</p>
                    <h3>Phần 2</h3>
                    <p>Nội dung phần 2 của bài viết.</p>
                    <h3>Kết luận</h3>
                    <p>Kết luận của bài viết.</p>
                    ''',
                    'featured': random.random() < 0.2
                }
            )
            if created:
                # Gán ảnh mặc định nếu chưa có
            if not post.image:
                    post.image.save(f'post_{i}_placeholder.jpg', ContentFile(default_image_content), save=True)
                self.stdout.write(self.style.SUCCESS(f'Created post: {post.title}'))

        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write('No admin user found. Please create a superuser first.')
            return

        # Create contacts
        for i in range(1, 11):
            Contact.objects.get_or_create(
                name=f'Khách hàng {i}',
                email=f'customer{i}@example.com',
                phone=f'09000000{i:02d}',
                subject=f'Yêu cầu tư vấn {i}',
                message=f'Tôi muốn được tư vấn về sản phẩm camera {i}',
                status='pending',
                replied=False
            )
        self.stdout.write(self.style.SUCCESS('Created 10 contacts'))

        # Đảm bảo các bảng khác cũng có dữ liệu mẫu nếu cần

        # Create FAQs (đã có ở trên)
        # Create promotions (đã có ở trên)
        # Đảm bảo các bảng khác cũng có dữ liệu mẫu nếu cần 