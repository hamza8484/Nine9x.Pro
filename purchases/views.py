from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import PurchaseInvoice, InvoiceDetail
from .forms import PurchaseInvoiceForm, InvoiceDetailForm, SupplierForm
from purchases.models import Supplier
import logging
from decimal import Decimal
from django.http import Http404
from django.utils.translation import gettext_lazy as _

# تهيئة اللوج
logger = logging.getLogger(__name__)

# عرض قائمة فواتير المشتريات
def purchase_invoices_list(request):
    invoices = PurchaseInvoice.objects.all()
    return render(request, 'purchase_invoices_list.html', {'invoices': invoices})

# عرض صفحة إضافة فاتورة
def create_purchase_invoice(request):
    if request.method == 'POST':
        invoice_form = PurchaseInvoiceForm(request.POST)
        if invoice_form.is_valid():
            # إذا كانت البيانات صالحة، قم بتعيين قيم الحقول
            invoice = invoice_form.save(commit=False)
            invoice.user = request.user  # تعيين المستخدم الحالي

            # تأكد من تعيين المورد إذا كانت القيمة موجودة
            supplier = invoice_form.cleaned_data.get('supplier')
            if supplier:
                invoice.supplier = supplier
            invoice.save()

            # حفظ تفاصيل الفاتورة
            invoice_details = request.POST.getlist('items')
            for detail in invoice_details:
                item_id, unit_id, quantity, price, discount = detail.split(',')
                try:
                    InvoiceDetail.objects.create(
                        invoice=invoice,
                        Items_id=item_id,
                        unit_id=unit_id,
                        quantity=int(quantity),
                        price=Decimal(price),
                        discount=Decimal(discount),
                    )
                except ValueError as e:
                    logger.error(_("Error while creating invoice details: %s") % e)
                    return JsonResponse({'status': '0', 'error': _('خطأ في تفاصيل الفاتورة')})

            return redirect('purchase_invoice_success', invoice_code=invoice.invoice_code)
        else:
            return render(request, 'purchase_invoice_form.html', {'invoice_form': invoice_form})
    else:
        invoice_form = PurchaseInvoiceForm()

    return render(request, 'purchase_invoice_form.html', {'invoice_form': invoice_form})

# عرض صفحة نجاح الفاتورة
def purchase_invoice_success(request, invoice_code):
    invoice = get_object_or_404(PurchaseInvoice, invoice_code=invoice_code)
    details = InvoiceDetail.objects.filter(invoice=invoice)
    
    context = {
        'invoice': invoice,
        'details': details,
        'invoice_code': invoice_code,
    }

    return render(request, 'purchase_invoice_success.html', context)

# عرض قائمة الموردين
def supplier_list(request):
    suppliers = Supplier.objects.all()  # جلب كل الموردين من قاعدة البيانات
    return render(request, 'purchases/suppliers_list.html', {'suppliers': suppliers})

# عرض تفاصيل المورد أو إضافة/تعديل المورد
class Supplier_view(View):
    def get(self, request, id=None):
        if id:
            try:
                supplier = Supplier.objects.get(id=id)  # محاولة جلب المورد
            except Supplier.DoesNotExist:
                raise Http404(_("المورد غير موجود"))
            return render(request, 'purchases/supplier_detail.html', {'supplier': supplier})
        else:
            suppliers = Supplier.objects.all()
            return render(request, 'purchases/suppliers_list.html', {'suppliers': suppliers})

    def post(self, request, id=None):
        if id:  # تعديل المورد
            try:
                supplier = Supplier.objects.get(id=id)
                form = SupplierForm(request.POST, instance=supplier)  # تحميل النموذج مع بيانات المورد
            except Supplier.DoesNotExist:
                raise Http404(_("المورد غير موجود"))
        else:  # إضافة مورد جديد
            form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()  # حفظ المورد الجديد أو المعدل
            return redirect('suppliers_list')  # إعادة التوجيه إلى صفحة قائمة الموردين بعد الحفظ
        return render(request, 'purchases/supplier_add.html', {'form': form})

# جلب بيانات الموردين بتنسيق JSON
class SupplierJson(View):
    def get(self, request):
        suppliers = Supplier.objects.all()
        suppliers_data = list(suppliers.values())  # تحويل البيانات إلى قائمة
        return JsonResponse(suppliers_data, safe=False)

# دالة لعرض صفحة إضافة المورد
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            # تحقق من وجود المورد بنفس الاسم في قاعدة البيانات
            supplier_name = form.cleaned_data.get('name_lo')  # استبدل بـ الحقل الصحيح
            if Supplier.objects.filter(name_lo=supplier_name).exists():
                logger.warning(_("Supplier with name %s already exists.") % supplier_name)  # تسجيل تحذير
                return JsonResponse({'status': '0', 'error': _('المورد موجود بالفعل')})
            
            try:
                form.save()  # حفظ المورد الجديد في قاعدة البيانات
                return JsonResponse({'status': '1', 'message': _('تم إضافة المورد بنجاح')})
            except Exception as e:
                logger.error(_("Error while saving supplier: %s") % e)  # تسجيل الخطأ في اللوج
                return JsonResponse({'status': '0', 'error': _('حدث خطأ في إضافة المورد')})
        else:
            logger.error(_("Form validation failed: %s") % form.errors)  # تسجيل الأخطاء في النموذج
            return JsonResponse({'status': '0', 'error': _('البيانات غير صحيحة')})
    else:
        form = SupplierForm()

    return render(request, 'purchases/supplier_add.html', {'form': form})
