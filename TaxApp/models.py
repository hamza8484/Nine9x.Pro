from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _  # استيراد _()


class Tax(models.Model):
    # اسم الضريبة يجب أن يكون فريدًا
    name = models.CharField(max_length=100, unique=True, verbose_name=_('اسم الضريبة'))
    
    # نسبة الضريبة مع التحقق من أنها بين 0 و 100
    rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name=_('نسبة الضريبة'),
        validators=[MinValueValidator(0), MaxValueValidator(100)]  # التحقق من النسبة بين 0 و 100
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("الضريبة")
        verbose_name_plural = _("الضرائب")
