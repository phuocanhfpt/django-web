# Generated by Django 5.2.1 on 2025-05-27 16:52

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Họ và tên')),
                ('address', models.CharField(max_length=200, verbose_name='Địa chỉ lắp đặt')),
                ('phone', models.CharField(max_length=20, verbose_name='Điện thoại liên hệ')),
                ('content', models.TextField(verbose_name='Nội dung nhu cầu')),
                ('status', models.CharField(choices=[('pending', 'Chờ xử lý'), ('processing', 'Đang xử lý'), ('completed', 'Đã hoàn thành'), ('cancelled', 'Đã hủy')], default='pending', max_length=20, verbose_name='Trạng thái')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ngày tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Cập nhật lúc')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Ghi chú')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Đăng ký tư vấn',
                'verbose_name_plural': 'Đăng ký tư vấn',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Họ và tên')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Số điện thoại')),
                ('message', models.TextField(verbose_name='Nội dung liên hệ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày gửi')),
                ('is_read', models.BooleanField(default=False, verbose_name='Đã đọc')),
            ],
            options={
                'verbose_name': 'Liên hệ',
                'verbose_name_plural': 'Liên hệ',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FooterMenuGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Tiêu đề nhóm')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Thứ tự')),
                ('is_active', models.BooleanField(default=True, verbose_name='Đang hoạt động')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Nhóm menu footer',
                'verbose_name_plural': 'Nhóm menu footer',
                'ordering': ['order', 'title'],
            },
        ),
        migrations.CreateModel(
            name='FooterSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default='LẮP CAMERA HCM', max_length=100)),
                ('description', models.TextField(default='Chuyên cung cấp, lắp đặt camera giám sát, thiết bị an ninh tại TP.HCM và toàn quốc.')),
                ('address', models.CharField(default='C16/4/5D Liên Ấp 234, Vĩnh Lộc A, Bình Chánh, Tp.HCM', max_length=200)),
                ('hotline', models.CharField(default='08.2222.3000', max_length=20)),
                ('technical_support', models.CharField(default='083.660.6699', max_length=20)),
                ('business_phone', models.CharField(default='090.167.1179', max_length=20)),
                ('email', models.EmailField(default='lapcamerahcm.vn@gmail.com', max_length=254)),
                ('facebook_url', models.URLField(blank=True)),
                ('youtube_url', models.URLField(blank=True)),
                ('instagram_url', models.URLField(blank=True)),
                ('tiktok_url', models.URLField(blank=True)),
                ('zalo_url', models.URLField(blank=True, verbose_name='Zalo URL')),
                ('working_hours', models.CharField(default='8h - 18h (T2 - CN)', max_length=100)),
                ('copyright_text', models.CharField(default='© 2018 - {} LẮP CAMERA HCM. All rights reserved.', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cài đặt Footer',
                'verbose_name_plural': 'Cài đặt Footer',
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=True, verbose_name='Đang hoạt động')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ngày đăng ký')),
            ],
            options={
                'verbose_name': 'Đăng ký nhận tin',
                'verbose_name_plural': 'Đăng ký nhận tin',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FooterMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Tiêu đề')),
                ('url', models.CharField(max_length=200, verbose_name='Đường dẫn')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Thứ tự')),
                ('is_active', models.BooleanField(default=True, verbose_name='Đang hoạt động')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='consultations.footermenugroup', verbose_name='Nhóm menu')),
            ],
            options={
                'verbose_name': 'Menu footer',
                'verbose_name_plural': 'Menu footer',
                'ordering': ['group', 'order', 'title'],
            },
        ),
    ]
