from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import PaymentVoucherForm, ReceiptVoucherForm
from .models import PaymentVoucher, ReceiptVoucher
from purchases.models import Supplier
from sales.models import Customer

# إضافة سند الدفع
def add_payment_voucher(request):
    if request.method == 'POST':
        form = PaymentVoucherForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # محاولة حفظ السند
                messages.success(request, 'تم إضافة سند الدفع بنجاح.')
                return redirect('payment_voucher_list')
            except ValidationError as e:
                messages.error(request, f"خطأ في البيانات: {e.message}")  # عرض رسالة الخطأ إذا حدث استثناء
        else:
            messages.error(request, 'توجد أخطاء في النموذج.')
    else:
        form = PaymentVoucherForm()
    return render(request, 'payments/add_payment_voucher.html', {'form': form})

# إضافة سند القبض
def add_receipt_voucher(request):
    if request.method == 'POST':
        form = ReceiptVoucherForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'تم إضافة سند القبض بنجاح.')
                return redirect('receipt_voucher_list')
            except ValidationError as e:
                messages.error(request, f"خطأ في البيانات: {e.message}")
        else:
            messages.error(request, 'توجد أخطاء في النموذج.')
    else:
        form = ReceiptVoucherForm()
    return render(request, 'payments/add_receipt_voucher.html', {'form': form})

# عرض تفاصيل سند الدفع
def payment_voucher_detail(request, voucher_number):
    payment_voucher = get_object_or_404(PaymentVoucher, voucher_number=voucher_number)
    return render(request, 'payments/payment_voucher_detail.html', {'payment_voucher': payment_voucher})

# عرض تفاصيل سند القبض
def receipt_voucher_detail(request, voucher_number):
    try:
        receipt_voucher = get_object_or_404(ReceiptVoucher, voucher_number=voucher_number)
    except ReceiptVoucher.DoesNotExist:
        messages.error(request, "سند القبض غير موجود.")
        return redirect('receipt_voucher_list')
    return render(request, 'payments/receipt_voucher_detail.html', {'receipt_voucher': receipt_voucher})

# عرض سندات الدفع مع البحث
def payment_voucher_list(request):
    search_supplier = request.GET.get('search_supplier', '').strip()  # احصل على البحث وتخلص من المسافات
    if search_supplier:
        # تصفية البيانات بناءً على اسم المورد
        payment_vouchers = PaymentVoucher.objects.filter(supplier__name_lo__icontains=search_supplier)
    else:
        payment_vouchers = PaymentVoucher.objects.all()

    return render(request, 'payments/voucher_list.html', {'payment_vouchers': payment_vouchers, 'search_supplier': search_supplier})

# عرض سندات القبض مع البحث
def receipt_voucher_list(request):
    search_customer = request.GET.get('search_customer', '').strip()  # احصل على البحث وتخلص من المسافات
    if search_customer:
        # تصفية البيانات بناءً على اسم العميل
        receipt_vouchers = ReceiptVoucher.objects.filter(customer__name_lo__icontains=search_customer)
    else:
        receipt_vouchers = ReceiptVoucher.objects.all()

    return render(request, 'payments/voucher_list.html', {'receipt_vouchers': receipt_vouchers, 'search_customer': search_customer})

# عرض تفاصيل السند
def voucher_detail(request, id):
    voucher = get_object_or_404(ReceiptVoucher, id=id)
    return render(request, 'payments/voucher_detail.html', {'voucher': voucher})

# عرض تفاصيل سند المورد
def supplier_voucher_detail(request, voucher_number):
    voucher = get_object_or_404(PaymentVoucher, voucher_number=voucher_number)
    return render(request, 'payments/supplier_voucher_detail.html', {'voucher': voucher})

# عرض قائمة جميع السندات (سندات الدفع وسندات القبض)
def voucher_list(request):
    payment_vouchers = PaymentVoucher.objects.all()
    receipt_vouchers = ReceiptVoucher.objects.all()
    
    return render(request, 'payments/voucher_list.html', {
        'payment_vouchers': payment_vouchers,
        'receipt_vouchers': receipt_vouchers
    })
