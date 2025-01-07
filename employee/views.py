from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .models import Employee
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import SalaryPayment
from .forms import SalaryPaymentForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.translation import gettext as _


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            # حفظ الموظف
            employee = form.save()
            # بعد حفظ الموظف، إعادة تعيين النموذج ليكون فارغًا
            form = EmployeeForm()  # إعادة تهيئة النموذج فارغًا
            return render(request, 'employee/add_employee.html', {
                'form': form,
                'employee_number': employee.employee_number  # تمرير رقم الموظف إذا أردت
            })
    else:
        form = EmployeeForm()

    return render(request, 'employee/add_employee.html', {'form': form})


def employee_list(request):
    query = request.GET.get('search', '')
    employees = Employee.objects.filter(
        Q(name__icontains=query) | 
        Q(employee_number__icontains=query) |
        Q(mobile_number__icontains=query) |
        Q(id_card_number__icontains=query)
    )
    return render(request, 'employee/employee_list.html', {'employees': employees})


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employee/employee_detail.html', {'employee': employee})


def edit_employee(request, id):
    # جلب الموظف باستخدام ID
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # أو أي صفحة أخرى بعد التحديث
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employee/edit_employee.html', {'form': form, 'employee': employee})

def create_salary_payment(request):
    if request.method == 'POST':
        form = SalaryPaymentForm(request.POST)
        if form.is_valid():
            # الحصول على البيانات من النموذج
            payment = form.save(commit=False)

            # تحقق من أنه لم يتم دفع الراتب لهذا الموظف في نفس الشهر
            existing_payment = SalaryPayment.objects.filter(
                employee=payment.employee,
                payment_date__year=payment.payment_date.year,
                payment_date__month=payment.payment_date.month
            ).exists()

            if existing_payment:
                # إذا كان هناك راتب مدفوع في نفس الشهر، نعرض رسالة خطأ
                messages.error(request, _("تم دفع راتب الموظف {payment.employee.name} في شهر {payment.payment_date.strftime('%B %Y')}."))

            else:
                # إذا كان الدفع صحيحًا، نحفظ البيانات
                payment.save()
                messages.success(request, _("تم تسليم الراتب للموظف {payment.employee.name} لشهر {payment.payment_date.strftime('%B %Y')}."))

                return redirect('salary_payment_list')  # إعادة التوجيه إلى قائمة المدفوعات
    else:
        form = SalaryPaymentForm()

    return render(request, 'employee/create_salary_payment.html', {'form': form})

def salary_payment_list(request):
    payments = SalaryPayment.objects.all()
    return render(request, 'employee/salary_payment_list.html', {'payments': payments})



def get_salary_and_allowances(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        data = {
            'salary': employee.base_salary,  # تأكد أن هذا الحقل موجود في نموذج الموظف
            'allowances': employee.allowances,  # تأكد من وجود هذا الحقل أيضًا
        }
        return JsonResponse(data)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)


def salary_list(request):
    # جلب المدفوعات بدلاً من الموظفين
    payments = SalaryPayment.objects.all()  # هنا يجب أن تستخدم استعلام المدفوعات
    paginator = Paginator(payments, 10)  # تقسيم المدفوعات إلى صفحات، 10 مدفوعات لكل صفحة
    page_number = request.GET.get('page')  # الحصول على رقم الصفحة من معلمات الاستعلام
    page_obj = paginator.get_page(page_number)  # الحصول على صفحة المدفوعات الحالية

    return render(request, 'employee/salary_payment_list.html', {'page_obj': page_obj})

def print_salary_details(request, payment_id):
    # جلب تفاصيل الدفع بناءً على payment_id
    payment = get_object_or_404(SalaryPayment, id=payment_id)

    return render(request, 'employee/print_salary_details.html', {'payment': payment})