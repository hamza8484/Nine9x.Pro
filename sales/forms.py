import datetime
from django import forms
from django.db import models

from django.utils.translation import gettext_lazy as _  # تم تحميل gettext_lazy للتطبيق
from crispy_forms.helper import FormHelper
from django.core.exceptions import ObjectDoesNotExist
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, ButtonHolder, Div
from crispy_forms.bootstrap import InlineRadios, InlineField, FormActions

from sales.models import (SalesInvoicelocal, SalesInvoicelocalDetails)
from configrate.models import Unit, Store
from input.models import Items

from django.urls import reverse_lazy
from datetime import timedelta
from datetime import date
from sales.models import Customer


class SalesInvoiceForm(forms.ModelForm):
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(),
        label=_('المخزن'),  # ترجمة النص
    )

    def __init__(self, *args, **kwargs):
        super(SalesInvoiceForm, self).__init__(*args, **kwargs)
        
        self.fields["customer"] = forms.ModelChoiceField(
            label=_("العميل"),  # ترجمة النص
            queryset=Customer.objects.all(),
        )

        self.fields["discount_item"] = forms.FloatField(
            label=_("إجمالي الخصم "),  # ترجمة النص
            required=False,
            widget=forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                    "value": 0,
                    "placeholder": _("القيمة"),  # ترجمة النص
                }
            ),
        )
      
        self.fields["total_net_bill"] = forms.FloatField(
            label=_("إجمالي الفاتورة"),  # ترجمة النص
            required=False,
            widget=forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                    "placeholder": _("القيمة"),  # ترجمة النص
                }
            ),
        )

        self.fields["date"] = forms.DateField(
            label=_('تاريخ الفاتورة'),  # ترجمة النص
            widget=forms.DateInput(
                attrs={"type": "Date",}
            ),
            initial=datetime.date.today(),
        )
    
        self.fields["store"] = forms.ModelChoiceField(
            label=_('المخزن'),  # ترجمة النص
            queryset=Store.objects.all(), required=False
        )
        self.fields["store"].widget.attrs.update(
            {"class": " store select form-control"}
        )
        try:
            self.fields["statement"].widget.attrs.update({"class": "form-control"})
            self.fields["reference_number"].widget.attrs.update({"class": "form-control"})
            self.fields["code"].widget.attrs.update({"class": "form-control"})
            self.fields["date"].widget.attrs.update({"class": "form-control"})
            self.fields["customer"].widget.attrs.update({"class": "form-control"})
            self.fields["tax"].widget.attrs.update({"class": "form-control"})
            self.fields["check_amount"].widget.attrs.update({"class": "form-control"})
            self.fields["total_amount"].widget.attrs.update({"class": "form-control"})
            self.fields["discount"].widget.attrs.update({"class": "form-control"})
            self.fields["discount_rate"].widget.attrs.update({"class": "form-control"})
        except ObjectDoesNotExist as e:
            raise e

    class Meta:
        model = SalesInvoicelocal
        fields = [
            "code",
            "date",
            "customer",
            "tax",
            "check_amount",
            "amount",
            "statement",
            "reference_number",
            "total_amount",
            "discount",
            "discount_rate",
            'is_stage',
        ]
       
        widgets = {
            "statement": forms.Textarea(attrs={"rows": 1, "class": "form-control","required":False}),
            "store": forms.Select(),
            "discount": forms.NumberInput(
                attrs={"class": "form-control", "oninput": "getPercentag(this)"}
            ),
            "discount_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "oninput": "getPercentag(this)",
                    "min": "0",
                    "max": "100",
                }
            ),
            "code": forms.NumberInput(attrs={"readonly": True}),
            "total_amount": forms.NumberInput(
                attrs={"class": "form-control", "readonly": True}
            ),
            "tax": forms.NumberInput(attrs={"class": "form-control", "readonly": True}),
        }
        labels = {
            "total_amount": _("المجموع"),  # ترجمة النص
            "code": _("رقم الفاتورة"),  # ترجمة النص
            "discount": _("خصم بالمبلغ"),  # ترجمة النص
            "discount_rate": _("خصم بالنسبة %"),  # ترجمة النص
            "total_net_bill": _("إجمالي بعد الخصم"),  # ترجمة النص
            "tax": _("ضريبة 15 %"),  # ترجمة النص
        }


class SalesInvoicelocalDetailsForm(forms.ModelForm):
    """Form For Sales Invoicelocal Details"""
    
    def __init__(self, *args, **kwargs):
        super(SalesInvoicelocalDetailsForm, self).__init__(*args, **kwargs)
        self.fields["item"] = forms.ModelChoiceField(
            label=_("الصنف"),  # ترجمة النص
            queryset=Items.objects.all(),
        )
        self.fields["unit"].widget.attrs.update(
                {
                    "class": "formset-field form-control",
                    "onchange":"get_store_items_data(this)",
                }
            )

        self.fields["total_price"] = forms.FloatField(
            label=_("المجموع الكلي"),  # ترجمة النص
            required=False,
            widget=forms.NumberInput(
                attrs={
                    "oninput": "getPrice(this)",
                    "readonly": True,
                    "class": "formset-field form-control sss",
                    "style": "width: 150px !important",
                }
            ),
        )

        try:
            self.fields["item"].widget.attrs.update(
                {
                    "class": "formset-field form-control",
                    "style": "width: 150px !important",
                    "onchange": "get_Price_item(this)",
                    "required": True,
                }
            )

            self.fields["statement"].widget.attrs.update({"required": False})
            del self.fields["statement"]

            self.fields["item_specification"].widget.attrs.update(
                {"required": False}
            )
            del self.fields["item_specification"]
        except:
            pass


    qty_store = forms.IntegerField(
        label=_("الكمية المتوفرة"),  # ترجمة النص
        widget=forms.NumberInput(attrs={"class": "formset-field form-control","readonly": True,"style": "width: 100px !important"})
    )

    class Meta:
        model = SalesInvoicelocalDetails

        fields = [
            "item",
            "unit",
            "qty",
            "statement",
            "discount",
            "discount_rate",
            "store",
            "selling_price",
        ]

        widgets = {
            "qty_store":forms.NumberInput(
                attrs={
                    "class": "formset-field form-control sss",
                    "style": "width: 100px !important",
                }
            ),
            "total_price": forms.NumberInput(
                attrs={
                    "class": "formset-field form-control sss",
                    "style": "width: 100px !important",
                }
            ),
            "qty": forms.NumberInput(
                attrs={
                    "class": "formset-field form-control sss",
                    "step": 1,
                    "oninput": "getTotal(this)",
                    "style": "width: 100px !important",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "formset-field form-control sss",
                    "style": "width: 100px !important",
                }
            ),
            "store": forms.Select(
                attrs={
                    "class": " formset-field form-control sss",
                    "style": "width: 100px !important",
                }
            ),
            "statement": forms.TextInput(
                attrs={
                    "class": "formset-field form-control sss",
                    "style": "width: 100px !important",
                }
            ),
            "discount": forms.NumberInput(
                attrs={
                    "class": "sss formset-field form-control",
                    "oninput": "getTotal(this)",
                    "style": "width: 100px !important",
                }
            ),
            "discount_rate": forms.NumberInput(
                attrs={
                    "class": "sss formset-field form-control",
                    "style": "width: 150px !important",
                    "oninput": "getTotal(this)",
                    "min": "0",
                    "max": "100",
                }
            ),
            "selling_price": forms.NumberInput(
                attrs={
                    "class": "sss formset-field form-control",
                    "style": "width: 100px !important",
                }
            ),
        }
        labels = {
            "total_price": "",
            "item": _("الصنف"),  # ترجمة النص
            "unit": _("الوحدة"),  # ترجمة النص
            "qty": _("الكمية"),  # ترجمة النص
            "expire_date": _("تاريخ انتهاء الصلاحية"),  # ترجمة النص
            "statement": _("الوصف"),  # ترجمة النص
            "discount": _("الخصم"),  # ترجمة النص
            "discount_rate": _("معدل الخصم"),  # ترجمة النص
            "store": _("المخزن"),  # ترجمة النص
            "selling_price": _("السعر البيع"),  # ترجمة النص
            "item_specification": _("مواصفات الصنف"),  # ترجمة النص
        }
