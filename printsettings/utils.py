
import win32print

def get_available_printers():
    printers = []
    try:
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None)
        printers_list = [printer[2] for printer in printers]  # استرجاع اسماء الطابعات
    except Exception as e:
        printers_list = []
        print(f"Error: {e}")
    
    return printers_list



