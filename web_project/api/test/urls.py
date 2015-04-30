#coding=utf-8

datas = [
    ######## 首页视频
    ### iphone 首页
    # iphone v3.8 support user-type-video
    # {
    #     "new": "http://localhost:10000/interface/ios_v3/box_contents_with_slider_playlist_and_url?ver=4.3.2&client_type=phone"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ios_v3/box_contents_with_slider_playlist_and_url?ver=4.3.2&client_type=phone"
    # },
    # #iphone v3.4 support mon-pay-video
    # {
    #     "new": "http://localhost:10000/interface/ios_v3/box_contents_with_slider_playlist_and_url?ver=3.4&client_type=phone"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ios_v3/box_contents_with_slider_playlist_and_url?ver=3.4&client_type=phone"
    # },
    #iphone v3.3
    # {
    #     "new": "http://test.api.cms.m.youku.com/interface/ios_v3/box_contents_with_slider_playlist_and_url?ver=4.3&client_type=phone"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ios_v3/box_contents_with_slider_playlist_and_url?ver=4.3&client_type=phone"
    # },
    # #
    #
    # #iphone v3.2.2
    # {
    #     "new": "http://localhost:10000/interface/ios_v3/box_contents_with_slider_and_url?client_type=phone"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ios_v3/box_contents_with_slider_and_url?client_type=phone"
    # },
    # #iphone v3.2
    # {
    #     "new": "http://localhost:10000/interface/ios_v3/box_contents_with_slider?client_type=phone"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ios_v3/box_contents_with_slider?client_type=phone"
    # },
#     # iphone v3.2 接口已经不再使用（线上看不到日志）
#
#     ### android 首页
#     #android <= v3.2
#     {
#         "new": "http://localhost:10000/interface/android_v3/contents"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/contents"
#     },
#     #android v3.3
#     {
#         "new": "http://localhost:10000/interface/android_v3/contents?show_video_list=1"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/contents?show_video_list=1"
#     },
#     #android v3.4
#     {
#         "new": "http://localhost:10000/interface/android_v3/contents?show_video_list=1&show_paid_video=1"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/contents?show_video_list=1&show_paid_video=1"
#     },
#     #android v3.5
#     {
#         "new": "http://localhost:10000/interface/android_v3/contents?show_video_list=1&show_paid_video=1&show_slider=1"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/contents?show_video_list=1&show_paid_video=1&show_slider=1"
#     },
#     #android v3.7
#     {
#         "new": "http://localhost:10000/interface/android_v3/contents?show_video_list=1&show_paid_video=1&show_slider=1&show_game_information=1"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/contents?show_video_list=1&show_paid_video=1&show_slider=1&show_game_information=1"
#     },
#     #android v4.1
#     {
#         "new": "http://localhost:10000/interface/android_v3/contents?show_video_list=1&show_paid_video=1&show_slider=1&show_game_information=1&show_live_broadcast=1"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/contents?show_video_list=1&show_paid_video=1&show_slider=1&show_game_information=1&show_live_broadcast=1"
#     },
#     #TODO: can not check by this tool
#     # #android v4.4 use new unit-layout
#     # {
#     #     "new": "http://localhost:10000/interface/android_v3/contents?ver=4.4&device_type=phone"
#     #     ,
#     #     "old": "http://cms.m.youku.com/interface/android_v3/contents?ver=4.4&device_type=phone"
#     # },
#
#
    # # checked
    # ### ipad 首页
    # #ipad < v3.0.2
    # {
    #     "new": "http://localhost:10000/interface/ipad_v3/index_videos"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ipad_v3/index_videos"
    # },
    # #ipad v3.0.2
    # {
    #     "new": "http://localhost:10000/interface/ipad_v3/index_videos_with_playlist"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ipad_v3/index_videos_with_playlist"
    # },
    # #ipad v3.2 # support mon_pay video
    # {
    #     "new": "http://localhost:10000/interface/ipad_v3/index_videos_with_playlist?ver=3.2"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ipad_v3/index_videos_with_playlist?ver=3.2"
    # },
    # #ipad v3.9.5 # support jump tag
    # {
    #     "new": "http://localhost:10000/interface/ipad_v3/index_videos_with_playlist?ver=3.9.5"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ipad_v3/index_videos_with_playlist?ver=3.9.5"
    # },
#
#     ######## 频道视频
#     #iphone 1
#     {
#         "new": "http://localhost:10000/interface/ios_v3/channel_videos.json?channel_id=97"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/channel_videos.json?channel_id=1007"
#     },
#     #iphone 2
#     {
#         "new": "http://localhost:10000/interface/ios_v3/channel_videos.json?channel_id=96"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/channel_videos.json?channel_id=96"
#     },
# ######## 频道视频
#     #iphone 1
#     {
#         "new": "http://localhost:10000/interface/ios_v3/channel_videos?channel_id=97"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/channel_videos?channel_id=1007"
#     },
#     #iphone 2
#     {
#         "new": "http://localhost:10000/interface/ios_v3/channel_videos?channel_id=96"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/channel_videos?channel_id=96"
#     },
#     #ipad
#     {
#         "new": "http://localhost:10000/interface/ipad_v3/channel_videos?channel_id=96"
#         ,
#         "old": "http://cms.m.youku.com/interface/ipad_v3/channel_videos?channel_id=96"
#     },
# #
    # ######## 频道
    # #iphone v3.0
    # {
    #     "new": "http://localhost:10000/interface/ios_v3/channels.json"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ios_v3/channels.json"
    # },
    # ######## 频道
    #iphone v3.0
    # {
    #     "new": "http://localhost:10000/interface/ios_v3/channels.json"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ios_v3/channels.json"
    # },
#     #iphone v3.2
#     {
#         "new": "http://localhost:10000/interface/ios_v3/channels_with_choiceness_state_and_icons?updated_at=1416482976"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/channels_with_choiceness_state_and_icons?updated_at=1416482976"
#     },
#     #
#     #TODO: has not check
#     # TODO: has not completed or error
#     # #android  #type: 0优酷频道，1编辑推荐频道
#     # {
#     #     "new": "http://localhost:10000/interface/android_v3/channels.json?type=0"
#     #     ,
#     #     "old": "http://cms.m.youku.com/interface/android_v3/channels.json?type=0"
#     # },
#
#     #ipad v3.0 checked
#     {
#         "new": "http://localhost:10000/interface/ipad_v3/channels"
#         ,
#         "old": "http://cms.m.youku.com/interface/ipad_v3/channels"
#     },
#     # checked
#     # ipad v3.1 #ver >= 3.1时，会显示营销类频道
#     {
#         "new": "http://localhost:10000/interface/ipad_v3/channels?ver=3.1"
#         ,
#         "old": "http://cms.m.youku.com/interface/ipad_v3/channels?ver=3.1"
#     },
# #
#
#     ######## 子频道标签
#     #iphone v3.2.2
#     {
#         "new": "http://localhost:10000/interface/ios_v3/sub_channels?cid=88"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/sub_channels?cid=88"
#     },
#     #iphone v3.4 #当ver >= 3.4时，电影频道才会显示"会员"子频道
#     {
#         "new": "http://localhost:10000/interface/ios_v3/sub_channels?cid=88&ver=3.4"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/sub_channels?cid=88&ver=3.4"
#     },
#
    # #ipad v3 checked
    # {
    #     "new": "http://localhost:10000/interface/ipad_v3/sub_channels?cid=96"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ipad_v3/sub_channels?cid=96"
    # },
    # #ipad v3.2 #ver >= 3.2时，会显示“会员”子频道
    # {
    #     "new": "http://localhost:10000/interface/ipad_v3/sub_channels?cid=96&ver=3.2"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ipad_v3/sub_channels?cid=96&ver=3.2"
    # },
#
#     #android
#     {
#         "new": "http://localhost:10000/interface/android_v3/sub_channels?cid=96"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/sub_channels?cid=96"
#     },
#
#
#     ######## 子频道内容
#     #iphone 3.2.2
#     {
#         "new": "http://localhost:10000/interface/ios_v3/sub_channel_details?sub_channel_id=234"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/sub_channel_details?sub_channel_id=1"
#     },
# #     #iphone 3.3
#     {
#         "new": "http://localhost:10000/interface/ios_v3/sub_channel_details_with_playlist?sub_channel_id=234"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/sub_channel_details_with_playlist?sub_channel_id=1"
#     },
#     #iphone 3.4 # ver大于等于3.4时，会支持包月付费视频
#     {
#         "new": "http://localhost:10000/interface/ios_v3/sub_channel_details_with_playlist?sub_channel_id=234&ver=3.4"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/sub_channel_details_with_playlist?sub_channel_id=1&ver=3.4"
#     },
#     #iphone 3.9 # ver大于等于3.9时，会支持子频道精选页的游戏视频（包括两种：跳转到列表、跳转到游戏详情）
#     {
#         "new": "http://localhost:10000/interface/ios_v3/sub_channel_details_with_playlist?sub_channel_id=234&ver=3.9"
#         ,
#         "old": "http://cms.m.youku.com/interface/ios_v3/sub_channel_details_with_playlist?sub_channel_id=1&ver=3.9"
#     },
#
    # #ipad v3  checked
    # {
    #     "new": "http://localhost:10000/interface/ipad_v3/sub_channel_details?sub_channel_id=41"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ipad_v3/sub_channel_details?sub_channel_id=41"
    # },
    # #ipad v3.2 # ver >= 3.2时，支持会员包月视频，会员包月视频会多一个is_mon_pay_video字段
    # {
    #     "new": "http://localhost:10000/interface/ipad_v3/sub_channel_details?sub_channel_id=41&ver=3.2"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/ipad_v3/sub_channel_details?sub_channel_id=41&ver=3.2"
    # },
#
#     #android v3.5
#     {
#         "new": "http://localhost:10000/interface/android_v3/sub_channel_details?sub_channel_id=1"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/sub_channel_details?sub_channel_id=349"
#     },
#     #android v3.7 # ver >= 3.7时， 会显示游戏的信息
#     {
#         "new": "http://localhost:10000/interface/android_v3/sub_channel_details?sub_channel_id=1&show_game_information=1"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/sub_channel_details?sub_channel_id=349&show_game_information=1"
#     },
#     #android v4.0 # ver >= 4.0时， 会显示has_brands_headline字段（该字段决定该子频道是否用品牌官网的内容替换轮播图）
#     {
#         "new": "http://localhost:10000/interface/android_v3/sub_channel_details?sub_channel_id=1&show_game_information=1&ver=4.0"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/sub_channel_details?sub_channel_id=349&show_game_information=1&ver=4.0"
#     },
#     #android v4.2 # ver >= 4.2时:
#     #  才会显示游戏模块/游戏banner模块；
#     #  才会显示'子频道轮播图/游戏模块/游戏banner模块'的中的游戏视频
#     #  增加 游戏中心入口字段（game_entrances）
#     #  子频道轮播图模块中的游戏类型会增加 game_download_button_name 和 game_details_button_name 字段，
#     #     这两个字段分别表示：游戏下载按钮名 和 游戏详情按钮名；如果按钮名称为空，说明该按钮不应该出现
#     {
#         "new": "http://localhost:10000/interface/android_v3/sub_channel_details?sub_channel_id=1&show_game_information=1&ver=4.2"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/sub_channel_details?sub_channel_id=349&show_game_information=1&ver=4.2"
#     },
#
#
#     ######## 频道导航
#     #android
#     {
#         "new": "http://localhost:10000/interface/android_v3/navigations.json"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/navigations.json"
#     },
#
#
#     ######## 频道内容/VideoList内容
#     #android # 只显示免费视频。
#     {
#         "new": "http://localhost:10000/interface/android_v3/channel_contents.json?channel_id=5&pid=aabbcc"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/channel_contents.json?channel_id=901&pid=aabbcc"
#     },
#     #android >= v3.4 # ver >= 3.4 时： 会显示付费视频  和 免费视频 ; ver < v3.4 # 只显示免费视频。
#     {
#         "new": "http://localhost:10000/interface/android_v3/channel_contents.json?channel_id=901&pid=aabbcc&ver=3.4"
#         ,
#         "old": "http://cms.m.youku.com/interface/android_v3/channel_contents.json?channel_id=901&pid=aabbcc&ver=3.4"
#     },
    #品牌官网
    # {
    #     "new": "http://localhost:10000/interface/marketing/brands?platform=android&device_type=phone&sub_channel_id=335"
    #     ,
    #     "old": "http://cms.m.youku.com/interface/marketing/brands?platform=android&device_type=phone&sub_channel_id=335"
    # },

    # # winphone首页 checked
    # {
    #     "new": "http://localhost:10000/interface/windows_phone/index_page?ver=3.3",
    #     "old": "http://cms-test.m.youku.com/interface/windows_phone/index_page?ver=3.3"
    # },
    # {
    #     "new": "http://localhost:10000/interface/windows_phone/index_page?ver=1.0",
    #     "old": "http://cms-test.m.youku.com/interface/windows_phone/index_page?ver=1.0"
    # },
    # # winphone频道页 checked
    # {
    #     "new": "http://localhost:10000/interface/windows_phone/channels_page?channel_id=85",
    #     "old": "http://cms-test.m.youku.com/interface/windows_phone/channels_page?channel_id=85"
    # },
    # # winphone子频道页 checked
    # {
    #     "new": "http://localhost:10000/interface/windows_phone/sub_channels?channel_id=96",
    #     "old": "http://cms-test.m.youku.com/interface/windows_phone/sub_channels?channel_id=96"
    # },
    # # winpad首页 checked
    # {
    #     "new": "http://localhost:10000/interface/windows_pad/index_page",
    #     "old": "http://cms-test.m.youku.com/interface/windows_pad/index_page"
    # },
    # # winphone8.1首页 checked
    # {
    #     "new": "http://localhost:10000/interface/wp8/index_page",
    #     "old": "http://cms-test.m.youku.com/interface/wp8/index_page"
    # },
    #android4.2+搜索背景图
    {
         "new": "http://localhost:10000/interface/android_v3/search_background_videos",
         "old": "http://cms-test.m.youku.com:6897/interface/android_v3/search_background_videos"
    }
]
