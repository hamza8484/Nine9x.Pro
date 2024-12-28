from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _  # استيراد الترجمة

from .models import Profile

# نموذج التسجيل للمستخدم
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': _('الأسم الأول'),
                                                               'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': _('الإسم الثاني'),
                                                              'class': 'form-control'}))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': _('إسم المستخدم'),
                                                             'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': _('الإيميل'),
                                                           'class': 'form-control'}))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': _('كلمة المرور'),
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password'}))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': _('تأكيد كلمة المرور'),
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

# نموذج تسجيل الدخول
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': _('إسم المستخدم'),
                                                             'class': 'form-control'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': _('كلمة المرور'),
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password'}))
    remember_me = forms.BooleanField(required=False, label=_("تذكرني"))

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']

# نموذج تعديل المستخدم
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']  # استخدم 'email' بدلاً من 'الإيميل'

# نموذج تعديل الملف الشخصي
class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

# نموذج التسجيل مع الملف الشخصي
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    bio = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': _('أخبرنا عن نفسك')}), required=False)
    avatar = forms.ImageField(required=False)  # لا نحتاج لجعل هذا الحقل مطلوبًا

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'bio', 'avatar']

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        # تحقق مما إذا كان هناك ملف شخصي للمستخدم
        profile, created = Profile.objects.get_or_create(user=user)
        profile.bio = self.cleaned_data.get('bio', '')

        # التعامل مع صورة الـ avatar
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            profile.avatar = avatar
        else:
            # تعيين صورة افتراضية في حال لم يقم المستخدم برفع صورة
            profile.avatar = 'default.jpg'  # تأكد من أنك قد وضعت صورة افتراضية في مجلد الصور لديك

        profile.save()

        return user


# نموذج إعدادات المستخدم
class SettingsForm(forms.Form):
    LANGUAGE_CHOICES = (
        ('en', _('إنجليزي')),
        ('ar', _('عربي')),
    )
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, label=_("اللغة"))

    THEME_CHOICES = (
        ('light', _('إضاءة بيضاء')),
        ('dark', _('إضاءة سوداء')),
    )
    theme = forms.ChoiceField(choices=THEME_CHOICES, label=_("الخلفية"))

    app_icon = forms.ImageField(required=False, label=_("تغيير الايقونة"))

    notifications_enabled = forms.BooleanField(initial=True, required=False, label=_("تشغيل التنبيهات"))
