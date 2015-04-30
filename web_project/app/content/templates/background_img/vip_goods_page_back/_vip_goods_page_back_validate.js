$(function () {
    var validate_rules;
    validate_form = function (form_selector, options) {
        var default_options;
        console.log("in validate_form")
        console.log(validate_rules)
        default_options = {
            errorPlacement: function (error, element) {

                if (element.is(":checkbox")) {
                    return error.prependTo(element.parent());
                } else {
                    element.addClass('error');
                    error.css({"padding-left": "0px","color": "#933", "display": "block"});
                    return error.prependTo(element.parent());
                }
            }
//            highlight: function (element, errorClass) {
//                return $(element).parent().find("." + errorClass).removeClass("checked");
//            }
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
    validate_rules = {
        'vip_img': 'required',
        'vip_img_hd': 'required'
    }

    validate_form('form', {
            ignore: ':hidden:not(input[id*=big-input])',
            rules: validate_rules
        }
    );
})