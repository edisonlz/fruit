// below function can only be used for non video page
function collect_change_box_ids() {
    var box_id_array = [];
    var box_ids;
    $("input:checkbox:checked.box-state-tag").each(function () {
        box_id_array.push($(this).parent().parent().attr('value'))
    });
    box_ids = box_id_array.join(",");
    return box_ids;
}


function is_all_boxes_checked() {
    var checked_boxs = $("input:checkbox:checked.box-state-tag");
    var boxs = $("input:checkbox.box-state-tag");
    var all_pick_box = $("#state-all-pick");
    if (checked_boxs.length === boxs.length) {
        all_pick_box.prop('checked', true);
    } else {
        all_pick_box.prop('checked', false);
    }
}

$(document).ready(function () {
    $('#state-all-pick').click(function () {
        if ($(this).is(':checked')) {
            $("input:checkbox.box-state-tag").prop("checked", true)
        } else {
            $("input:checkbox:checked.box-state-tag").attr("checked", false)
        }
    });
    $('input:checkbox.box-state-tag').click(function () {
        is_all_boxes_checked();
    });
//    $('.box-state').click(function () {
//        var source = {
//            '1': '开启',
//            '0': '关闭'
//        };
//        var val = $(this).attr("value");
//        var box_ids = collect_change_box_ids();
//        if (box_ids.length > 0) {
//            $.ajax({
//                url: '/content/update_items_state',
//                type: "POST",
//                dataType: 'json',
//                data: {
//                    item_ids: box_ids,
//                    value: val,
//                    target_model: 'AndroidSubChannelModule'
//                },
//                success: function (data) {
//                    $().toastmessage({
//                        position: 'middle-center'
//                    });
//
//                    if (data.status === 'success') {
//                        for (var i = 0; i < data.item_ids.length; i++) {
//                            $('#status_' + data.item_ids[i]).html(source[val])
//                        }
//                        $().toastmessage('showSuccessToast', '操作成功');
//                    } else {
//                        $().toastmessage('showErrorToast', '操作失败');
//                    }
//                    $("input:checkbox.box-status-tag").prop('checked', false);
//                    $('#state-all-pick').prop("checked", false)
//                }
//            })
//        }
//    });
});