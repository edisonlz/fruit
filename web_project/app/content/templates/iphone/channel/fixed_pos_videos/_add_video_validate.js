$(function () {
    var validate_rules;
    validate_form = function (form_selector, options) {
        var default_options;
        console.log("in validate_form")
        console.log(validate_rules)
        default_options = {
            errorPlacement: function (error, element) {

                if (element.is(":checkbox")) {
                    return error.appendTo(element.next());
                } else if (element.attr('id') === 'original_game_id') {
                    element.addClass('error');
                    error.css({"padding-left": "0px", "color": "#933", "display": "inline"})
                    return error.appendTo(element.next());
                } else {
                    element.addClass('error');
                    error.css({"padding-left": "0px", "color": "#933", "display": "block"});
                    if (element.is(":hidden")) {
                        return element.parent().children().eq(0).before(error);
                    }
                    return error.insertBefore(element);
                }
            },
            submitHandler: function (form) {
                if ($("#game_name").is(':visible') === true) {
                    if ($("#game_name").val().length === 0) {
                        alert("请先通过游戏ID获取游戏信息~~");
                        return false;
                    }
                }
                return form.submit();
            },
            //success: function(label) {
            //     console.log(label)
            //    return label.html("&nbsp;").addClass("checked");
            //  },
            highlight: function (element, errorClass) {
                return $(element).parent().find("." + errorClass).removeClass("checked");
            }
        };
        options = $.extend(default_options, options);
        var mes_obj = {};
        var mes = $.validator.messages;
        for (var k in mes) {
            if (typeof mes[k] !== 'function') {
                mes_obj[k] = mes[k] + ' (｡･ω･｡) ';
            }
        }
        $.extend(mes, mes_obj);
        return $(form_selector).validate(options);
    };
    jQuery.validator.addMethod("check_url", function (value, element, param) {
        if ($("#url").is(':visible') === true) {
            if ($("#url").val().length > 0) {
                return true
            } else {
                return false
            }
        } else {
            return true
        }
    }, $.validator.format("url不能为空"));
//    jQuery.validator.addMethod("check_fixed_position", function (value, element, param) {
//        $.ajax({
//            url: '/android/check_fixed_position/fixed_position_video',
//            type: "POST",
//            dataType: 'json',
//            data: {
//                value: $('#fixed_position').val()
//            },
//            success:function(data){
//                if (data.status == 'success'){
//
//                }else{
//
//                }
//            }
//        })
//            if($("#url").val().length > 0){
//                return true
//            }else{
//                return false
//            }
//        }else{
//            return true
//    }, $.validator.format("url不能为空"));
    validate_rules = {
        'url': {
            'check_url': true,
            'url': true
        },
        'title': 'required',
//        'h_image': 'required',
//        's_image': 'required',
        'game_page_id': 'required',
        'video_id': 'required',
        'original_game_id': {
            'required': true
        },
        'fixed_position': {
            remote: {
                type: 'get',
                url: '/content/android/check_fixed_position/fixed_position_video',
                data: {
                    value: $('#fixed_position').val(),
                    method: 'add',
                    subchannel_id: $('#subchannel_id').val(),
                    module_id: $('#module_id').val()
                }
            }
        }
    };

    validate_form('form', {
            ignore: ':hidden:not(input[id*=normal-input]):not(input[id=slider-input])',
            rules: validate_rules
        }
    );
});

$(document).ready(function () {
    $("button[type='submit']").bind('click', function (e) {
//        $(".container form").bind('submit', function (e) {
        var img_arr = ['h_image', 'v_image'];
        var img_flag = false;
        var fill_flag = false;
        for (var i = 0; i < img_arr.length; i++) {
            var target = $("input[name=" + img_arr[i] + "]");
            if (target.length > 0) {
                img_flag = true;
                if (target.attr('value') !== '') {
                    fill_flag = true;
                    break;
                }
            }
        }
        if (img_flag === true) {
            var prevent_flag = true;
            var mes;
            var s_obj = $("input[name='s_image']");
            console.log('value'+s_obj.attr('value'));
            if (s_obj.length > 0) {
                if (s_obj.attr('value') === '') {
                    mes = "请一定上传轮播图";
                } else {
                    prevent_flag = false;
                }
            } else {
                if (fill_flag) {
                    prevent_flag = false;
                } else {
                    mes = "请至少上传一种类型的图片！"
                }
            }
            if (prevent_flag) {
                e.preventDefault();
                $(this).prevAll('label').remove();
                $('<label class="error" style="padding:0;color: rgb(153, 51, 51); display: block;">' + mes + '</label>')
                    .insertBefore($(this));
            }
        }

    })
});


