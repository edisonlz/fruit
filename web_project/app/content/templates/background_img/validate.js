
$(document).ready(function(){
    var validate = function (form_selector, options) {
                var default_options = {
                    errorPlacement: function (error, element) {
                        element.addClass('error');
                        error.css({"padding-left": "0px", "color": "#933", "display": "block"});
                        return error.appendTo(element.parent());
                    }
                };
                options = $.extend(default_options, options);
                return $(form_selector).validate(options);
            };
            var validate_rules = {
                'expired_at': 'required',
                'effect_at': 'required',
                'normal-input': 'required',
                'image': 'required',
                'image_4s': 'required',
                'image_5s': 'required',
                'image_6': 'required',
                'image_6plus': 'required'
            };
            validate('form', {
                        ignore: '',
                        rules: validate_rules
                    }
            );

})
