from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.core import serializers
from .models import Supplier
from .forms import SupplierForm

# عرض قائمة الموردين
def supplier_list(request):
    suppliers = Supplier.objects.all()  # جلب كل الموردين من قاعدة البيانات
    return render(request, 'purchases/Supplier/suppliers_list.html', {'suppliers': suppliers})

# عرض وتعديل بيانات الموردين أو إضافة مورد جديد
class SupplierView(View):
    def get(self, request, id=None):
        if id:
            # إذا كان هناك id في الطلب، عرض تفاصيل المورد
            supplier = get_object_or_404(Supplier, id=id)
            return render(request, 'purchases/Supplier/supplier_detail.html', {'supplier': supplier})
        else:
            # إذا لم يكن هناك id، عرض قائمة الموردين
            suppliers = Supplier.objects.all()
            return render(request, 'purchases/Supplier/suppliers_list.html', {'suppliers': suppliers})

    def post(self, request, id=None):
        # إذا كان id موجودًا، قم بتعديل المورد، وإذا لم يكن موجودًا، قم بإضافة مورد جديد
        if id:
            supplier = get_object_or_404(Supplier, id=id)
            form = SupplierForm(request.POST, instance=supplier)
        else:
            form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('supplier_list')  # بعد الحفظ، ارجع إلى قائمة الموردين
        return render(request, 'purchases/Supplier/supplier_form.html', {'form': form})

    def delete(self, request, id=None):
        if id:
            try:
                supplier = get_object_or_404(Supplier, id=id)
                supplier.delete()
                return JsonResponse({'status': 1, 'message': 'تمت عملية الحذف'})
            except Supplier.DoesNotExist:
                return JsonResponse({'status': 0, 'message': 'المورد غير موجود'})
        return JsonResponse({'status': 0, 'message': 'لا يوجد مورد'})

# جلب بيانات الموردين بتنسيق JSON
class SupplierJson(View):
    def get(self, request):
        suppliers = Supplier.objects.all()
        suppliers_data = list(suppliers.values())  # تحويل البيانات إلى قائمة
        return JsonResponse(suppliers_data, safe=False)

# دالة إضافة الرصيد
def add_balance_view(request, supplier_id, amount):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.add_balance(amount)  # تأكد أن هذه الدالة موجودة في النموذج
    return HttpResponse(f"تم إضافة {amount} ريال إلى رصيد {supplier.name_lo}.")

# دالة خصم الرصيد
def subtract_balance_view(request, supplier_id, amount):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.subtract_balance(amount)  # تأكد أن هذه الدالة موجودة في النموذج
    return HttpResponse(f"تم خصم {amount} ريال من رصيد {supplier.name_lo}.")

# الدالة الخاصة بنموذج إضافة رصيد
def add_balance_form_view(request):
    if request.method == 'POST':
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            supplier = form.add_balance()
            return redirect('supplier_detail', supplier_id=supplier.id)
    else:
        form = AddBalanceForm()
    return render(request, 'add_balance.html', {'form': form})

# دالة عرض الموردين باستخدام الجداول
class SupplierJson(BaseDatatableView):
    model = Supplier

    # الأعمدة التي سيتم إرجاعها في الجدول
    columns = [
        'id',
        'name_lo',
        'name_fk',
        'VatNumber',
        'TelPhone',
        'phone',
        'Address',
        'balance',
        'is_stop',
        'action',  # عمود الأزرار
    ]

    # الأعمدة التي سيتم السماح بالترتيب عليها
    order_columns = [
        'id',
        'name_lo',
        'name_fk',
        'VatNumber',
        'TelPhone',
        'phone',
        'Address',
        'balance',
        'is_stop',
        'action',
    ]
    
    # تصفية البيانات استنادًا إلى البحث
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name_lo__istartswith=search)
        return qs
    
    # تخصيص دالة render_column لعرض الأزرار بشكل صحيح
    def render_column(self, row, column):
        if column == 'action':
            # إضافة أزرار التعديل والحذف في عمود الأفعال
            return f'''
                <button class="btn btn-warning edit_row" data-id="{row.id}" data-url="/supplier/edit/{row.id}/">تعديل</button>
                <button class="btn btn-danger delete_row" data-id="{row.id}" data-url="/supplier/delete/{row.id}/">حذف</button>
            '''
        # يمكن إضافة حالات أخرى لأعمدة أخرى إذا لزم الأمر
        return super().render_column(row, column)
    