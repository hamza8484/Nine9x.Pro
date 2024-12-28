from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # تحقق مما إذا كان المستخدم لديه بالفعل ملف تعريف
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()  # حفظ الملف الشخصي
    except Profile.DoesNotExist:
        pass  # في حال عدم وجود الملف الشخصي
