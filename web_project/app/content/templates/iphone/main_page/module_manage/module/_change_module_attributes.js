function change_content_according_to_box_type() {
            if ($('#box_type').val() === '2') {
                //轮播图模块隐藏图片，跳转
                $("#image_link_div").hide();
                $("#image_div").hide();
                $("#cid_div").hide();
//                $("#module_title_div").show();
                $('#normal-input').removeClass('in_validate')
                $('#video_count_for_phone').rules('remove','check_num')
            } else if($('#box_type').val() === '3') {
                //今日精选模块隐藏图片，跳转，标题
               $("#image_link_div").hide();
                $("#image_div").hide();
                $("#cid_div").hide();
//                $("#module_title_div").hide();
                $('#normal-input').removeClass('in_validate')
                $('#video_count_for_phone').rules('add',{'check_num':true})
            } else{
                $("#image_link_div").show();
                $("#image_div").show();
                $("#cid_div").show();
//                $("#module_title_div").show();
                $('#normal-input').addClass('in_validate')
                $('#video_count_for_phone').rules('add',{'check_num':true})
            }
        }