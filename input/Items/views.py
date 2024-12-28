from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views #new
from .forms import ItemsForm
from CompanyInfo.models import CompanyInfo 
from django.utils.translation import gettext_lazy as _, gettext
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import QueryDict
from django_datatables_view.base_datatable_view import BaseDatatableView
from input.models import Category
from django.db.models import Sum
from django.contrib import messages
from input.models import Items, Category, InventoryItem, StoryItem





# دالة للحصول على جميع الأصناف
def get_items(request):
    try:
        items = Items.objects.all().values('id', 'barcode', 'name_lo', 'unit', 'purchase_price', 'salse_price')
        return JsonResponse({'items': list(items)}, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'فشل في تحميل الأصناف: {str(e)}'}, status=500)

# دالة للحصول على الأصناف بناءً على مصطلح البحث
def get_items_list(request):
    try:
        search_term = request.GET.get('search', '')  # الحصول على معلمة البحث من الـ URL
        search_type = request.GET.get('type', 'name')  # الحصول على نوع البحث (الاسم أو الباركود)

        if search_type == 'barcode' and search_term:
            # تصفية الأصناف التي تحتوي على النص المدخل في حقل barcode
            items = Items.objects.filter(barcode__icontains=search_term)
        elif search_term:
            # تصفية الأصناف التي تحتوي على النص المدخل في حقل name_lo (اسم الصنف)
            items = Items.objects.filter(name_lo__icontains=search_term)
        else:
            # إذا لم يكن هناك نص بحث، إرجاع جميع الأصناف
            items = Items.objects.all()

        # إعداد البيانات للرد
        items_data = []
        for item in items:
            items_data.append({
                'id': item.id,
                'barcode': item.barcode,  # حقل الباركود
                'name_lo': item.name_lo,  # اسم الصنف
                'unit': item.unit.name_lo if item.unit else '',  # اسم الوحدة (إذا كانت موجودة)
                'purchase_price': item.purch_price,  # سعر الشراء
                'salse_price': item.salse_price,  # سعر البيع
            })

        # إرجاع البيانات على شكل JSON
        return JsonResponse({'items': items_data})

    except Exception as e:
        # في حالة حدوث أي خطأ، إرجاع رسالة خطأ
        return JsonResponse({'error': f'فشل في تحميل الأصناف: {str(e)}'}, status=500)

# دالة للحصول على الصنف بناءً على الباركود
def get_item_by_barcode(request):
    try:
        barcode = request.GET.get('barcode', '').strip()
        if not barcode:
            return JsonResponse({'error': 'الباركود مطلوب.'}, status=400)  # حالة خطأ إذا لم يتم توفير الباركود

        item = Items.objects.filter(barcode=barcode).first()
        if item:
            item_data = {
                'barcode': item.barcode,
                'name_lo': item.name_lo,
                'unit': item.unit.name_lo if item.unit else '',
                'purchase_price': item.purch_price,
                'salse_price': item.salse_price,
            }
            return JsonResponse({'item': item_data})
        else:
            return JsonResponse({'item': None}, status=404)

    except Exception as e:
        return JsonResponse({'error': f'خطأ: {str(e)}'}, status=500)


# دالة للحصول على تفاصيل الصنف بناءً على معرّف الصنف
def get_item_details(request):
    item_id = request.GET.get('item_id')
    if not item_id:
        return JsonResponse({'error': 'مفقود معرّف الصنف'}, status=400)  # حالة خطأ إذا كان الـ ID مفقودًا

    try:
        # جلب الصنف بناءً على معرّف الصنف
        item = Items.objects.get(id=item_id)
        data = {
            'name_lo': item.name_lo,  # الاسم باللغة العربية
            'unit': item.unit.name_lo if item.unit else '',  # اسم الوحدة
            'purchase_price': item.purch_price,  # سعر الشراء
            'salse_price': item.salse_price,  # سعر البيع
            'barcode': item.barcode,  # الباركود
            'image': item.image.url if item.image else '',  # الرابط للصورة
        }
        return JsonResponse({'item': data})  # إرجاع البيانات كـ JSON
    except Items.DoesNotExist:
        return JsonResponse({'error': 'الصنف غير موجود'}, status=404)  # حالة خطأ إذا لم يتم العثور على الصنف
    except Exception as e:
        return JsonResponse({'error': f'حدث خطأ: {str(e)}'}, status=500)



def inventory_list(request):
    query = request.GET.get('q', '')  # استعلام البحث
    category_id = request.GET.get('category', None)  # تصفية حسب الفئة

    # تصفية الأصناف حسب الاسم أو الفئة
    items = Items.objects.all()

    if query:
        items = items.filter(name_lo__icontains=query)  # تصفية البحث حسب الاسم
    if category_id:
        items = items.filter(category_id=category_id)  # تصفية حسب الفئة

    # حساب الكميات المتاحة من StoryItem
    inventory_data = []
    for item in items:
        total_qty = StoryItem.objects.filter(Items=item).aggregate(total_qty=Sum('qty'))['total_qty'] or 0
        inventory_data.append({
            'item': item,
            'total_qty': total_qty,
            'unit': item.unit.name_lo if item.unit else _('N/A'),  # ترجمة الحقل "N/A"
            'purch_price': item.purch_price,
        })

    # استرجاع جميع الفئات لتمريرها إلى القالب
    categories = Category.objects.all()

    # حساب عدد الأصناف المسترجعة
    total_items_count = items.count()

    # تمرير البيانات إلى القالب
    return render(request, 'input/inventory/inventory_list.html', {
        'inventory_data': inventory_data,
        'categories': categories,
        'total_items_count': total_items_count,  # تمرير عدد الأصناف إلى القالب
    })

# دالة تحديث الكمية
def update_quantity(request, item_id):
    # التحقق من وجود الطلب ووجود الكمية
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 0))
            if quantity < 0:
                messages.error(request, _("الكمية يجب أن تكون قيمة موجبة أو صفر."))  # ترجمة الرسالة
                return redirect('inventory')  # إعادة التوجيه في حالة الخطأ

            # العثور على الصنف المطلوب
            item = Items.objects.get(id=item_id)
            
            # تحديث الكمية في نموذج StoryItem أو أي شيء آخر تحتاج إلى تحديثه
            item_qty = StoryItem.objects.filter(Items=item).first()  # تصحيح الحقل هنا

            if item_qty:
                item_qty.qty = quantity  # تحديث الكمية
                item_qty.save()
                messages.success(request, _("تم تحديث الكمية بنجاح."))  # ترجمة الرسالة
            else:
                messages.error(request, _("لم يتم العثور على الكمية الحالية لهذا الصنف."))  # ترجمة الرسالة
        except Exception as e:
            messages.error(request, _(f"حدث خطأ: {e}"))  # ترجمة الرسالة
        
        # إعادة التوجيه إلى صفحة الأصناف بعد التحديث
        return redirect('inventory')

def inventory_report(request):
    # جلب معلومات الشركة
    company_info = CompanyInfo.objects.first()  # أو حسب حاجتك لجلب بيانات الشركة

    # جلب بيانات الجرد
    inventory_data = InventoryItem.objects.all()

    # تمرير البيانات إلى القالب
    return render(request, 'inventory_report.html', {
        'company_info': company_info,
        'inventory_data': inventory_data,
        'total_items_count': inventory_data.count(),
    })

def inventory_view(request):
    # جلب البيانات اللازمة للجرد
    inventory_data = InventoryItem.objects.all()
    total_items_count = inventory_data.count()

    # جلب معلومات المؤسسة
    company_info = CompanyInfo.objects.first()  # افتراضياً أخذ أول سجل

    return render(request, 'inventory_report.html', {
        'inventory_data': inventory_data,
        'total_items_count': total_items_count,
        'company_info': company_info,
    })


 
class Items_item(CreateView):

    def get(self, request, *args, **kwargs):
        # إحضار بيانات الصنف عند طلبها بواسطة id
        if 'id' in request.GET.keys():
            if request.GET.get('id'):
                data = Items.objects.filter(pk=request.GET.get('id'))
                result = {'status': 1, 'data': serializers.serialize('json', data)}
            else:
                result = {'status': 0, 'data': ''}
            return JsonResponse(result)
        else:
            # عرض الصفحة الخاصة بإضافة أو تعديل الصنف
            Uni = Items.objects.all()
            fileduse = ItemsForm()
            context = {
                "Items": Uni,
                "filed": fileduse
            }
            return render(request, 'input/Items/Items.html', context)

    def post(self, request, *args, **kwargs):
        # إنشاء الكائن form باستخدام request.POST و request.FILES
        form = ItemsForm(request.POST, request.FILES)

        if request.POST.get('id'):  # تعديل صنف موجود
            data = get_object_or_404(Items, pk=int(request.POST.get('id')))
            form = ItemsForm(request.POST, request.FILES, instance=data)

        if form.is_valid():
            # إذا كان النموذج صحيحًا، نقوم بحفظ البيانات
            item = form.save(commit=False)

            # التأكد من أنه إذا كانت الصورة موجودة في الـ request فسيتم إضافتها
            if 'image' in request.FILES:
                item.image = request.FILES['image']
            
            item.save()  # حفظ البيانات في قاعدة البيانات

            # إرسال الرد المناسب استنادًا إلى ما إذا كنا نضيف أو نعدل
            if request.POST.get('id'):
                result = {'status': 1, 'message': _("تم التعديل بنجاح")}  # ترجمة الرسالة
            else:
                result = {'status': 1, 'message': _("تم الحفظ بنجاح")}  # ترجمة الرسالة
        else:
            # في حالة وجود أخطاء في النموذج، نعرض الأخطاء
            result = {'status': 0, 'error': form.errors.as_json()}

        return JsonResponse(result)

    def delete(self, request, *args, **kwargs):
        # حذف صنف
        pk = int(QueryDict(request.body).get('id'))
        if pk:
            try:
                data = get_object_or_404(Items, pk=pk)
                data.delete()
                msg = _("تم الحذف")  # ترجمة الرسالة
                result = {'status': 1, 'message': msg}
            except Exception as e:
                msg = _("خطأ في الحذف: ") + str(e)  # ترجمة الرسالة
                result = {'status': 0, 'message': msg}
        else:
            msg = _("لا يوجد الصنف")  # ترجمة الرسالة
            result = {'status': 0, 'message': msg}
        return JsonResponse(result)

class ItemsJson(BaseDatatableView):
    # The model we're going to show
    model = Items

    # define the columns that will be returned
    columns = [
        'id',
        "name_lo",
        "name_fk",
        "items_type",
        "unit",
        "category",
        "salse_price",
        "purch_price",
        "barcode",
        "action",
    ]

    # define column names that will be used in sorting
    order_columns = [
        'id',
        "name_lo",
        "name_fk",
        "items_type",
        "unit",
        "category",
        "salse_price",
        "purch_price",
        "barcode",
        "action",
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    max_display_length = 500

    def render_column(self, row, column):
        if column == "id":
            return row.pk
        if column == "action":
            return '<a class="edit_row" data-url="{3}" data-id="{0}" data-toggle="tooltip" title="{1}"><i class="fa fa-edit"></i></a>' \
                   '<a class="delete_row" data-url="{3}" data-id="{0}" data-toggle="tooltip" title="{2}"><i class="fa fa-trash"></i></a>'.format(row.pk, _("تعديل"), _("حذف"), reverse("Items"))
        return super(ItemsJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name_lo__istartswith=search)
        return qs


def get_item_details(request, item_id):
    try:
        item = Items.objects.get(id=item_id)
        data = {
            'id': item.id,
            'name': item.name_lo,
            'description': item.description,
            'price': item.price,
            # إضافة أي تفاصيل أخرى حسب الحاجة
        }
        return JsonResponse({'status': 1, 'data': data})
    except Items.DoesNotExist:
        return JsonResponse({'status': 0, 'message': 'Item not found'})

