$(document).ready(function () {
    var desc_obj = {
        1: '480x800',
        2: '1024x600',
        4: '1024x768'
    };
    var term = $('input[name=terminal_type]').attr('value');
    var img_set = $('.imgDesc');
    if (term !== '3') {
        img_set.each(function () {
            $(this).text($.trim($(this).text()) + '(' + desc_obj[term] + ')');
        })
    } else {
        var iphone_desc_arr = ['960x640', '1136x640', '1334x750', '2208x1242'];
        img_set.each(function (index) {
            $(this).text($.trim($(this).text()) + '(' + iphone_desc_arr[index] + ')');
        })
    }
});