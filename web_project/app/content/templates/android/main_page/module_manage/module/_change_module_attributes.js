function change_content_according_to_box_type() {
            if ($('#box_type').val() === '2') {
                //轮播图模块隐藏图片，跳转
                $("#image_link_div").hide();
                $("#image_div").hide();
                $("#cid_div").hide();
//                $("#module_title_div").show();
                $('#normal-input').removeClass('in_validate')
                $('#video_count_for_pad').rules('remove','check_num')
                $('#video_count_for_phone').rules('remove','check_num')
                $('#video_count_for_pad').attr('title','').attr('data-original-title','视频个数必填')
                $('#video_count_for_phone').attr('title','').attr('data-original-title','视频个数必填')
            } else if($('#box_type').val() === '3') {
                //今日精选模块隐藏图片，跳转，标题
               $("#image_link_div").hide();
                $("#image_div").hide();
                $("#cid_div").hide();
//                $("#module_title_div").hide();
                $('#normal-input').removeClass('in_validate')
                $('#video_count_for_pad').rules('add',{'check_num':true})
                $('#video_count_for_phone').rules('add',{'check_num':true})
                $('#video_count_for_pad').attr('title','').attr('data-original-title','视频个数必填且为大于0的偶数')
                $('#video_count_for_phone').attr('title','').attr('data-original-title','视频个数必填且为大于0的偶数')
            } else{
                $("#image_link_div").show();
                $("#image_div").show();
                $("#cid_div").show();
//                $("#module_title_div").show();
                $('#normal-input').addClass('in_validate')
                $('#video_count_for_pad').rules('add',{'check_num':true})
                $('#video_count_for_phone').rules('add',{'check_num':true})
                $('#video_count_for_pad').attr('title','').attr('data-original-title','视频个数必填且为大于0的偶数')
                $('#video_count_for_phone').attr('title','').attr('data-original-title','视频个数必填且为大于0的偶数')
            }
            $('input').tooltip()
        }