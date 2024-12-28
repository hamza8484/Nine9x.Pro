from django.shortcuts import render
from django.http import JsonResponse
from django.utils import translation
import logging
import requests
from django.utils.translation import activate
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _


def check_server_connection(request):
    server_url = "http://127.0.0.1:8000/"  # ضع هنا عنوان السيرفر الذي تريد التحقق من الاتصال به

    try:
        # محاولة إرسال طلب GET إلى السيرفر
        response = requests.get(server_url, timeout=5)
        
        if response.status_code == 200:
            return JsonResponse({'status': 'online'})
        else:
            return JsonResponse({'status': 'offline'})
    
    except requests.RequestException:
        # إذا حدث خطأ أو لم يستجب السيرفر، سيتم إرجاع حالة "offline"
        return JsonResponse({'status': 'offline'})




def check_connection(request):
   try:
        # إرسال طلب HTTP إلى موقع موثوق (مثلاً google)
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            return JsonResponse({'status': 'online'})
        else:
            return JsonResponse({'status': 'offline'})
   except requests.ConnectionError:
        return JsonResponse({'status': 'offline'})


def change_language(request):
    language = request.GET.get('language')

    if language and language in dict(settings.LANGUAGES):
        # تفعيل اللغة الجديدة
        translation.activate(language)
        # حفظ اللغة في الجلسة
        request.session['django_language'] = language
        messages.success(request, "تم تغيير اللغة بنجاح!")
    else:
        # العودة إلى اللغة الافتراضية إذا كانت اللغة غير معروفة
        translation.activate(settings.LANGUAGE_CODE)
        request.session['django_language'] = settings.LANGUAGE_CODE
        messages.warning(request, "اللغة غير معروفة، تم الرجوع إلى اللغة الافتراضية.")

    # إعادة توجيه المستخدم إلى الصفحة السابقة أو الصفحة الرئيسية
    return redirect(request.META.get('HTTP_REFERER', '/'))

