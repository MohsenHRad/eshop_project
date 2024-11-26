from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ایمیل'
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,

        ],
        # error_messages={
        #
        # }
    )
    password = forms.CharField(
        label='کلمه عبور',
        # required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'پسورد'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ])
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'تکرار پسورد'
        }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "yahoo.com" in email:
            raise ValidationError('یاهو قبول نیست یابو')
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password

        raise ValidationError("کصکش خر کلمه عبور با تکرارش یکی نیست جقی")


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ایمیل'
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ],
        # error_messages={
        #
        # }
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'پسورد'

        }),
        validators=[
            validators.MaxLengthValidator(100)
        ],
    )


class ForgetPassForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ایمیل'
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ],
        # error_messages={
        #
        # }
    )


class ResetPassForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی',
        required=True,
        widget=forms.PasswordInput(attrs={
            'palceholder': 'پسورد فعلی'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ])
    new_password = forms.CharField(
        label='کلمه عبور جدید',
        # required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'پسورد'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ])
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'تکرار پسورد'
        }))
