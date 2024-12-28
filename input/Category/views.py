from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Printer
from .forms import CategoryForm

def category_view(request):
    categories = Category.objects.all()  # جلب جميع الأقسام
    printers = Printer.objects.all()  # جلب جميع الطابعات

    # التعامل مع إضافة قسم جديد
    if request.method == 'POST' and 'add_category' in request.POST:
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            # تحقق إذا كان القسم بنفس الاسم موجودًا مسبقًا
            name_lo = category_form.cleaned_data['name_lo']
            if Category.objects.filter(name_lo=name_lo).exists():
                # إذا كان القسم موجودًا بالفعل، عرض رسالة تحذير
                category_form.add_error('name_lo', 'هذا القسم موجود بالفعل!')
            else:
                # إذا لم يكن القسم موجودًا، حفظ القسم الجديد
                category_form.save()
                return redirect('category_view')  # إعادة التوجيه بعد إضافة القسم
    else:
        category_form = CategoryForm()  # نموذج فارغ لإضافة قسم جديد

    # التعامل مع تعديل قسم
    if request.method == 'POST' and 'edit_category' in request.POST:
        category_id = request.POST.get('edit_category')
        category = get_object_or_404(Category, id=category_id)
        # تحديث الطابعة المحددة
        printer_id = request.POST.get('printer')
        if printer_id:
            printer = get_object_or_404(Printer, id=printer_id)
            category.printer = printer
            category.save()  # حفظ التعديلات
            return redirect('category_view')  # إعادة التوجيه بعد تعديل القسم

    # التعامل مع حذف قسم
    if request.method == 'POST' and 'delete_category' in request.POST:
        category_id = request.POST.get('delete_category')
        category = get_object_or_404(Category, id=category_id)
        category.delete()  # حذف القسم
        return redirect('category_view')  # إعادة التوجيه بعد حذف القسم

    return render(request, 'input/Category/category.html', {
        'category_form': category_form,  # تمرير النموذج لإضافة قسم جديد
        'categories': categories,  # تمرير الأقسام لعرضها في الجدول
        'printers': printers,  # تمرير الطابعات لعرضها في النموذج
    })
