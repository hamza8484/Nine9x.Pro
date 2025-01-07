from django.shortcuts import render, redirect
from .models import Safe, Transaction
from .forms import TransactionForm

# شاشة عرض الخزائن
def safe_list(request):
    safes = Safe.objects.all()
    return render(request, 'cashbox/safe_list.html', {'safes': safes})

# شاشة إضافة خزنة جديدة
def add_safe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        creation_date = request.POST.get('creation_date')
        balance_added = request.POST.get('balance_added')
        notes = request.POST.get('notes', '')
        
        safe = Safe.objects.create(
            name=name,
            creation_date=creation_date,
            balance_added=balance_added,
            notes=notes
        )
        
        return redirect('safe_list')  # إعادة التوجيه إلى قائمة الخزائن بعد الحفظ
    return render(request, 'cashbox/add_safe.html')


# شاشة عرض الحركات المالية
def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'cashbox/transaction_list.html', {'transactions': transactions})

# شاشة إضافة حركة مالية (إيداع أو سحب)
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')  # إعادة التوجيه إلى قائمة الحركات بعد الحفظ
    else:
        form = TransactionForm()
    return render(request, 'cashbox/add_transaction.html', {'form': form})
