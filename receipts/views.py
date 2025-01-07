from django.shortcuts import render
from .models import Receipt
from .forms import ReceiptForm
from .models import Payment
from .forms import PaymentForm
from purchases.models import Supplier
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

def receipt_list(request):
    receipts = Receipt.objects.all()

    # تصفية بناءً على العميل أو التاريخ
    customer_filter = request.GET.get('customer')
    if customer_filter:
        receipts = receipts.filter(customer__name_lo__icontains=customer_filter)

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from and date_to:
        receipts = receipts.filter(receipt_date__range=[date_from, date_to])

    return render(request, 'receipts/receipt_list.html', {'receipts': receipts})


def payment_list(request):
    payments = Payment.objects.all()

    # تصفية بناءً على المورد أو التاريخ
    supplier_filter = request.GET.get('supplier')
    if supplier_filter:
        payments = payments.filter(supplier__name_lo__icontains=supplier_filter)

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from and date_to:
        payments = payments.filter(payment_date__range=[date_from, date_to])

    return render(request, 'receipts/payment_list.html', {'payments': payments})

# إضافة سند قبض
def receipt_form(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receipt_list')
    else:
        form = ReceiptForm()
    return render(request, 'receipts/receipt_form.html', {'form': form})

# إضافة سند صرف
def payment_form(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'receipts/payment_form.html', {'form': form})


# عرض رصيد المورد بناءً على ID المورد
def get_supplier_balance(request, supplier_id):
    try:
        # جلب المورد بناءً على ID المورد
        supplier = Supplier.objects.get(id=supplier_id)
        
        # إرجاع رصيد المورد
        return JsonResponse({'supplier_balance': str(supplier.balance)}, status=200)
    except Supplier.DoesNotExist:
        return JsonResponse({'error': 'Supplier not found'}, status=404)
    

# عرض الرصيد المتبقي بعد الدفع
@require_http_methods(["GET"])
def get_balance_after_payment(request, payment_number):
    try:
        # جلب المدفوعات بناءً على رقم الدفع
        payment = Payment.objects.get(payment_number=payment_number)
        
        # استرجاع الرصيد المتبقي بعد الدفع
        balance_after_payment = payment.balance_after_payment
        
        # إرسال الاستجابة مع الرصيد المتبقي
        return JsonResponse({'balance_after_payment': str(balance_after_payment)}, status=200)
    except Payment.DoesNotExist:
        # في حالة عدم وجود السداد
        return JsonResponse({'error': 'Payment not found'}, status=404)

# عرض رصيد المورد الحالي بناءً على ID المورد
@require_http_methods(["GET"])
def get_supplier_balance(request, supplier_id):
    try:
        # جلب المورد بناءً على ID المورد
        supplier = Supplier.objects.get(id=supplier_id)
        
        # إرجاع رصيد المورد
        return JsonResponse({'supplier_balance': str(supplier.balance)}, status=200)
    except Supplier.DoesNotExist:
        return JsonResponse({'error': 'Supplier not found'}, status=404)