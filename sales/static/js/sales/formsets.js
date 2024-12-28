// دالة لتحديث فهرس العناصر
function update_elem_index(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+-)');
    var replacement = prefix + '-' + ndx + '-';
    
    // تحديث الخصائص for و id و name
    if ($(el).attr("for")) {
        $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    }
    if (el.id) {
        el.id = el.id.replace(id_regex, replacement);
    }
    if (el.name) {
        el.name = el.name.replace(id_regex, replacement);
    }
}

// دالة لإضافة صف جديد إلى النموذج
function add_form(btn, prefix) {
    var max_row_count = 1000; // الحد الأقصى لعدد الصفوف (يمكنك تخصيص هذا الرقم حسب الحاجة)
    var row_count = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

    if (row_count < max_row_count) {
        var row = $(".form-row-purshess:last").clone(false).get(0);
        
        // إزالة أي رسائل خطأ سابقة
        $(".errorlist", row).remove();
        $(".text-danger", row).remove();
        $(row).children().removeClass("error");
        $(row).children().removeClass("text-danger");

        // تحديث الرقم المتسلسل للصف
        $(row).find('td:first').text(row_count + 1);

        // تحديث الحقول الجديدة
        $(row).find('.formset-field').each(function() {
            update_elem_index(this, prefix, row_count);
            $(this).val(0); // إعادة تعيين القيم إلى 0
        });

        // إضافة حدث الحذف للصف الجديد
        $(row).find(".delete").click(function() {
            return delete_form(this, prefix);
        });

        // إدراج الصف الجديد بعد آخر صف
        $(row).insertAfter(".form-row-purshess:last").slideDown(300);

        // إعادة تعيين قيم الحقول (مثل الخصم)
        $("#id_" + prefix + "-discount").val(0);
        $(`#id_${prefix}-${row_count}-item`).prop('required', true);

        // تحديث إجمالي عدد الصفوف
        $("#id_" + prefix + "-TOTAL_FORMS").val(row_count + 1);
    }

    return false;
}

// دالة لحذف صف من النموذج
function delete_form(btn, prefix) {
    var totalFormsField = $('#id_' + prefix + '-TOTAL_FORMS');
    var row_count = parseInt(totalFormsField.val());

    if (row_count > 1) {
        var goto_id = $(btn).find('input').val();
        
        if (goto_id) {
            $.ajax({
                url: "/" + window.location.pathname.split("/")[1] + "/formset-data-delete/" + goto_id + "/?next=" + window.location.pathname,
                error: function() {
                    console.log("Error while deleting form data.");
                },
                success: function(data) {
                    $(btn).parents('.form-row-purshess').remove();
                },
                type: 'GET'
            });
        } else {
            $(btn).parents('.form-row-purshess').remove();
        }

        // تحديث عدد الصفوف
        var forms = $('.form-row-purshess');
        totalFormsField.val(forms.length);

        // إعادة فهرسة العناصر بعد الحذف
        forms.each(function(i) {
            $(this).find('.formset-field').each(function() {
                update_elem_index(this, prefix, i);
            });
        });
    }

    return false;
}

// إضافة حدث على زر الإضافة
$("body").on('click', '.add_row', function() {
 
    return add_form($(this), String($(this).attr('id')));
});

// إضافة حدث على زر الحذف
$("body").on('click', '.remove', function() {
    delete_form($(this), String($('.add_row').attr('id')));
});