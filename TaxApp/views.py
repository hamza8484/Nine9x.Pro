from django.shortcuts import render, redirect
from .models import Tax
from .forms import TaxForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _  # استيراد _() للترجمة

def add_tax(request):
    # تحقق إذا كانت الضريبة موجودة بالفعل
    existing_tax = Tax.objects.first()  # استرجاع الضريبة الأولى (إذا كانت موجودة)

    if existing_tax:
        # إذا كانت الضريبة موجودة، يمكن للمستخدم تعديلها بدلاً من إضافتها
        if request.method == 'POST':
            form = TaxForm(request.POST, instance=existing_tax)
            if form.is_valid():
                form.save()
                messages.success(request, _('تم تعديل الضريبة بنجاح!'))  # استخدام _() لترجمة الرسالة
                return redirect('taxapp:list_taxes')  # تأكد من أن الاسم هو 'taxapp:list_taxes'
        else:
            form = TaxForm(instance=existing_tax)
        return render(request, 'tax_app/add_tax.html', {'form': form, 'is_edit': True})

    else:
        # إذا كانت الضريبة غير موجودة، قم بإضافتها
        if request.method == 'POST':
            form = TaxForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _('تم إضافة الضريبة بنجاح!'))  # استخدام _() لترجمة الرسالة
                return redirect('taxapp:list_taxes')  # تأكد من أن الاسم هو 'taxapp:list_taxes'
        else:
            form = TaxForm()
        return render(request, 'tax_app/add_tax.html', {'form': form, 'is_edit': False})

def list_taxes(request):
    # الحصول على جميع الضرائب من قاعدة البيانات
    taxes = Tax.objects.all()  # إذا كنت تستخدم نموذج Tax، تأكد من أنه يحتوي على البيانات
    return render(request, 'tax_app/list_taxes.html', {'taxes': taxes})

def tax_rate_view(request):
    # حاول الحصول على أول قيمة للضريبة من قاعدة البيانات
    tax = Tax.objects.first()  # استرجاع الضريبة الأولى (إذا كانت موجودة)
    
    if tax:
        # إذا كانت الضريبة موجودة، إرجاع قيمة النسبة المئوية
        return JsonResponse({'tax_rate': str(tax.rate)})  # إرسال النسبة كـ JSON
    else:
        # إذا لم توجد أي ضريبة في قاعدة البيانات، إعادة قيمة افتراضية (مثل 0.00)
        return JsonResponse({'tax_rate': '0.00'})


