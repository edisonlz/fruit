$(document).ready(function () {

    //switch the textarea and text
    $(".canBeEdit").dblclick(function () {

        $(this).children('div.text-block').width($(this).width()-2).show();
        $(this).children('div.text-piece').hide();
//        $(this).children('div.text-block').show();
//        $(this).children('div.text-piece').hide();
    });

    //handle the event after clicking 'cancel'
    $(".recover-text").click(function () {
        var textarea_div = $(this).parent();
        textarea_div.hide().next().show();
    });

    //solve the behavior of clicking 'ok'
    $(".modify-text").click(function () {
        var textarea = $(this).prevAll('textarea');
        var id_arr = textarea.attr('id').split('-');
        var module_id = $('#this_module_id').val();
        var attr = id_arr[0];
        var video_id = id_arr[1];
        var value = textarea.val();
        $.ajax({
//            url: '/content/android/update_item_value/subchannel/module/item',
            url: '{{ save_url }}',
            type: "POST",
            dataType: 'json',
            data: {
                channel_id: "{{ this_channel.id }}",
                module_id: module_id,
                video_id: video_id,
                attribute: attr,
                value: value
            },
            success: function (data) {
                $().toastmessage({
                    position: 'middle-center'
                });
                if (data.status === 'success') {
                    textarea.parent().hide().nextAll('.text-piece').text(value).show();
                    $().toastmessage('showSuccessToast', '操作成功');
                } else {
                    $().toastmessage('showErrorToast', '操作失败');
                }
            }
        })
    });

    // Ctrl-Enter pressed
    $(".edit-area").keydown(function (e) {
        if (e.ctrlKey && e.keyCode == 13) {
            $(this).nextAll('.modify-text').triggerHandler('click');
        }
    });
});