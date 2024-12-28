# views.py
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from .forms import PrinterSettingForm
from .models import PrinterSetting
from django.http import JsonResponse
from .models import Printer
from .forms import PrinterForm, IPAddressForm
import socket
from printsettings.models import Printer
from .models import Category 
from django.views.decorators.csrf import csrf_exempt
import json


def printer_setting_view(request):
    # محاولة الحصول على إعدادات الطابعة الحالية إذا كانت موجودة
    printer_setting = PrinterSetting.objects.first()

    if request.method == 'POST':
        form = PrinterSettingForm(request.POST, instance=printer_setting)
        
        # تحقق إذا كان اسم الطابعة المدخل موجود بالفعل
        if form.is_valid():
            # التحقق من وجود طابعة بنفس الاسم في قاعدة البيانات
            if PrinterSetting.objects.filter(printer_name=form.cleaned_data['printer_name']).exists():
                messages.error(request, "اسم الطابعة هذا موجود بالفعل.")
                return redirect('printsettings:printer_settings')  # إعادة التوجيه بعد الخطأ

            # حفظ الإعدادات أو تعديلها إذا كانت موجودة
            form.save()
            messages.success(request, "تم حفظ إعدادات الطابعة بنجاح!")  # رسالة نجاح
            return redirect('printsettings:printer_settings')  # إعادة توجيه للمسار بعد الحفظ
    else:
        form = PrinterSettingForm(instance=printer_setting)

    return render(request, 'printsettings/printer_settings.html', {
        'form': form,
        'printersetting': PrinterSetting.objects.all()
    })

# views.py

#def printer_list(request):
 #   printers = Printer.objects.all()
  #  return render(request, 'printsettings/printer_list.html', {'printers': printers})


from django.shortcuts import render, redirect
from .forms import PrinterForm
from .models import Printer

def add_printer(request):
    # جلب الطابعات فقط لأن حقل category تم إزالته
    printers = Printer.objects.all()

    if request.method == 'POST':
        form = PrinterForm(request.POST)
        if form.is_valid():
            # حفظ الطابعة الجديدة
            form.save()
            return redirect('printsettings:add_printer')  # التوجيه إلى مسار عرض الطابعات بعد الحفظ
    else:
        form = PrinterForm()

    return render(request, 'printsettings/add_printer.html', {
        'form': form,
        'printers': printers,
    })

def check_printer_connection(ip):
    try:
        # محاولة الاتصال بالطابعة عبر المنفذ 9100 (البورت الشائع للطابعات)
        sock = socket.create_connection((ip, 9100), timeout=5)  # 5 ثواني كحد أقصى للاتصال
        sock.close()
        return True
    except (socket.timeout, socket.error):
        return False

def search_printer(request):
    ip_address = request.GET.get('ip')
    if ip_address:
        # تحقق من الاتصال باستخدام الـ IP (يمكنك إضافة منطقك هنا)
        printer = Printer.objects.filter(ip_address=ip_address).first()
        if printer:
            return JsonResponse({'status': 'success', 'message': 'تم الاتصال بالطابعة!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'فشل الاتصال بالطابعة أو IP غير صالح.'})
    return JsonResponse({'status': 'error', 'message': 'لم يتم إرسال عنوان IP.'})



@csrf_exempt  # فقط إذا كنت تستخدم طلبات AJAX بدون التحقق من CSRF
def update_printer(request, pk):
    if request.method == 'POST':
        printer = get_object_or_404(Printer, pk=pk)

        # الحصول على البيانات من JSON المرسل
        data = json.loads(request.body)
        new_ip = data.get('ip_address')

        # التحقق من صحة عنوان الـ IP
        if new_ip:
            printer.ip_address = new_ip
            printer.save()
            return JsonResponse({'success': True, 'message': 'تم التعديل بنجاح'})
        else:
            return JsonResponse({'success': False, 'message': 'عنوان الـ IP غير صالح'})

    return JsonResponse({'success': False, 'message': 'طلب غير صحيح'})

def test_printer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ip_address = data.get('ip_address')

        if ip_address:
            try:
                # محاولة الاتصال بالطابعة عبر المنفذ (عادة يكون 9100 للطابعات)
                socket.create_connection((ip_address, 9100), timeout=5)
                return JsonResponse({'status': 'success', 'message': 'تم الاتصال بالطابعة بنجاح'})
            except (socket.timeout, socket.error):
                return JsonResponse({'status': 'error', 'message': 'فشل الاتصال بالطابعة'})
        else:
            return JsonResponse({'status': 'error', 'message': 'عنوان الـ IP غير صالح'})

    return JsonResponse({'status': 'error', 'message': 'طلب غير صالح'})


import socket
from django.http import JsonResponse
import threading

# وظيفة لاختبار الاتصال بالطابعة عبر بروتوكول TCP/IP
def check_printer(ip_address, port=9100, timeout=1):
    try:
        # محاولة الاتصال بالطابعة عبر الـ IP والبورت المحدد
        with socket.create_connection((ip_address, port), timeout=timeout):
            return True  # إذا تم الاتصال بالطابعة بنجاح
    except (socket.timeout, socket.error):
        return False  # إذا فشل الاتصال بالطابعة

# وظيفة لاكتشاف الطابعات عبر الشبكة المحلية
def search_printers(request):
    # قائمة لتخزين الطابعات المكتشفة
    printers = []
    
    # نطاق IP في الشبكة المحلية التي تريد البحث فيها
    network_range = ['192.168.1.' + str(i) for i in range(1, 255)]  # نطاق العناوين من 192.168.1.1 إلى 192.168.1.254
    
    # فحص الطابعات عبر الشبكة باستخدام Threading لتحسين الأداء
    def find_printer(ip):
        # اختبار الاتصال بالطابعة
        if check_printer(ip):
            printers.append({
                'id': len(printers) + 1,
                'name': f'Printer {len(printers) + 1}',  # استبدل باسم الطابعة إذا كان معروفًا
                'brand': 'Unknown',  # استبدل بعلامة الطابعة إذا كانت معروفة
                'model': 'Unknown',  # استبدل بنموذج الطابعة إذا كان معروفًا
                'ip_address': ip,
                'is_connected': True
            })

    # استخدام Threading لتحسين سرعة عملية البحث
    threads = []
    for ip in network_range:
        thread = threading.Thread(target=find_printer, args=(ip,))
        threads.append(thread)
        thread.start()
    
    # الانتظار حتى تنتهي جميع الخيوط (threads)
    for thread in threads:
        thread.join()

    return JsonResponse({'printers': printers})



@csrf_exempt  # فقط إذا كنت تستخدم طلبات AJAX بدون التحقق من CSRF
def delete_printer(request, printer_id):
    if request.method == 'POST':
        try:
            printer = Printer.objects.get(id=printer_id)
            printer.delete()
            return JsonResponse({'status': 'success', 'message': 'تم الحذف بنجاح'})
        except Printer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'الطابعة غير موجودة'})
    return JsonResponse({'status': 'error', 'message': 'طريقة غير مسموح بها'})
