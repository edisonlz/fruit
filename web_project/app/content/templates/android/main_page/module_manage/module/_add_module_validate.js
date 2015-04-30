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
                } else {
                    element.addClass('error');
                    error.css("padding-left", "0px")
                    return error.appendTo(element.parent());
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
        return $(form_selector).validate(options);
    };
    jQuery.validator.addMethod("check_num", function (value, element, param) {
        if (parseInt(value) < 1) {
            return false
        } else if (parseInt(value) % 2 == 1) {
            return false
        } else {
            return true
        }
    }, $.validator.format("视频数应为大于0的偶数"));
    jQuery.validator.addMethod("check_video_num", function (value, element, param) {
        var pad_num = parseInt($('#video_count_for_pad').val());
        var phone_num = parseInt($('#video_count_for_phone').val())
        if (pad_num >= 0 && phone_num >= 0) {
            return phone_num <= pad_num
        } else {
            return true
        }
    }, $.validator.format("手机端视频个数不能大于Pad端视频个数"));
    validate_rules = {
        'video_count_for_phone': {
            'required': true,
            'digits': true,
            'maxlength': 6,
            'check_num': true,
            'check_video_num': true
        },
        'video_count_for_pad': {
            'required': true,
            'digits': true,
            'maxlength': 6,
            'check_num': true,
            'check_video_num': true
        }
    }
    var module_type = $('#box_type').val()
    if (module_type != '2' && module_type != '3') {
        validate_rules['cid'] = {
            'required': true,
            'digits': true
        }
    }
    if (module_type != '3') {
        validate_rules['title'] = {
            'required': true
        }
    }

    validate_form('form.validate_module', {
            ignore: ':hidden:not(input.in_validate)',
            rules: validate_rules
        }
    );
})


