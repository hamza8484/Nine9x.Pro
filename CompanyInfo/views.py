from django.shortcuts import render, redirect, get_object_or_404
from .models import CompanyInfo  
from .forms import CompanyInfoForm  # استيراد النموذج الصحيح
from django.contrib import messages
from django.utils.translation import gettext as _



def add_or_edit_company_info(request):
    # التحقق من وجود بيانات المؤسسة في قاعدة البيانات أو إنشاء مؤسسة جديدة
    company_info = CompanyInfo  .objects.first()  # تعديل الجلب حسب الحاجة (يمكنك تعديل id أو إضافة معايير إضافية)

    if request.method == 'POST':
        # إذا كانت البيانات موجودة، نقوم بتعديلها
        if company_info:
            form = CompanyInfoForm(request.POST, request.FILES, instance=company_info)
        else:
            # إذا كانت البيانات غير موجودة، نسمح بإضافة البيانات لأول مرة
            form = CompanyInfoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, _('تم حفظ المعلومات بنجاح!'))
            return redirect('CompanyInfo:company_info_success')  # التوجيه إلى صفحة النجاح
        else:
            messages.error(request,_('حدث خطأ أثناء حفظ البيانات. الرجاء التحقق من المدخلات.'))
    else:
        # تحميل النموذج مع البيانات إذا كانت موجودة
        form = CompanyInfoForm(instance=company_info)

    return render(request, 'add_company_info.html', {'form': form})

def company_info_success(request):
    return render(request, 'company_info_success.html')



