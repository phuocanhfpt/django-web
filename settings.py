TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

# --- Cấu hình gửi mail qua Gmail SMTP ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lapcamerahcm.vn@gmail.com'  # <-- Điền email của bạn
EMAIL_HOST_PASSWORD = 'znziydcsgytpyljf'  # <-- Điền App Password của bạn
DEFAULT_FROM_EMAIL = 'Lắp Camera HCM <lapcamerahcm.vn@gmail.com>' 