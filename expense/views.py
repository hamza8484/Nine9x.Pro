from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  # استيراد messages لإظهار الرسائل
from .forms import ExpenseForm
from .models import Expense
from django.utils.translation import gettext as _

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()  # حفظ المصروف
            messages.success(request, _('تم إضافة المصروف بنجاح'))  # الترجمة هنا
            return redirect('expense_list')  # إعادة التوجيه إلى صفحة عرض المصاريف
        else:
            messages.error(request, _('حدث خطأ أثناء إضافة المصروف'))  # الترجمة هنا
    else:
        form = ExpenseForm()  # إذا كانت الصفحة محملة لأول مرة
    return render(request, 'expense/add_expense.html', {'form': form})

def expense_list(request):
    expenses = Expense.objects.all()  # جلب جميع المصاريف من قاعدة البيانات
    return render(request, 'expense/expense_list.html', {'expenses': expenses})

def expense_edit(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)  # العثور على المصروف بناءً على الـ id

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()  # حفظ التعديلات
            return redirect('expense_list')  # إعادة التوجيه إلى قائمة المصاريف بعد التعديل
    else:
        form = ExpenseForm(instance=expense)  # إذا كانت طريقة الطلب هي GET، نعرض النموذج مع البيانات الحالية للمصروف

    return render(request, 'expense/expense_edit.html', {'form': form})
