# forms.py
from django import forms
from .models import PrinterSetting
from .utils import get_available_printers  # دالة لجلب الطابعات المخزنة في الجهاز.
from .models import Printer
from .models import Category


class PrinterSettingForm(forms.ModelForm):
    class Meta:
        model = PrinterSetting
        fields = ['printer_name', 'paper_size']  # الحقول الموجودة بالفعل

    printer_name = forms.ChoiceField(choices=[], label="اختر الطابعة")

    def __init__(self, *args, **kwargs):
        super(PrinterSettingForm, self).__init__(*args, **kwargs)
        printers = get_available_printers()  # جلب الطابعات المتاحة من جهاز الكمبيوتر.
        self.fields['printer_name'].choices = [(printer, printer) for printer in printers]  # تخصيص قائمة الطابعات



class PrinterForm(forms.ModelForm):
   

    class Meta:
        model = Printer
        fields = ['name', 'model', 'brand', 'ip_address']  # الحقول التي تريد تضمينها في النموذج
        
        
class IPAddressForm(forms.Form):
    ip_address = forms.GenericIPAddressField()
