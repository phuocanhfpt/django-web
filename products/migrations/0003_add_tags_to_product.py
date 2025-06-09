from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0002_add_tags_to_category'),
    ]
    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.CharField(max_length=500, blank=True, help_text='Nhập các từ khóa, phân cách bằng dấu phẩy'),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_description',
            field=models.TextField(max_length=160, blank=True, help_text='Mô tả ngắn cho SEO (tối đa 160 ký tự)'),
        ),
    ] 