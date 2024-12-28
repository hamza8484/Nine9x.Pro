from django import forms
from pos.models import Session
import datetime
from django.forms.widgets import DateTimeInput
from django.utils.translation import gettext_lazy as _  # استيراد الترجمة

class SessionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        self.fields["start_date"] = forms.DateTimeField(
            label=_('تاريخ البداية'),  # إضافة الترجمة
            widget=forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control float-right"},
            ),
            initial=datetime.datetime.now(),
        )
        self.fields["end_date"] = forms.DateTimeField(
            label=_('تاريخ الإنهاء'),  # إضافة الترجمة
            widget=forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control float-right"},
            ),
            initial=datetime.datetime.now(),
        )
        self.fields["device"].widget.attrs.update({"class": "form-control"})
    
    class Meta:
        model = Session
        fields = "__all__"
