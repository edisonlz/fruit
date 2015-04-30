# coding=utf-8
import os, sys
import random


PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "site-packages"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "..", ".."))

Menus = [
    {
        "id": "ipad_content",
        "name": "iPad内容管理",
        "children": [
            {
                "id": "preview",
                "name": "预览",
                "path": "/content/ipad/preview",
                "is_link": True,
                # "target":"_blank",
            },
            {
                "id": "home_admin",
                "name": "首页管理",
                "path": "/content/ipad/main_page/modules",  # 默认显示子菜单
                "children": [
                    {
                        "id": "mod_admin",
                        "name": "模块管理",
                        "path": "/content/ipad/main_page/modules",
                    },
                    {
                        "id": "video_admin",
                        "name": "视频管理",
                        "path": "/content/ipad/main_page/videos",
                    },

                ]
            },
            {
                "id": "channel_page_admin",
                "name": "频道页管理",
                "path": "/content/ipad/new_channels",
                "children": [
                    {
                        "id": "channel_admin",
                        "name": "频道管理",
                        "path": "/content/ipad/new_channels",
                    },

                    # {
                    # "id": "subchannel_admin",
                    #     "name": "子频道标签",
                    #     "path": "/content/ipad/channel/subchannels",
                    # },
                    # {
                    #     "id": "subchannel_module_admin",
                    #     "name": "子频道模块",
                    #     "path": "/content/ipad/subchannel/modules",
                    # },
                    # {
                    #     "id": "subchannel_item_admin",
                    #     "name": "子频道视频",
                    #     "path": "/content/ipad/subchannel/module/items",
                    # },
                    # {
                    # "id": "jinpage_module_admin",
                    #     "name": "精选页模块管理",
                    #     "path": "/content/ipad/jinpage/modules",
                    # },
                    # {
                    #     "id": "jinpage_item_admin",
                    #     "name": "精选页视频管理",
                    #     "path": "/content/ipad/jinpage/module/items",
                    # },
                    # {
                    #     "id": "jinpage_seeditem_admin",
                    #     "name": "精选页种子视频管理",
                    #     "path": "/content/ipad/jinpage/seeditems",
                    # },
                    {
                        "id": "list_sync_plans",
                        "name": "同步任务",
                        "path": "/content/ipad/sync/module/items",
                    }
                ]
            },
        ]
    },
    {
        "id": "iphone_content",
        "name": "iPhone内容管理",
        "children": [
            {
                "id": "preview",
                "name": "预览",
                "path": "/content/iphone/preview",
                "is_link": True,
                # "target":"_blank",
            },
            {
                "id": "home_admin",
                "name": "首页管理",
                "path": "/content/iphone/main_page/modules",
                "children": [
                    {
                        "id": "mod_admin",
                        "name": "模块管理",
                        "path": "/content/iphone/main_page/modules",
                    },
                    {
                        "id": "video_admin",
                        "name": "视频管理",
                        "path": "/content/iphone/main_page/videos",
                    },

                ]
            },
            {
                "id": "channel_page_admin",
                "name": "频道页管理",
                "path": "/content/iphone/new_channels",
                "children": [
                    {
                        "id": "channel_admin",
                        "name": "频道管理",
                        "path": "/content/iphone/new_channels",
                    },

                    {
                        "id": "subchannel_admin",
                        "name": "子频道标签",
                        "path": "/content/iphone/channel/subchannels",
                    },
                    # {
                    # "id": "subchannel_module_admin",
                    # "name": "子频道模块管理",
                    #     "path": "/content/iphone/subchannel/modules",
                    # },
                    # {
                    #     "id": "subchannel_module_admin",
                    #     "name": "v4.x子频道模块管理",
                    #     "path": "/content/iphone/subchannel/modules_v4",
                    # },
                    #
                    # {
                    #     "id": "subchannel_item_admin",
                    #     "name": "v4.x子频道视频管理",
                    #     "path": "/content/iphone/subchannel/module_v4/items",
                    # },
                    # {
                    #     "id": "subchannel_module_admin",
                    #     "name": "v3.x子频道模块管理",
                    #     "path": "/content/iphone/subchannel/modules",
                    # },
                    #
                    # {
                    #     "id": "subchannel_item_admin",
                    #     "name": "v3.x子频道视频管理",
                    #     "path": "/content/iphone/subchannel/module/items",
                    # },

                    # {
                    #     "id": "subchannel_item_admin",
                    #     "name": "子频道视频管理",
                    #     "path": "/content/iphone/subchannel/module/items",
                    # },
                ]
            },
        ]
    },
    {
        "id": "android_content",
        "name": "Android内容管理",
        "children": [
            {
                "id": "preview",
                "name": "预览",
                "path": "/content/android/preview",
                "is_link": True,
                # "target":"_blank",
            },
            {
                "id": "home_admin",
                "name": "首页管理",
                "path": "/content/android/main_page/modules",
                "children": [
                    {
                        "id": "mod_admin",
                        "name": "模块管理",
                        "path": "/content/android/main_page/modules",
                    },
                    {
                        "id": "video_admin",
                        "name": "视频管理",
                        "path": "/content/android/main_page/videos",
                    },

                ]
            },
            {
                "id": "channel_page_admin",
                "name": "频道页管理",
                "path": "/content/android/new_channels",
                "children": [
                    {
                        "id": "channel_admin",
                        "name": "频道管理",
                        "path": "/content/android/new_channels",
                    },

                    {
                        "id": "subchannel_admin",
                        "name": "子频道标签管理",
                        "path": "/content/android/channel/subchannels",
                    },
                    {
                        "id": "subchannel_module_admin",
                        "name": "子频道模块管理",
                        "path": "/content/android/subchannel/modules",
                    },

                    {
                        "id": "subchannel_item_admin",
                        "name": "子频道视频管理",
                        "path": "/content/android/subchannel/module/items",
                    },
                ]
            },
        ]
    },
    {
        "id": "win_phone_content",
        "name": "WinPhone内容管理",
        "children": [
            {
                "id": "preview",
                "name": "预览",
                "path": "/content/win_phone/preview",
                "is_link": True,
                # "target":"_blank",
            },
            {
                "id": "home_admin",
                "name": "首页管理",
                "path": "/content/win_phone/main_page/modules",
                "children": [
                    {
                        "id": "mod_admin",
                        "name": "模块管理",
                        "path": "/content/win_phone/main_page/modules",
                    },
                    {
                        "id": "video_admin",
                        "name": "视频管理",
                        "path": "/content/win_phone/main_page/videos",
                    },

                ]
            },
            {
                "id": "channel_page_admin",
                "name": "频道页管理",
                "path": "/content/win_phone/channels",
                "children": [
                    {
                        "id": "channel_admin",
                        "name": "频道管理",
                        "path": "/content/win_phone/channels",
                    },

                    {
                        "id": "subchannel_admin",
                        "name": "子频道标签管理",
                        "path": "/content/win_phone/channel/subchannels",
                    },
                    {
                        "id": "subchannel_module_admin",
                        "name": "子频道模块管理",
                        "path": "/content/win_phone/subchannel/modules",
                    },

                    {
                        "id": "subchannel_item_admin",
                        "name": "子频道视频管理",
                        "path": "/content/win_phone/subchannel/module/items",
                    },
                ]
            },
        ]
    },
    {
        "id": "common_content",
        "name": "公共模块",
        "path": "/content/common_content/boxes",
    }

]

FRESH_MENU = [
    {"id": "home_management",
     "img_class": "icon-home",
     "name": u"首页管理",
     "children": [
         {
             "id": "main_page_module_admin",
             "name": u"推荐池",
             "path": "/content/common_content/boxes",
             "level": 1,
             "img_class": 'icon-chevron-right',
             "path_candidates": [
                 "/content/common_content/current_box_page/(\d+)/box/(\d+)/videos",
                 "/content/common_content/current_box_page/(\d+)/box/(\d+)/video/(\d+)/update_video",
             ]
         },
         {
             "id": "main_page_content_admin",
             "name": u"平台管理",
             "path": "/content/iphone/main_page/uniq_modules",
             "img_class": "icon-th-list",
             "children": [
                 {
                     "id": "main_page_content_admin",
                     "name": u"iPhone",
                     "path": "/content/iphone/main_page/uniq_modules",
                     "path_candidates": [
                         "/content/iphone/main_page/preview",
                         "/content/iphone/main_page/videos",
                         "/content/iphone/main_page/add/video",
                         '/content/iphone/main_page/update/video',
                         "/content/iphone/main_page/query/module/(\d+)",
                     ],
                 },
                 {
                     "id": "main_page_content_admin",
                     "name": u"iPad",
                     "path": "/content/ipad/main_page/uniq_modules",
                     "path_candidates": [
                         "/content/ipad/main_page/preview",
                         '/content/ipad/main_page/videos',
                         "/content/ipad/main_page/add/video",
                         '/content/ipad/main_page/update/video',
                         "/content/ipad/main_page/query/module/(\d+)",
                     ],
                 },
                 {
                     "id": "main_page_content_admin",
                     "name": u"Android",
                     "path": "/content/android/main_page/uniq_modules",
                     "path_candidates": [
                         "/content/android/main_page/preview",
                         '/content/android/main_page/videos',
                         "/content/android/main_page/add/video",
                         '/content/android/main_page/update/video',
                         "/content/android/main_page/query/module/(\d+)",
                     ],
                 },
                 # {
                 # "id": "main_page_content_admin",
                 #     "name": u"winPhone",
                 #     "path": "/content/win_phone/main_page/uniq_modules",
                 #     "path_candidates": ["/content/win_phone/main_page/preview"],
                 # },
             ]
         },
     ]
    },
    {
        "id": "Channel",
        "name": u"频道管理",
        "img_class": "icon-tablet",
        "children": [

            {
                "id": "iphone_channel_admin",
                "name": u"iPhone频道",
                "path": "#",
                "level": 1,
                "img_class": "icon-th-list",
                "children": [
                    # {
                    # "id": "iphone_channel_navi",
                    #     "name": u"频道导航",
                    #     "path": "#",
                    # },
                    # {
                    # "id": "iphone_channel_admin",
                    #     "name": u"频道管理",
                    #     "path": "/content/iphone/new_channels"
                    # },
                    {
                        "id": "channel_admin",
                        "name": "频道管理",
                        "path": "/content/iphone/new_channels",
                        "path_candidates": [
                            "/content/iphone/query/new_channel/(\d+)",
                            "/content/iphone/channel/subchannels",
                            "/content/iphone/query/subchannel",
                            "/content/iphone/subchannel/modules",
                            "/content/iphone/query/subchannel/module",
                            "/content/iphone/add/subchannel/module/item",
                            "/content/iphone/query/subchannel/module/item",
                            "/content/iphone/subchannel/module/items",
                            "/content/iphone/fixed_position_videos",
                            "/content/iphone/add/fixed_position_video",
                            "/content/iphone/query/fixed_position_video",
                            "/content/iphone/ranking",
                        ]
                    },

                    # {
                    #     "id": "subchannel_admin",
                    #     "name": "子频道标签管理",
                    #     "path": "/content/iphone/channel/subchannels",
                    # },
                    # {
                    #     "id": "subchannel_module_admin",
                    #     "name": "子频道模块管理",
                    #     "path": "/content/iphone/subchannel/modules",
                    # },
                    # {
                    #     "id": "subchannel_module_admin",
                    #     "name": "v4.x子频道模块管理",
                    #     "path": "/content/iphone/subchannel/modules_v4",
                    # },
                    #
                    # {
                    #     "id": "subchannel_item_admin",
                    #     "name": "v4.x子频道视频管理",
                    #     "path": "/content/iphone/subchannel/module_v4/items",
                    # },
                    # {
                    #     "id": "subchannel_module_admin",
                    #     "name": "v3.x子频道模块管理",
                    #     "path": "/content/iphone/subchannel/modules",
                    # },
                    #
                    # {
                    #     "id": "subchannel_item_admin",
                    #     "name": "v3.x子频道视频管理",
                    #     "path": "/content/iphone/subchannel/module/items",
                    # },

                ]
            },
            {
                "id": "ipad_channel_admin",
                "name": u"iPad频道",
                "path": "#",
                "level": 1,
                "img_class": "icon-th-list",
                "children": [
                    # {
                    # "id": "ipad_channel_navi",
                    #     "name": u"频道导航",
                    #     "path": "#",
                    # },
                    # {
                    # "id": "ipad_channel_admin",
                    #     "name": u"频道管理",
                    #     "path": "/content/ipad/new_channels"
                    # },
                    {
                        "id": "channel_admin",
                        "name": "频道管理",
                        "path": "/content/ipad/new_channels",
                        "path_candidates": [
                            "/content/ipad/query/new_channel/(\d+)",
                            "/content/ipad/channel/subchannels",
                            "/content/ipad/query/subchannel",
                            "/content/ipad/subchannel/modules",
                            "/content/ipad/query/subchannel/module",
                            "/content/ipad/add/subchannel/module/item",
                            "/content/ipad/query/subchannel/module/item",
                            "/content/ipad/subchannel/module/items",
                            "/content/ipad/fixed_position_videos",
                            "/content/ipad/add/fixed_position_video",
                            "/content/ipad/query/fixed_position_video",
                            "/content/ipad/ranking",
                        ]
                    },

                    # {
                    #     "id": "subchannel_admin",
                    #     "name": "子频道标签管理",
                    #     "path": "/content/ipad/channel/subchannels",
                    # },
                    # {
                    #     "id": "subchannel_module_admin",
                    #     "name": "子频道模块管理",
                    #     "path": "/content/ipad/subchannel/modules",
                    # },
                    # {
                    #     "id": "subchannel_item_admin",
                    #     "name": "子频道视频管理",
                    #     "path": "/content/ipad/subchannel/module/items",
                    # },
                ]
            },
            {
                "id": "android_channel_admin",
                "name": u"Android频道",
                "path": "#",
                "level": 1,
                "img_class": "icon-th-list",
                "children": [
                    {
                        "id": "channel_navigation",
                        "name": u"频道导航",
                        "path": "/content/android/channel_navigation",
                        "path_candidates": [
                            "/content/android/update_channel_navigation/(\d+)",
                        ]
                    },
                    # {
                    # "id": "android_channel_admin",
                    # "name": u"频道管理",
                    #     "path": "/content/android/new_channels"
                    # },
                    {
                        "id": "channel_admin",
                        "name": "频道管理",
                        "path": "/content/android/new_channels",
                        "path_candidates": [
                            "/content/android/query/new_channel/(\d+)",
                            "/content/android/channel/subchannels",
                            "/content/android/query/subchannel",
                            "/content/android/subchannel/modules",
                            "/content/android/query/subchannel/module",
                            "/content/android/add/subchannel/module/item",
                            "/content/android/query/subchannel/module/item",
                            "/content/android/subchannel/module/items",
                            "/content/android/fixed_position_videos",
                            "/content/android/add/fixed_position_video",
                            "/content/android/query/fixed_position_video",
                            "/content/android/ranking",
                        ]
                    },

                    # {
                    #     "id": "subchannel_admin",
                    #     "name": "子频道标签管理",
                    #     "path": "/content/android/channel/subchannels",
                    # },
                    # {
                    #     "id": "subchannel_module_admin",
                    #     "name": "子频道模块管理",
                    #     "path": "/content/android/subchannel/modules",
                    # },
                    #
                    # {
                    #     "id": "subchannel_item_admin",
                    #     "name": "子频道视频管理",
                    #     "path": "/content/android/subchannel/module/items",
                    # },
                    {
                        "id": "android_video_list",
                        "name": u"专题管理",
                        "path": "/content/android/video_lists",
                        "path_candidates": [
                            "/content/android/query/video_list/(\d+)",
                            "/content/android/video_list/(\d+)/videos",
                            "/content/android/video_list/(\d+)/query_video/(\d+)",
                        ]
                    },
                ]
            },
            {
                "id": "brand_official_website_admin",
                "name": u"品牌官网",
                "path": "#",
                "level": 1,
                "img_class": "icon-th-list",
                "hidden_for_normal_user": False,
                "children": [
                    {
                        "id": "brand_module_admin",
                        "name": "频道投放管理",
                        "path": "/content/brand/brand_modules",
                        "path_candidates": [
                            "/content/brand/brand_module/update_module/(\d+)",
                            "/content/brand/brand_videos",
                            "/content/brand/brand_video/add_video",
                            "/content/brand/brand_video/update_video/(\d+)",
                        ]
                    },
                ]
            },
            {
                "id": "virtual_name_and_fetch_plan",
                "name": u"抓取管理",
                "path": "#",
                "level": 1,
                "img_class": "icon-th-list",
                "hidden_for_normal_user": True,
                "children": [
                    {
                        "id": "virtual_names",
                        "name": u"虚名称列表",
                        "path": "/content/sync/virtual_names",
                    },
                    {
                        "id": "fetch_plans",
                        "name": u"抓取计划",
                        "path": "/content/sync/select_plans",
                        "path_candidates": [
                            "/content/sync/update/plan/(\d+)",
                        ]
                    }
                ]
            },
        ]
    },
    {
        "id": "background_image_management",
        "name": u"背景图管理",
        "hidden_for_normal_user": True,
        "img_class": "icon-desktop",
        "children": [
            {
                "id": "client_start_images",
                "name": u"开机启动图",
                "path": "/content/entrance/client_start_images",
                "path_candidates": ["/content/entrance/client_start_images"],
                "level": 1,
                "img_class": 'icon-chevron-right',
                "children": [],
            },
            {
                "id": "vip_goods_page_back_image",
                "name": u"会员商品页背景图",
                "path": "/content/vip_goods_page/back_img",
                "level": 1,
                "img_class": 'icon-chevron-right',
                "children": [],
            },
            {
                "id": "search_back_image",
                "name": u"Android搜索背景图",
                "path": "/content/search/back_img",
                "level": 1,
                "img_class": 'icon-chevron-right',
                "children": [],
            },
        ]
    },
    {
        "id": "system_management",
        "name": u"系统管理",
        "img_class": "icon-desktop",
        "children": [
            {
                "id": "action_log_management",
                "name": u"操作日志管理",
                "path": "/content/user_action/logs",
                "level": 1,
                "img_class": 'icon-chevron-right',
                "children": [],
            },
            {
                "id": "cid_management",
                "name": u"Cid管理",
                "path": "/content/cids",
                "hidden_for_normal_user": True,
                "level": 1,
                "img_class": 'icon-chevron-right',
                "children": [],
            },
            # {
            # "id": "version_management",
            #     "name": u"版本管理",
            #     "path": "/content/versions",
            #     "level": 1,
            #     "img_class": 'icon-chevron-right',
            #     "children": [],
            #     },
        ]
    }
]

Channel_menu_hash = {
    "id": "Channel",
    "name": "频道页管理",
    "has_img": True,
    "img_url": "images/channel.png",
    "children": [
        {
            "id": "android_channel_admin",
            "name": "Android频道",
            "path": "#",
            "children": [
                {
                    "id": "android_channel_navi",
                    "name": "频道导航",
                    "path": "#",
                },
                {
                    "id": "android_channel_admin",
                    "name": "频道管理",
                    "path": "/content/android/new_channels"
                },
                {
                    "id": "android_video_list",
                    "name": "VL管理",
                    "path": "/content/android/video_lists"
                },
            ]
        },
        {
            "id": "iphone_channel_admin",
            "name": "Iphone频道",
            "path": "#",
            "children": [
                {
                    "id": "iphone_channel_navi",
                    "name": "频道导航",
                    "path": "#",
                },
                {
                    "id": "iphone_channel_admin",
                    "name": "频道管理",
                    "path": "/content/iphone/new_channels"
                }
            ]
        },
        {
            "id": "ipad_channel_admin",
            "name": "Ipad频道",
            "path": "#",
            "children": [
                {
                    "id": "ipad_channel_navi",
                    "name": "频道导航",
                    "path": "#",
                },
                {
                    "id": "ipad_channel_admin",
                    "name": "频道管理",
                    "path": "/content/ipad/new_channels"
                }
            ]
        },
    ]
}

New_Menus = {
    "iphone": [
        {
            "id": "Main_Page",
            "name": "首页管理",
            "has_img": True,
            "img_url": "images/main_page.png",
            "children": [
                {
                    "id": "main_page_module_admin",
                    "name": "模板管理",
                    "path": "/content/common_content/boxes",
                },
                {
                    "id": "main_page_content_admin",
                    "name": "内容管理",
                    "path": "/content/iphone/main_page/uniq_modules",
                },
            ]
        },
        Channel_menu_hash
    ],
    "android": [
        {
            "id": "Main_Page",
            "name": "首页管理",
            "has_img": True,
            "img_url": "images/main_page.png",
            "children": [
                {
                    "id": "main_page_module_admin",
                    "name": "模板管理",
                    "path": "/content/common_content/boxes",
                },
                {
                    "id": "main_page_content_admin",
                    "name": "内容管理",
                    "path": "/content/android/main_page/uniq_modules",
                },
            ]
        }, Channel_menu_hash
    ],
    "ipad": [
        {
            "id": "Main_Page",
            "name": "首页管理",
            "has_img": True,
            "img_url": "images/main_page.png",
            "children": [
                {
                    "id": "main_page_module_admin",
                    "name": "模板管理",
                    "path": "/content/common_content/boxes",
                },
                {
                    "id": "main_page_content_admin",
                    "name": "内容管理",
                    "path": "/content/ipad/main_page/uniq_modules",
                },
            ]
        },
        Channel_menu_hash

    ],
    "win_phone": [
        {
            "id": "Main_Page",
            "name": "首页管理",
            "has_img": True,
            "img_url": "images/main_page.png",
            "children": [
                {
                    "id": "main_page_module_admin",
                    "name": "模板管理",
                    "path": "/content/common_content/boxes",
                },
                {
                    "id": "main_page_content_admin",
                    "name": "内容管理",
                    "path": "/content/win_phone/main_page/uniq_modules",
                },
            ]
        },
        Channel_menu_hash
    ]

}


