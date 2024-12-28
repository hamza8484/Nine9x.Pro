from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _  # إضافة استيراد الترجمة

class BaseModel(models.Model):
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=False, auto_now=True)
    modified_at = models.DateTimeField(_("تاريخ التعديل"), auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)s_createdby", null=True, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)s_modifiedby", null=True, blank=True)

    class Meta:
        abstract = True
