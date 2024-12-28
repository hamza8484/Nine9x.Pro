from django.shortcuts import render
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.views import View
from django.utils.translation import gettext_lazy as _  # استيراد الترجمة
from pos.models import Session
from pos.session.forms import SessionForm
from django.urls import reverse
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import QueryDict

class SessionView(CreateView):

    def get(self, request, *args, **kwargs):
        if 'id' in request.GET.keys():
            if request.GET.get('id'):
                data = Session.objects.filter(pk=request.GET.get('id'))
                result = {'status': 1, 'data': serializers.serialize('json', data)}
            else:
                result = {'status': 0, 'data': ''}
            return JsonResponse(result)
        else:
            Uni = Session.objects.all()
            fileduse = SessionForm()
            context = {
                "Session": Uni,
                "filed": fileduse
            }
        return render(request, 'session/session.html', context)

    def post(self, request, *args, **kwargs):
        form = SessionForm(request.POST)
        if request.POST.get('id'):
            data = get_object_or_404(Session, pk=int(request.POST.get('id')))
            form = SessionForm(request.POST, instance=data)

        session = ''
        if form.is_valid():
            session = form.save(commit=False)
            session.status = "open"
            session.save()
        else:
            print(form.errors)

        if session.id:
            context = {
                "status": 1,
                "message": _("تم الحفظ")  # إضافة الترجمة
            }
        else:
            context = {
                "status": 0,
                "message": _("خطاء في الحفظ")  # إضافة الترجمة
            }
        return JsonResponse(context)

    def delete(self, request, *args, **kwargs):
        pk = int(QueryDict(request.body).get('id'))
        if pk:
            try:
                data = get_object_or_404(Session, pk=pk)
                data.delete()
                msg = _("تم الحذف")  # إضافة الترجمة
                result = {'status': 1, 'message': msg}
            except:
                msg = _("خطاء بالحذف")  # إضافة الترجمة
                result = {'status': 0, 'message': msg}
        else:
            msg = _("لا يوجد الصنف")  # إضافة الترجمة
            result = {'status': 0, 'message': msg}
        return JsonResponse(result)

def edit_status(request):
    if request.method == "POST":
        if request.POST.get("id"):
            Session.objects.filter(id=request.POST.get("id")).update(status="close")
            return JsonResponse({'status': 1, 'message': _("تم التعديل")})  # إضافة الترجمة

    return JsonResponse({'status': 0, 'message': _("not found")})  # إضافة الترجمة


class SessionJson(BaseDatatableView):
    model = Session

    columns = [
        'id',
        "device",
        "start_date",
        "end_date",
        "status",
        "action",
    ]

    order_columns = [
        'id',
        "device",
        "start_date",
        "end_date",
        "status",
        "action",
    ]

    max_display_length = 500
    count = 0

    def render_column(self, row, column):
        if column == "id":
            self.count += 1
            return self.count
        if column == "status":
            if row.status == "open":
                return _("مفتوح")  # إضافة الترجمة
            else:
                return _("أغلاق")  # إضافة الترجمة

        if column == "action":
            options_model = '<a class="edit_status_row" data-url="{2}" data-id="{0}" style="DISPLAY: -webkit-inline-box;"  data-toggle="tooltip" title="{1}"><i class="fa fa-edit"></i></a>'.format(
                row.id, _("تعديل الحالة"), reverse("edit_status"))
            return options_model + ' <a class="edit_row" data-url="{3}" data-id="{0}" style="DISPLAY: -webkit-inline-box;"  data-toggle="tooltip" title="{1}"><i class="fa fa-edit"></i></a><a class="delete_row" data-url="{3}" data-id="{0}"  style="    DISPLAY: -webkit-inline-box;"     data-toggle="tooltip" title="{2}"><i class="fa fa-trash"></i></a>'.format(row.pk, _("تعديل"), _("حذف"), reverse("session"))

        else:
            return super(SessionJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)

        filter_customer = self.request.GET.get('customer', None)
        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part) | Q(customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs
