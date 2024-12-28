from django.shortcuts import render, redirect
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.views import View
from django.utils.translation import gettext_lazy as _  # استيراد _() للترجمة
from purchases.models import Supplier
from .forms import SupplierForm
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import QueryDict
from django.db.models import Q




class Supplier_view(CreateView):
   
    def get(self, request, *args, **kwargs):
        if 'id' in request.GET.keys():
            supplier_id = request.GET.get('id')
            supplier = Supplier.objects.filter(pk=supplier_id)
            result = {'status': 1, 'data': serializers.serialize('json', supplier)}
            return JsonResponse(result)
        else:
            suppliers = Supplier.objects.all()
            form = SupplierForm()
            context = {
                "Items": suppliers,
                "filed": form
            }
            return render(request, 'purchases/Supplier/Supplier.html', context)

    def post(self, request, *args, **kwargs):
        # تحقق من تكرار الاسم قبل الحفظ أو التعديل
        name_lo = request.POST.get('name_lo')
        if Supplier.objects.filter(name_lo=name_lo).exists() and not request.POST.get('id'):
            return JsonResponse({'status': 0, 'error': _('اسم المورد موجود بالفعل!')})
        
        if request.POST.get('id'):
            supplier = get_object_or_404(Supplier, pk=int(request.POST.get('id')))
            form = SupplierForm(request.POST, instance=supplier)
        else:
            form = SupplierForm(request.POST)
        
    
        if form.is_valid():
            supplier = form.save()
            return JsonResponse({'status': 1, 'message': _('تمت عملية الحفظ')})
        else:
            return JsonResponse({'status': 0, 'error': form.errors.as_json()})

    def delete(self, request, *args, **kwargs):
        pk = int(request.body.decode('utf-8').split('=')[-1])
        if pk:
            try:
                supplier = get_object_or_404(Supplier, pk=pk)
                supplier.delete()
                return JsonResponse({'status': 1, 'message': _('تمت عملية الحذف')})
            except Supplier.DoesNotExist:
                return JsonResponse({'status': 0, 'message': _('المورد غير موجود')})
        return JsonResponse({'status': 0, 'message': _('لا يوجد مورد')})


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

# دالة إضافة الرصيد
def add_balance_view(request, supplier_id, amount):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.add_balance(amount)
    return HttpResponse(f"تم إضافة {amount} ريال إلى رصيد {supplier.name_lo}.")

# دالة خصم الرصيد
def subtract_balance_view(request, supplier_id, amount):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.subtract_balance(amount)
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

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'purchases/Supplier/supplier_list.html', {'suppliers': suppliers})