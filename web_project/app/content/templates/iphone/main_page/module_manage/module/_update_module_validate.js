$(function () {
    var validate_rules;
    validate_form = function (form_selector, options) {
        var default_options;
        console.log("in validate_form")
        console.log($(form_selector))
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
    validate_rules = {
        'title': {
            'required': true
        },
        'video_count_for_phone': {
            'required': true,
            'digits': true,
            'maxlength': 6,
            'check_num': true
        }
    }
    if ('{{ module.box_type_to_s }}' != 'slider' && '{{ module.box_type_to_s}}' != 'under_slider') {
        validate_rules['cid'] = {
            'required': true,
            'digits': true
        }
    }
    if ('{{ module.box_type_to_s}}' != 'under_slider') {
        validate_rules['title'] = {
            'required': true
        }
    }
    if ('{{ module.box_type_to_s}}' === 'slider') {
        validate_rules['video_count_for_phone'] = {
            'required': true,
            'digits': true,
            'maxlength': 6
        }
    }
//    validate_rules['normal_img'] = {
//        'required': true
//    }
    validate_form('form.validate_module', {
            ignore: ':hidden:not(input[id*=normal-input])',
            rules: validate_rules
        }
    );
})


