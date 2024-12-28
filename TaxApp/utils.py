import requests

def get_tax_rate_from_tax_app():
    try:
        # إرسال طلب GET إلى الـ API للحصول على نسبة الضريبة
        response = requests.get('http://127.0.0.1:8000/api/tax_rate/')
        
        # التحقق من أن الاستجابة ناجحة
        if response.status_code == 200:
            data = response.json()
            # محاولة استخراج قيمة tax_rate
            tax_rate = data.get('tax_rate', None)
            if tax_rate is not None and isinstance(tax_rate, (int, float)):
                return tax_rate
            else:
                return 0.15  # قيمة افتراضية إذا كانت tax_rate غير صالحة
        else:
            return 0.15  # قيمة افتراضية إذا كانت الاستجابة غير ناجحة
    except requests.exceptions.RequestException as e:
        # في حال حدوث استثناء عند الاتصال بالخدمة
        print(f"حدث خطأ في الاتصال بـ TaxApp: {e}")
        return 0.15  # قيمة افتراضية في حال حدوث خطأ
