function change_content_according_to_box_type() {
            if ($('#box_type').val() === '2') {
                //轮播图模块隐藏图片，跳转
                $("#cid_div").hide();
//                $("#module_title_div").show();
                $('#video_count_for_pad').rules('remove','check_num')
            } else if($('#box_type').val() === '3') {
                $("#cid_div").hide();
//                $("#module_title_div").hide();
                $('#video_count_for_pad').rules('add',{'check_num':true})
            } else{
                $("#cid_div").show();
//                $("#module_title_div").show();
                $('#video_count_for_pad').rules('add',{'check_num':true})
            }
        }