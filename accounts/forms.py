from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    full_name = forms.CharField(max_length=150, required=True, label='Họ và tên')
    phone = forms.CharField(max_length=20, required=False, label='Số điện thoại')

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user 