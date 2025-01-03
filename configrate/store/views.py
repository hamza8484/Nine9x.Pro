from django.shortcuts import render
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views #new
from django.views import View
from configrate.models import Store
from .forms import storeForm
from django.utils.translation import gettext as _  # إضافة استيراد الترجمة

class store_item(CreateView):

    def get(self, request, *args, **kwargs):
        Uni = Store.objects.all()
        fileduse = storeForm()
        context = {
            "store": Uni,
            "filed": fileduse
        }
        return render(request, 'configrate/store/store.html', context)

    def post(self, request, *args, **kwargs):
        form = storeForm(request.POST)
        store = ''
        if form.is_valid():
            store = form.save()

        if store.id:
            context = {
                "status": 1,
                "message": _("تم الحفظ")  # استخدام الترجمة
            }
        else:
            context = {
                "status": 0,
                "message": _("خطأ في الحفظ")  # استخدام الترجمة
            }
        return JsonResponse(context)

class storeJson(BaseDatatableView):
    # The model we're going to show
    model = Store

    # define the columns that will be returned
    columns = [
        'id',
        "name_lo",
        "name_fk",
        "is_stop",
    ]

    # define column names that will be used in sorting
    order_columns = [
        'id',
        "name_lo",
        "name_fk",
        "is_stop",
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    max_display_length = 500
    count = 0

    def render_column(self, row, column):
        if column == "is_stop":
            if row.is_stop:
                return _("مفعل")  # استخدام الترجمة
            else:
                return _("موقف")  # استخدام الترجمة
        if column == "id":
            self.count += 1
            return self.count
        else:
            # We want to render store as a custom column
            return super(storeJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)

        # more advanced example using extra parameters
        filter_customer = self.request.GET.get('customer', None)

        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part) | Q(customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs
