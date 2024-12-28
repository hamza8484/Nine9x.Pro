from django.db import models
from django.utils.translation import gettext as _  # Import gettext for translation

class Unit(models.Model):
    name_lo = models.CharField(_("الاسم عربي"), max_length=50)
    name_fk = models.CharField(_("الاسم الاجنبي"), max_length=50)
    codeUnit = models.CharField(_("رمز الوحدة"), max_length=50)

    def __str__(self):
        return self.name_lo

class Items_type(models.Model):
    name_lo = models.CharField(_("الاسم عربي"), max_length=50)
    name_fk = models.CharField(_("الاسم الاجنبي"), max_length=50)

    def __str__(self):
        return self.name_lo

class Store(models.Model):
    name_lo = models.CharField(_("الاسم عربي"), max_length=50)
    name_fk = models.CharField(_("الاسم الاجنبي"), max_length=50)
    is_stop = models.BooleanField(default=True, verbose_name=_("مغلق"))

    def __str__(self):
        return self.name_lo



class ProgramSettings(models.Model):
    # إعدادات الشعار
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    
    # إعدادات الألوان
    sidebar_color = models.CharField(max_length=7, default='#2980b9')  # اللون الافتراضي للـ sidebar
    navbar_color = models.CharField(max_length=7, default='#34495e')  # اللون الافتراضي للـ navbar
    footer_color = models.CharField(max_length=7, default='#2c3e50')  # اللون الافتراضي للـ footer
    text_color = models.CharField(max_length=7, default='#ffffff')  # لون النصوص بشكل عام
    link_color = models.CharField(max_length=7, default='#1abc9c')  # لون الروابط
    
    # إعدادات حجم الخط
    sidebar_font_size = models.IntegerField(default=14)  # حجم الخط في الـ sidebar
    navbar_font_size = models.IntegerField(default=16)  # حجم الخط في الـ navbar
    footer_font_size = models.IntegerField(default=12)  # حجم الخط في الـ footer
    body_font_size = models.IntegerField(default=14)  # حجم الخط في باقي الصفحة

    # إعدادات الشفافية
    text_opacity = models.FloatField(default=1.0)  # الشفافية الافتراضية للنصوص
    
    def __str__(self):
        return "Settings for the program"
