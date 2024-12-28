from django.shortcuts import render
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views #new
from django.views import View
from configrate.models import Items_type
from .forms import items_typeForm
from django.utils.translation import gettext as _  # إضافة الترجمة
from django.urls import reverse
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import QueryDict

class items_type_item(CreateView):

    def get(self, request, *args, **kwargs):
        if 'id' in request.GET.keys():
            if request.GET.get('id'):
                data=Items_type.objects.filter(pk=request.GET.get('id'))
                result={'status':1,'data':serializers.serialize('json',data)}
            else:
                result={'status':0,'data':''}
            return JsonResponse(result)
        else:
            Uni=Items_type.objects.all()
            fileduse=items_typeForm()
            context={
                "items_type":Uni,
                "filed":fileduse
            }
        
        return render(request, 'configrate/itemstype/items_type.html',context)


    def post(self, request, *args, **kwargs):
        form = items_typeForm(request.POST)
        if request.POST.get('id'):
            data=get_object_or_404(Items_type, pk=int(request.POST.get('id')))
            form=items_typeForm(request.POST, instance=data)
        
        items_type = ''
        if form.is_valid():
            items_type = form.save()

        if items_type.id:
            context = {
                "status": 1,
                "message": _("تمت عملية الحفظ")  # استخدام الترجمة
            }
        else:
            context = {
                "status": 0,
                "message": _("خطأ في عملية الحفظ")  # استخدام الترجمة
            }
        return JsonResponse(context)

    def delete(self, request, *args, **kwargs):
        pk = int(QueryDict(request.body).get('id'))
        if pk:
            try:
                data = get_object_or_404(Items_type, pk=pk)
                data.delete()
                msg = _("تمت عملية الحذف")  # استخدام الترجمة
                result = {'status': 1, 'message': msg}
            except:
                msg = _("خطأ في عملية الحذف")  # استخدام الترجمة
                result = {'status': 0, 'message': msg}
        else:
            msg = _("لا يوجد أصناف")  # استخدام الترجمة
            result = {'status': 0, 'message': msg}
        return JsonResponse(result)


class items_typeJson(BaseDatatableView):
    # The model we're going to show
    model = Items_type

    # define the columns that will be returned
    columns = [
        'id',
        "name_lo",
        "name_fk",
        "action",
    ]

    # define column names that will be used in sorting
    order_columns = [
        'id',
        "name_lo",
        "name_fk",
        "action",
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    max_display_length = 500
    count = 0
    
    def render_column(self, row, column):
        if column == "id":
            self.count += 1
            return self.count
        if column == "action":
            return '''
            <div class="d-flex justify-content-center align-items-center" style="height: 100%;">
                <a class="btn btn-sm btn-primary text-white mr-2 edit_row" 
                   data-url="{3}" 
                   data-id="{0}" 
                   data-toggle="tooltip" 
                   title="{1}">
                   <i class="fa fa-edit"></i> {2}
                </a>
                <a class="btn btn-sm btn-danger text-white delete_row" 
                   data-url="{3}" 
                   data-id="{0}" 
                   data-toggle="tooltip" 
                   title="{4}">
                   <i class="fa fa-trash"></i> {5}
                </a>
            </div>
            '''.format(
                row.pk, _("تعديل"), _("تعديل"), reverse("Itemstype"),
                _("حذف"), _("حذف")
            )
        else:
            return super(items_typeJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)
        return qs
