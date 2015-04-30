$(document).ready(function () {
//设置主内容区域和表格同宽
    var main_table = $(document.getElementsByClassName('table')[0]);
    if (main_table.width() <= 720) {
        main_table.animate({width: 720});
        main_table.parent().animate({display: 'inline-block', width: 720});
    } else {
        main_table.parent().css('display', 'inline-block');
    }
});