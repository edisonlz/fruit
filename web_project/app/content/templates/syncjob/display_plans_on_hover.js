$(document).ready(function(){
    var tab = $('table#table-content');
            var fetch_btn = $("#fetch_btn");
            var plan_div = $("#display_plan");
            var distance = {
                compute: function () {
                    this.width = tab.width();
                    this.right = $(window).width() - tab.offset().left - this.width;
                    console.log(this.right);
//                    console.log(fetch_btn.offset().top);
                    this.top = fetch_btn.offset().top + fetch_btn.height() + 10;
                },
                initial: function () {
                    this.compute();
                    plan_div.css({top: this.top, right: this.right});  // initial position
                }
            };
            distance.initial();

            var check_mouse = function(){
                    if ($("#display_plan:hover").length){
                    } else {
                        plan_div.hide().css({width: 0, height: 0});
                    }
                };

            fetch_btn.hover(function () {
                distance.compute();
                plan_div.show().animate({top: distance.top, width: distance.width, height: 400, right: distance.right});
            }, function() {
                setTimeout(check_mouse, 500)
            });
            plan_div.hover(function(){

            }, function(){
                setTimeout(check_mouse, 500)
                });
});
