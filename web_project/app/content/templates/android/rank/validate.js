
$(document).ready(function(){
    var validate = function (form_selector, options) {
                var default_options = {
                    errorPlacement: function (error, element) {
                        element.addClass('error');
                        error.css({"padding-left": "0px", "color": "#933", "display": "block"});
                        return error.insertBefore(element);
                    }
                };
                options = $.extend(default_options, options);
                return $(form_selector).validate(options);
            };
            var validate_rules = {
                'cid': {
                    'required': true,
                    'number': true
                },
                'title': 'required'
            };
            validate('form', {
                        ignore: '',
                        rules: validate_rules
                    }
            );

});
