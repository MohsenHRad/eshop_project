from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from account_module.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_author']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'

            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Address',
            }),
            'about_author': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'About',
            }),

        }
        labels = {
            'first_name': 'نام  ',
            'last_name': 'نام خانوادگی  ',
            'avatar': 'تصویر پروفایل  ',
            'address': 'آدرس  ',
            'about_author': 'درباره شخص  ',

        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی ',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label='تکرار کلمه عبور جدید',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError("اطلاعات وارد شده صحیح نمییاشد")
