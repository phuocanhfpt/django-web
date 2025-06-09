from django.core.management.base import BaseCommand
from posts.models import PostCategory, Post
from django.utils.text import slugify
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates sample data for posts app'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = [
            {
                'name': 'Tin tức',
                'description': 'Các tin tức mới nhất về công nghệ'
            },
            {
                'name': 'Hướng dẫn',
                'description': 'Các hướng dẫn sử dụng sản phẩm'
            },
            {
                'name': 'Đánh giá',
                'description': 'Đánh giá sản phẩm'
            }
        ]

        for cat_data in categories:
            category, created = PostCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample posts
        posts = [
            {
                'title': 'iPhone 15 Pro Max - Đánh giá chi tiết',
                'short_description': 'Đánh giá chi tiết về iPhone 15 Pro Max - Flagship mới nhất từ Apple',
                'content': '''
                <h2>Thiết kế</h2>
                <p>iPhone 15 Pro Max sở hữu thiết kế cao cấp với khung viền titan siêu nhẹ và bền bỉ.</p>
                <h2>Màn hình</h2>
                <p>Màn hình 6.7 inch Super Retina XDR với tần số quét 120Hz cho trải nghiệm mượt mà.</p>
                <h2>Hiệu năng</h2>
                <p>Được trang bị chip A17 Pro mạnh mẽ, iPhone 15 Pro Max mang đến hiệu năng đỉnh cao.</p>
                ''',
                'category': 'Đánh giá',
                'status': 'published'
            },
            {
                'title': 'Cách sử dụng tính năng Always On Display trên iPhone',
                'short_description': 'Hướng dẫn chi tiết cách sử dụng và tùy chỉnh Always On Display trên iPhone',
                'content': '''
                <h2>Bật tính năng Always On Display</h2>
                <p>1. Vào Cài đặt > Màn hình & Độ sáng</p>
                <p>2. Bật tùy chọn Always On Display</p>
                <h2>Tùy chỉnh Always On Display</h2>
                <p>Bạn có thể tùy chỉnh các thông tin hiển thị như:</p>
                <ul>
                    <li>Thời gian</li>
                    <li>Ngày tháng</li>
                    <li>Thông báo</li>
                    <li>Widget</li>
                </ul>
                ''',
                'category': 'Hướng dẫn',
                'status': 'published'
            },
            {
                'title': 'Apple ra mắt MacBook Pro M3 mới',
                'short_description': 'Apple vừa chính thức ra mắt dòng MacBook Pro mới với chip M3',
                'content': '''
                <h2>Thông số kỹ thuật</h2>
                <p>MacBook Pro mới được trang bị chip M3 với hiệu năng vượt trội.</p>
                <h2>Giá bán</h2>
                <p>MacBook Pro 14 inch: Từ 999 USD</p>
                <p>MacBook Pro 16 inch: Từ 1,299 USD</p>
                <h2>Thời gian mở bán</h2>
                <p>Sản phẩm sẽ được mở bán vào ngày 7/11/2023.</p>
                ''',
                'category': 'Tin tức',
                'status': 'published'
            }
        ]

        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write('No admin user found. Please create a superuser first.')
            return

        for post_data in posts:
            category = PostCategory.objects.get(name=post_data['category'])
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'slug': slugify(post_data['title']),
                    'short_description': post_data['short_description'],
                    'content': post_data['content'],
                    'category': category,
                    'status': post_data['status']
                }
            )
            if created:
                self.stdout.write(f'Created post: {post.title}') 