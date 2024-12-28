from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Invoice, InvoiceItem, InvoiceCounter, save_invoice_and_items
from purchases.models import Supplier
from input.models import Items
from TaxApp.models import Tax
from configrate.models import Store
from decimal import Decimal
from datetime import date
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import Invoice, Supplier 
from django.db.models import Sum

@login_required
def create_invoice(request):
    suppliers = Supplier.objects.all()
    items = Items.objects.all()
    taxes = Tax.objects.all()
    user = request.user
    stores_list = Store.objects.all()

    # جلب الرقم التسلسلي الأخير للفواتير باستخدام get_or_create
    invoice_counter, created = InvoiceCounter.objects.get_or_create(defaults={'last_invoice_number': 0})

    # التحقق من أن `invoice_id` موجود في الجلسة أو في `POST`
    if 'invoice_id' in request.session or 'invoice_id' in request.POST:
        invoice_id = request.session.get('invoice_id', None) or request.POST.get('invoice_id', None)
        try:
            invoice = Invoice.objects.get(id=invoice_id)
            invoice_number = invoice.invoice_number
        except Invoice.DoesNotExist:
            invoice_number = f"PUR-{str(invoice_counter.last_invoice_number + 1).zfill(4)}"
            error_message = "الفاتورة غير موجودة، سيتم إنشاء فاتورة جديدة."
            request.session.pop('invoice_id', None)  # مسح الـ session المرتبط بالـ invoice_id
            return render(request, 'purchases/purchases/create_invoice.html', {
                'suppliers': suppliers,
                'items': items,
                'stores_list': stores_list,
                'taxes': taxes,
                'invoice_number': invoice_number,
                'user': user,
                'today': date.today(),
                'error_message': error_message,
            })
    else:
        # تعيين رقم الفاتورة إذا لم يكن في الجلسة
        invoice_number = f"PUR-{str(invoice_counter.last_invoice_number + 1).zfill(4)}"

        if request.method == 'POST':
            error_message = None  # تهيئة الرسالة قبل التحقق

            # التحقق من الحقول المطلوبة
            supplier_id = request.POST.get('supplier_id')
            supplier_invoice_number = request.POST.get('supplier_invoice_number')
            supplier_invoice_date_str = request.POST.get('supplier_invoice_date')
            store_id = request.POST.get('store_id')
            payment_method = request.POST.get('payment_method')
            discount_type = request.POST.get('discount_type')  # نوع الخصم (نسبة مئوية أو مبلغ ثابت)
            discount_value = Decimal(request.POST.get('discount_value', '0.00'))  # قيمة الخصم

            if not supplier_id:
                error_message = 'المورد مطلوب!'
            elif not supplier_invoice_number:
                error_message = 'رقم فاتورة المورد مطلوب!'
            elif not supplier_invoice_date_str:
                error_message = 'تاريخ فاتورة المورد مطلوب!'
            elif not store_id:
                error_message = 'المخزن مطلوب!'
            elif not payment_method:
                error_message = 'طريقة الدفع مطلوبة!'

            # إذا كانت هناك رسالة خطأ، قم بإرسالها إلى القالب
            if error_message:
                return render(request, 'purchases/purchases/create_invoice.html', {
                    'suppliers': suppliers,
                    'items': items,
                    'stores_list': stores_list,
                    'taxes': taxes,
                    'invoice_number': invoice_number,
                    'user': user,
                    'today': date.today(),
                    'error_message': error_message,
                })

            # التحقق من المورد والمخزن
            try:
                supplier = Supplier.objects.get(id=supplier_id)
            except Supplier.DoesNotExist:
                return render(request, 'purchases/purchases/create_invoice.html', {
                    'suppliers': suppliers,
                    'items': items,
                    'stores_list': stores_list,
                    'taxes': taxes,
                    'invoice_number': invoice_number,
                    'user': user,
                    'today': date.today(),
                    'error_message': 'المورد غير موجود!',
                })

            try:
                store = Store.objects.get(id=store_id)
            except Store.DoesNotExist:
                return render(request, 'purchases/purchases/create_invoice.html', {
                    'suppliers': suppliers,
                    'items': items,
                    'stores_list': stores_list,
                    'taxes': taxes,
                    'invoice_number': invoice_number,
                    'user': user,
                    'today': date.today(),
                    'error_message': 'المخزن غير موجود!',
                })

            # التعامل مع تاريخ فاتورة المورد
            try:
                supplier_invoice_date = date.fromisoformat(supplier_invoice_date_str)
            except ValueError:
                return render(request, 'purchases/purchases/create_invoice.html', {
                    'suppliers': suppliers,
                    'items': items,
                    'stores_list': stores_list,
                    'taxes': taxes,
                    'invoice_number': invoice_number,
                    'user': user,
                    'today': date.today(),
                    'error_message': 'تنسيق تاريخ فاتورة المورد غير صحيح! يجب أن يكون YYYY-MM-DD.',
                })

            # عناصر الفاتورة من الـ POST
            items_data = []  # هنا يجب معالجة العناصر وإضافتها إلى الفاتورة
            for item_id, quantity, price in zip(request.POST.getlist('item_id'), request.POST.getlist('quantity'), request.POST.getlist('price')):
                item = Items.objects.get(id=item_id)
                total = Decimal(quantity) * Decimal(price)
                items_data.append({
                    'item': item,
                    'quantity': quantity,
                    'price': price,
                    'total': total
                })

            # الآن يمكن حساب الخصم على الإجمالي بعد إضافة العناصر
            total_purchase = sum(item['total'] for item in items_data)  # جمع إجمالي جميع العناصر
            
            # حساب الخصم بناءً على نوعه
            if discount_type == 'percentage':
                discount_amount = (discount_value / Decimal('100')) * total_purchase
            else:
                discount_amount = discount_value

            # تحديث الإجمالي بعد الخصم
            total_after_discount = total_purchase - discount_amount

            # حساب الضريبة
            tax_percentage = Tax.objects.first().rate if Tax.objects.exists() else 0
            tax_value = (tax_percentage / Decimal('100')) * total_after_discount

            # إجمالي الفاتورة بعد إضافة الضريبة
            total_invoice = total_after_discount + tax_value

            # تحديث بيانات الفاتورة
            invoice_data = {
                'invoice_number': invoice_number,
                'invoice_date': date.today(),
                'supplier_invoice_number': supplier_invoice_number,
                'supplier_invoice_date': supplier_invoice_date,
                'supplier': supplier,
                'store': store,
                'payment_method': payment_method,
                'user': user,
                'total_purchase': total_purchase,
                'discount_type': discount_type,
                'discount_value': discount_amount,
                'tax_value': tax_value,
                'total_tax': tax_value,
                'total_invoice': total_invoice
            }

            # حفظ الفاتورة والعناصر
            invoice = save_invoice_and_items(invoice_data, items_data)

            # تحقق إذا كانت الفاتورة تم إنشاؤها بنجاح
            if invoice is None:
                error_message = "حدث خطأ أثناء إنشاء الفاتورة."
                return render(request, 'purchases/purchases/create_invoice.html', {
                    'suppliers': suppliers,
                    'items': items,
                    'stores_list': stores_list,
                    'taxes': taxes,
                    'invoice_number': invoice_number,
                    'user': user,
                    'today': date.today(),
                    'error_message': error_message,
                })

            # تخزين الـ invoice_id في الجلسة
            request.session['invoice_id'] = invoice.id

            # تحديث الرقم التسلسلي للفواتير
            invoice_counter.last_invoice_number += 1
            invoice_counter.save()

            return redirect('invoice_list')  # إعادة التوجيه إلى قائمة الفواتير بعد الحفظ

        # في حالة طلب GET أو فشل POST
        return render(request, 'purchases/purchases/create_invoice.html', {
            'suppliers': suppliers,
            'items': items,
            'stores_list': stores_list,
            'taxes': taxes,
            'invoice_number': invoice_number,
            'user': user,
            'today': date.today(),
            'tax_percentage': Tax.objects.first().rate if Tax.objects.exists() else 0,
        })


@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()

    if 'supplier' in request.GET:
        invoices = invoices.filter(supplier_id=request.GET['supplier'])

    if 'date_from' in request.GET and 'date_to' in request.GET:
        invoices = invoices.filter(invoice_date__range=[request.GET['date_from'], request.GET['date_to']])

    # حساب الإجماليات
    total_purchase_sum = invoices.aggregate(Sum('total_purchase'))['total_purchase__sum'] or 0
    total_discount_sum = invoices.aggregate(Sum('discount_value'))['discount_value__sum'] or 0
    total_tax_sum = invoices.aggregate(Sum('total_tax'))['total_tax__sum'] or 0
    total_invoice_sum = invoices.aggregate(Sum('total_invoice'))['total_invoice__sum'] or 0

    return render(request, 'purchases/purchases/invoice_list.html', {
        'invoices': invoices,
        'suppliers': Supplier.objects.all(),
        'total_purchase_sum': total_purchase_sum,
        'total_discount_sum': total_discount_sum,
        'total_tax_sum': total_tax_sum,
        'total_invoice_sum': total_invoice_sum,
    })


def invoice_print(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'purchases/invoice_print.html', {'invoice': invoice})
