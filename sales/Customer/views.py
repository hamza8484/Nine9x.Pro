from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomerForm
from .models import Customer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator



def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            # التحقق من وجود العميل بناءً على رقم الضريبة (أو رقم الهاتف أو أي حقل آخر)
            vat_number = form.cleaned_data['VatNumber']
            phone = form.cleaned_data['phone']

            # التحقق من وجود العميل بناءً على رقم الضريبة أو رقم الهاتف
            if Customer.objects.filter(VatNumber=vat_number).exists():
                messages.error(request, "العميل الذي يحمل هذا الرقم الضريبي موجود بالفعل.")
            elif Customer.objects.filter(phone=phone).exists():
                messages.error(request, "العميل الذي يحمل هذا الهاتف المحمول موجود بالفعل.")
            else:
                # إذا لم يكن العميل موجودًا، قم بحفظ البيانات
                form.save()
                messages.success(request, "تم إضافة العميل بنجاح.")
                return redirect('customer_list')  # إعادة التوجيه إلى قائمة العملاء بعد الإضافة
    else:
        form = CustomerForm()

    return render(request, 'sales/customer/add_customer.html', {'form': form})

def customer_list(request):
    customers = Customer.objects.all()  # الحصول على جميع العملاء
    paginator = Paginator(customers, 10)  # تقسيم العملاء إلى صفحات بحد أقصى 10 عملاء في الصفحة
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sales/customer/customer_list.html', {'page_obj': page_obj})

def edit_customer(request, id):
    # جلب العميل باستخدام المعرف
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        # تحديث بيانات العميل بناءً على المدخلات الجديدة
        customer.name_lo = request.POST['name_lo']
        customer.VatNumber = request.POST['VatNumber']
        customer.Telphone = request.POST['Telphone']
        customer.phone = request.POST['phone']
        customer.Address = request.POST['Address']
        customer.balance = request.POST['balance']
        customer.is_stop = 'is_stop' in request.POST  # تحديد ما إذا كان العميل موقوفًا
        customer.save()  # حفظ التعديلات
        return redirect('customer_list')  # إعادة التوجيه إلى قائمة العملاء بعد التعديل

    # في حالة استخدام GET لعرض النموذج
    return render(request, 'sales/customer/edit_customer.html', {'customer': customer})

def delete_customer(request, id):
    # جلب العميل باستخدام المعرف
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        # إذا تم إرسال طلب POST، نحذف العميل
        customer.delete()
        return redirect('customer_list')  # إعادة التوجيه إلى قائمة العملاء بعد الحذف

    # في حالة طلب GET، نعرض صفحة التأكيد
    return render(request, 'sales/customer/confirm_delete.html', {'customer': customer})
