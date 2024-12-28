from django import template

# قم بتسجيل الفلتر
register = template.Library()

@register.filter(name='add_class')
def add_class(field, class_name):
    """إضافة فئة (class) إلى الحقل"""
    return field.as_widget(attrs={'class': class_name})
