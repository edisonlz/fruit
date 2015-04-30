$(function () {
    var validate_rules;
    validate_form = function (form_selector, options) {
        var default_options;
        console.log("in validate_form")
        console.log(validate_rules)
        default_options = {
            errorPlacement: function (error, element) {

                if (element.is(":checkbox")) {
                    return error.appendTo(element.next())
                } else {
                    element.addClass('error');
                    error.css({"padding-left": "0px","color": "#933", "display": "block"});
                    return error.prependTo(element.parent());
                }
            },
            submitHandler: function (form) {
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
        if($("#url").is(':visible') === true){
            if($("#url").val().length > 0){
                return true
            }else{
                return false
            }
        }else{
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
        'url':{
            'check_url':true,
            'url': true
        },
        'title': 'required',
        'h_image': 'required',
        's_image': 'required',
        'v_image': 'required',
        'video_id': 'required'
    }

    validate_form('form', {
            ignore: ':hidden:not(input.hidden-img)',
            rules: validate_rules
        }
    );
})


