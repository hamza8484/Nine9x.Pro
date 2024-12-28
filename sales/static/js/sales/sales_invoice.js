// دالة للحصول على سعر المنتج بناءً على المخزن
function get_Price_item(element_id) {
    let index = element_id.name.split('-');
    let id_item = parseInt($(`#id_SalesInvoicelocalDetails-${index[1]}-item`).val());
    let id_store = $("#id_store").val();

    if (!id_store) {
        alert("يجب عليك اختيار المخزن");
        return;
    }

    $.ajax({
        url: '/get_store_items/',
        data: { "id_item": id_item, "id_store": id_store },
        method: 'GET',
        success: function(data) {
            let form_data = JSON.parse(data.data);
            // التفاعل مع البيانات المستلمة من السيرفر (بإضافة الشرح المناسب)
        },
        error: function(xhr, status, error) {
            console.error('Error fetching store item price:', error);
            alert("حدث خطأ أثناء جلب البيانات.");
        }
    });
}

// دالة للحصول على بيانات المنتج من المخزن
function get_store_items_data(element_id) {
    let index = element_id.name.split('-');
    let id_item = parseInt($(`#id_SalesInvoicelocalDetails-${index[1]}-item`).val());
    let id_store = $("#id_store").val();

    if (!id_store) {
        alert("يجب عليك اختيار المخزن");
        return;
    }

    $.ajax({
        url: '/get_store_items_data/',
        data: { "id_item": id_item, "id_store": id_store },
        method: 'GET',
        success: function(data) {
            let form_data = JSON.parse(data.data)[0].fields;
            $(`#id_SalesInvoicelocalDetails-${index[1]}-qty_store`).val(form_data['qty']);
            $(`#id_SalesInvoicelocalDetails-${index[1]}-selling_price`).val(form_data['selling_price']);
        },
        error: function(xhr, status, error) {
            console.error('Error fetching store item data:', error);
            alert("حدث خطأ أثناء جلب البيانات.");
        }
    });
}

// دالة لحساب إجمالي المبلغ
function getTotal(element_id) {
    let index = element_id.name.split('-');
    let qty = parseFloat($(`#id_SalesInvoicelocalDetails-${index[1]}-qty`).val()) || 0;
    let price = parseFloat($(`#id_SalesInvoicelocalDetails-${index[1]}-selling_price`).val()) || 0;
    let discount = parseFloat($(`#id_SalesInvoicelocalDetails-${index[1]}-discount`).val()) || 0;

    let total_price = (qty * price) - discount;
    $(`#id_SalesInvoicelocalDetails-${index[1]}-total_price`).val(total_price);

    let discount_rate = (discount * 100) / (qty * price);
    $(`#id_SalesInvoicelocalDetails-${index[1]}-discount_rate`).val(discount_rate);

    getAlltotal();
    getAllDiscountItem();
}

// دالة لحساب إجمالي المبالغ الكلية
function getAlltotal() {
    let total_debit = 0;
    $('input[id$="-total_price"]').each(function() {
        total_debit += parseFloat($(this).val()) || 0;
    });
    $("#id_total_amount").val(total_debit);
    getNettotal();
}

// دالة لحساب إجمالي الخصومات
function getAllDiscountItem() {
    let total_discount = 0;
    $('input[id$="-discount"]').each(function() {
        total_discount += parseFloat($(this).val()) || 0;
    });
    $("#id_discount_item").val(total_discount);
}

// دالة لحساب المجموع النهائي بعد الخصم
function getNettotal() {
    let total = parseFloat($('#id_total_amount').val()) || 0;
    let discount = parseFloat($('#id_discount').val()) || 0;
    $("#id_total_net_bill").val(total - discount);
}

// دالة للتحقق من صحة المدخلات
function is_valied() {
    let div = '<span class="text-danger">';
    let amount = parseFloat($('#id_amount').val()) || 0;
    let total1 = parseFloat($('#id_total_net_bill').val()) || 0;
    let check_amount = parseFloat($('#id_check_amount').val()) || 0;

    if (amount !== total1 && amount !== 0) {
        div += `- ${"المبلغ غير صحيح"}<br>`;
        alert("المبلغ غير صحيح", 'alert alert-danger');
        $('#id_amount').parent().append(div);
        return false;
    }

    if (check_amount > total1 && $("#id_payment_method").val() === '4') {
        div += `- ${"المبلغ المدفوع بالشيك أكبر من المجموع الكلي"}<br>`;
        $('#id_check_amount').parent().append(div);
        alert("المبلغ المدفوع بالشيك أكبر من المجموع الكلي", 'alert alert-danger');
        return false;
    }

    return true;
}

// إرسال النموذج باستخدام AJAX والتحقق من صحة البيانات
$(document).on('submit', '#myform_invoic', function(e) {
    e.preventDefault();
    $(".text-danger").remove(); // إزالة الأخطاء السابقة
    let isValid = is_valied();

    if (isValid) {
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: $(this).serialize(),
            success: function(data) {
                if (data.status == 1) {
                    clearForm();
                    alert(data.message);
                    $('.datatable_list').DataTable().ajax.reload();
                } else if (data.status == 0) {
                    displayErrors(data);
                } else {
                    alert('حدث خطأ غير متوقع.');
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', error);
                alert('حدث خطأ أثناء إرسال البيانات.');
            }
        });
    }
});

// عرض الأخطاء في النموذج إذا كانت هناك أخطاء
function displayErrors(data) {
    if (data.error) {
        let errorData = JSON.parse(data.error.error);
        $.each(errorData, function(i, value) {
            let errorMessage = `<span class="text-danger">${value.join('<br>')}</span>`;
            $(`#id_${data.error.form_id}-0-${i}`).parent().append(errorMessage);
        });
    }
}

// مسح البيانات بعد إرسال النموذج بنجاح
function clearForm() {
    let form_id = '#myform_invoic';
    $(form_id)[0].reset();
    $('textarea').text('');
    $('select').each(function() {
        $(this).prop('selectedIndex', 0);
    });
    $("#cash").addClass("hidden");
    $("#check").addClass("hidden");
    $("#cash_check").addClass("hidden");
    $("#check_amount").addClass("hidden");
}

// حذف صف من الجدول
$(document).on('click','.delete_row',function(){
    if (confirm('هل حقا تريد الحذف؟')) {
        let id_row = $(this).data('id');
        $.ajax({
            url: $(this).data('url'),
            data: { 'id': id_row },
            method: 'DELETE',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrf);
            },
            success: function (data) {
                if (data.status == 1) {
                    alert(data.message);
                    $('.datatable_list').DataTable().ajax.reload();
                } else if (data.status == 0) {
                    alert(data.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error deleting row:', error);
                alert("حدث خطأ أثناء الحذف.");
            }
        });
    }
});
