from django.db import models
from configrate.models import Unit, Items_type, Store
from parent.models import BaseModel
from django.utils.translation import gettext_lazy as _  
from input.Category.models import Category 
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Items(BaseModel):
    name_lo = models.CharField(_("اسم الصنف عربي"), max_length=50, unique=True)
    name_fk = models.CharField(_("اسم الصنف إنجليزي"), max_length=50, default="")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    items_type = models.ForeignKey(Items_type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    barcode = models.CharField(_("الباركود"), max_length=50, unique=True)  # حقل باركود مع شرط عدم التكرار
    image = models.ImageField(_("صورة الصنف"), upload_to="item", default="default.jpg")
    purch_price = models.CharField(_("سعر الشراء"), max_length=100)
    salse_price = models.CharField(_("سعر البيع"), max_length=100)
    is_stop = models.BooleanField(default=True)

    def __str__(self):
        return self.name_lo


class StoryItem(BaseModel):
    qty = models.IntegerField(_("الكمية"))
    Items = models.ForeignKey(Items, on_delete=models.CASCADE)
    stor = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    # exp_date = models.CharField(_("تاريخ الإنتهاء"))
    selling_price = models.FloatField(_("سعر البيع"))
    purch_price = models.FloatField(_("سعر الشراء"))


class InventoryItem(models.Model):
    item = models.ForeignKey('Items', on_delete=models.CASCADE)
    purch_price = models.DecimalField(max_digits=10, decimal_places=2)
    salse_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_qty = models.IntegerField()

    def __str__(self):
        return f"{self.item.name} - {self.total_qty}"
