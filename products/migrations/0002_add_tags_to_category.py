from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='tags',
            field=models.CharField(blank=True, help_text='Nhập các từ khóa, phân cách bằng dấu phẩy', max_length=500),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=models.TextField(blank=True, help_text='Mô tả ngắn cho SEO (tối đa 160 ký tự)', max_length=160),
        ),
    ] 