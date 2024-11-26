from django import forms

from contact_module.models import ContactUs


class ContactUsForm(forms.Form):
    full_name = forms.CharField(
        label='نام و نام خانوادگی  ',
        max_length=50,
        error_messages={
            'required': 'لطفا نام و نام خانوادگی خود را وارد کنید',
            'max_length': 'نام و نام خانوادگی نباید بیشتر از 50 کاراکتر باشد'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی'
        })
    )
    email = forms.EmailField(
        label='ایمیل  ',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        }))
    title = forms.CharField(
        label='عنوان',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان'
        }))
    message = forms.CharField(
        label='متن پیام',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان',
            'id': 'message'
        })
    )


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['title', 'full_name', 'message', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name'

            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'id': 'message',
                'placeholder': 'Text',
            }),

        }
        labels = {
            'full_name': 'نام و نام خانوادگی شما  ',
            'email': 'ایمیل شما  '
        }

        error_messages={
            'full_name':{
                'required':'نام و نام خانوادگی اجباری می باشد. لطفا وارد کنید'
            }
        }
        # fields = '__all__'
        # exclude = ['response','created_date']


