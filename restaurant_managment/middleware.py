from django.utils import translation
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # الحصول على اللغة من الـ GET أو الجلسة
        language = request.GET.get('language') or request.session.get('django_language')

        # إذا كانت اللغة موجودة في الـ GET أو الجلسة، نقوم بتفعيلها
        if language and language in dict(settings.LANGUAGES):
            translation.activate(language)
            request.session['django_language'] = language
        else:
            # إذا لم تكن هناك لغة مختارة، نقوم باستخدام اللغة الافتراضية
            translation.activate(settings.LANGUAGE_CODE)

        response = self.get_response(request)
        return response
