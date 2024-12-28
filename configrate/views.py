from django.shortcuts import render
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from .forms import UserForm
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.views import View
from .forms import RegisterForm
from django.urls import reverse
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import QueryDict
from django.utils.translation import gettext as _  

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'configrate/users.html'

    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'id' in request.GET.keys():
            if request.GET.get('id'):
                data = User.objects.filter(pk=request.GET.get('id'))
                result = {'status': 1, 'data': serializers.serialize('json', data)}
            else:
                result = {'status': 0, 'data': ''}
            return JsonResponse(result)
        else:
            form = RegisterForm()
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if request.POST.get('id'):
            data = get_object_or_404(User, pk=int(request.POST.get('id')))
            form = RegisterForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            context = {
                "status": 1,
                "message": _("تمت عملية الحفظ")
            }
        else:
            context = {
                "status": 0,
                "message": form.errors
            }

        return JsonResponse(context)

    def delete(self, request, *args, **kwargs):
        pk = int(QueryDict(request.body).get('id'))
        if pk:
            try:
                data = get_object_or_404(User, pk=pk)
                data.delete()
                msg = _("تمت عملية الحذف")
                result = {'status': 1, 'message': msg}
            except:
                msg = _("خطأ في عملية الحذف")
                result = {'status': 0, 'message': msg}
        else:
            msg = _("لا يوجد أصناف")
            result = {'status': 0, 'message': msg}
        return JsonResponse(result)


class UserDataJson(BaseDatatableView):
    model = User
    columns = [
        'id',
        "first_name",
        "last_name",
        "username",
        "action",
    ]
    order_columns = [
        'id',
        "first_name",
        "last_name",
        "username",
        "action",
    ]
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
                <i class="fa fa-edit"></i> {1}
                </a>
                <a class="btn btn-sm btn-danger text-white delete_row" 
                   data-url="{3}" 
                   data-id="{0}" 
                   data-toggle="tooltip" 
                   title="{2}">
                   <i class="fa fa-trash"></i> {2}
                </a>
            </div>
            '''.format(
                row.pk, _("تعديل"), _("حذف"), reverse("Itemstype")
            )
        else:
            return super(UserDataJson, self).render_column(row, column)

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
