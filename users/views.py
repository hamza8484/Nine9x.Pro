from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import SettingsForm
from django.core.files.storage import FileSystemStorage
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, UserRegisterForm
from django.utils import translation
from django.utils.translation import gettext_lazy as _  # Import gettext_lazy for translation

def home(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('login')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'configrate/templates/configrate/users.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('تم لإنشاء الحساب ل : %(username)s') % {'username': username})
            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = _('لقد أرسلنا إليك تعليمات عبر البريد الإلكتروني لإعداد كلمة المرور الخاصة بك، '
                        'إذا كان هناك حساب بالبريد الإلكتروني الذي أدخلته. يجب أن تستقبلهم قريبا. '
                        'إذا لم تتلق بريدًا إلكترونيًا، فيرجى التأكد من إدخال العنوان الذي قمت بالتسجيل به،'
                        'وتحقق من مجلد الرسائل غير المرغوب فيها.')
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = _('تم تغيير كلمة المرور بنجاح')
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    # تحقق إذا كان المستخدم لديه ملف تعريف، وإذا لم يكن لديه، قم بإنشائه
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        # التحديث على نموذج المستخدم ونموذج الملف الشخصي
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # حفظ نموذج المستخدم
            profile_form.save()  # حفظ نموذج الملف الشخصي
            messages.success(request, _('تم تحديث الصفحة بنجاح'))
            return redirect('users-profile')  # إعادة التوجيه إلى صفحة الملف الشخصي
    else:
        # تحميل النماذج بشكل افتراضي (بدون بيانات POST)
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

    
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.'))
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


@login_required
def settings_view(request):
    if 'language' in request.session:
        translation.activate(request.session['language'])
    else:
        translation.activate('en')

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            language = form.cleaned_data['language']
            theme = form.cleaned_data['theme']
            app_icon = form.cleaned_data['app_icon']
            notifications_enabled = form.cleaned_data['notifications_enabled']

            request.session['language'] = language
            request.session['theme'] = theme
            if app_icon:
                fs = FileSystemStorage()
                filename = fs.save(app_icon.name, app_icon)
                app_icon_url = fs.url(filename)
                request.session['app_icon_url'] = app_icon_url
            request.session['notifications_enabled'] = notifications_enabled

            messages.success(request, _('تم حفظ الإعدادات بنجاح'))

            return redirect('settings')
    else:
        form = SettingsForm()

    return render(request, 'users/settings.html', {'form': form})


def change_language(request):
    if 'language' in request.GET:
        language = request.GET['language']
        request.session['language'] = language
        translation.activate(language)
    return redirect(request.META.get('HTTP_REFERER', 'index'))
