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
            },
            submitHandler: function (form) {
                if($("#state_for_android").is(':checked') || $("#state_for_iphone").is(':checked') && $("#state_for_ipad").is(':checked')){
                   return form.submit();
                }else{
                   alert("请先选择投放平台~~");
                   return false;
                }

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
    validate_rules = {
        'title': 'required',
        'link_to_url': 'url'
    }

    validate_form('form', {
            rules: validate_rules
        }
    );
})