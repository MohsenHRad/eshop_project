from django.contrib.auth import login, logout
from django.http import Http404, HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

from account_module.forms import RegisterForm, LoginForm, ForgetPassForm, ResetPassForm
from utils.email_service import send_email
from .models import User


# Create your views here.

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user_exist: bool = User.objects.filter(email__iexact=user_email).exists()
            if user_exist:
                register_form.add_error('email', 'ایمیل وارد شده تکراری میباشد')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email
                )
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user},
                           'emails/activate_account.html')
                return redirect(reverse('login_page'))
                # todo: send email active code

        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo : show access message to user
                return redirect(reverse('login_page'))
            else:
                pass
                # todo : show your account was activated message to user

        else:
            raise Http404("fuck you :)")


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    # login_form.add_error('email', 'حساب کاربری شما فعال نمیباشد ')
                    raise HttpResponseNotAllowed
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))

                    else:
                        login_form.add_error('email', 'کاربری با مشخصات وارده شده یافت نشد')

        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)


class ForgetPassword(View):
    def get(self, request):
        forget_pass_form = ForgetPassForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request):
        forget_pass_form = ForgetPassForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                pass

        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)


class ResetPassword(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))
        reset_password_form = ResetPassForm()

        context = {'reset_pass_form': reset_password_form,
                   'user': user
                   }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_password_form = ResetPassForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_password_form.is_valid():
            user_current_password = reset_password_form.cleaned_data.get('current_password')
            is_password_correct = user.check_password(user_current_password)
            if is_password_correct:
                if user is None:
                    return redirect(reverse('login_page'))
                user_new_password = reset_password_form.cleaned_data.get('new_password')
                user.set_password(user_new_password)
                user.email_active_code = get_random_string(72)
                user.is_active = True
                user.save()

                return redirect(reverse('login_page'))

            else:
                reset_password_form.add_error('current_password', 'اطلاعات وارد شده صحیح نمی باشد پسورد')
                context = {'reset_pass_form': reset_password_form,
                           'user': user
                           }
                return render(request, 'account_module/login.html', context)


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))
