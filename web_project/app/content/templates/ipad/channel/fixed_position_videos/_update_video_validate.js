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
                if($("#game_name").is(':visible') === true){
                    if($("#game_name").val().length === 0){
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
    validate_rules = {
        'url':{
            'check_url':true,
            'url': true
        },
        'title': 'required',
        'h_image': 'required',
        'game_page_id': 'required',
        'video_id': 'required',
        'original_game_id':{
            'required': true
        },
        'fixed_position': {
            remote:{
                type:'get',
                url: '/content/ipad/check_fixed_position/fixed_position_video',
                data:{
                    value: $('#fixed_position').val(),
                    method: 'update',
                    subchannel_id: $('#subchannel_id').val(),
                    module_id: $('#module_id').val(),
                    video_id: $('#id').val()
                }
            }
        }
    }

    validate_form('form', {
            ignore: ':hidden:not(input[id*=screen-input])',
            rules: validate_rules
        }
    );
})


