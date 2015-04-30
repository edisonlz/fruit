#coding=utf-8

from django.db import models
from app.content.models import BaseVideo, AndroidBoxVideo
from app.content.models import HomeBox, BoxType, VideoType, AndroidGame, AndroidVideoListModule, AndroidHomeBoxTag
from wi_model_util.imodel import get_object_or_none

class IphoneHomePublishedVideo(BaseVideo):
    box_id = models.IntegerField(verbose_name='所属的盒子ID', default=0)
    live_broadcast_url = models.CharField(max_length=255, verbose_name='直播url', default='')
    live_broadcast_bg_image_3_5 = models.CharField(max_length=255, verbose_name='聊天背景图(3.5)', default='')
    live_broadcast_bg_image_4 = models.CharField(max_length=255, verbose_name='聊天背景图(4)', default='')
    live_broadcast_bg_image_4_7 = models.CharField(max_length=255, verbose_name='聊天背景图(4.7)', default='')
    live_broadcast_bg_image_5_5 = models.CharField(max_length=255, verbose_name='聊天背景图(5.5)', default='')

class AndroidHomePublishedVideo(BaseVideo):
    box_id = models.IntegerField(verbose_name='所属的盒子ID', default=0)
    video_list_id = models.IntegerField(verbose_name='VIDEO LIST ID', default=0)
    channel_id = models.IntegerField(verbose_name=u'编辑推荐的channel id', default=0) #好像没有用？
    pid = models.CharField(max_length=100, verbose_name='针对特定pid的视频', null=True, blank=True)

    def details_for_interface(self, params):
        if self.video_list_id:
            video_list_module_set = AndroidVideoListModule.objects.filter(id=self.video_list_id)[:1]
            if not video_list_module_set:
                return {}
            video_list_module = video_list_module_set.get()
            return {
                'content_type': VideoType.to_i('video_list'),#v4.4content_type 为 int类型
                'content_id': video_list_module.id,
                'title': self.title,
                'image': self.h_image,
                'intro': self.intro,
                'playlist_videoid': '',
                'url': '',
                'pv': 0,
                'image_size': 4,
                'second_title_in_front': self.subtitle,
                'second_title_in_back': ''
            }
        hash={
            'content_id': self.video_id,
            'content_type': self.video_type,
            'title': self.title,
            'image': self.h_image,
            'intro': self.intro,
            'url': self.url,
            'pv': self.first_episode_video_pv,
            'image_size': self.image_size,
            'paid': self.paid,
            'playlist_videoid': self.first_episode_video_id,
            'second_title_in_front': '',
            'second_title_in_back': ''
        }
        if VideoType.to_s(self.video_type) in ['game_list', 'game_download', 'game_details'] or self.attached_game_type:
            hash['game_information'] = self.game_information_hash(self.game_id)
            hash['content_type'] = self.video_type
            if self.type_of_game_without_video():
                hash['second_title_in_front'] = "安装"+str(self.game_download_count(self))
            if self.attached_game_type:
                hash['game_relation'] = 'attached'
            else:
                hash['game_relation'] = 'standalone'
        elif self.need_game_page_id():
            hash['game_page_id'] = self.game_page_id or ''
        if self.include_pgc_uid():
            hash['pgc_uid'] = self.pgc_uid

        return hash

    def include_pgc_uid(self):
        return self.video_type in [1, 2, 3] and not self.need_game_original_id()

    def need_game_original_id(self):
        return self.video_type in [7, 8, 9] or self.attached_game_type

    def need_game_page_id(self):
        return self.video_type in [ VideoType.to_i("game_gift"), VideoType.to_i("game_album"), VideoType.to_i("game_activity") ]

    def type_of_game_without_video(self):
        return self.video_type in [ VideoType.to_i("game_list"), VideoType.to_i("game_download"), VideoType.to_i("game_details") ]

    def game_download_count(self, content):
        try:
            download_count = AndroidGame.objects.get(content.game_id).download_count or 100
        except Exception,e:
            download_count = 100
        return download_count

    def api_columns(self, options):
        print '...api_columns.options: ', options

        columns = HomeBox.objects.filter(platform=1, is_delete=0, state=1).order_by('-position')

        if columns:
            columns = columns.exclude(box_type = BoxType.to_i('game'))
        if not options['show_slider']:
            columns = columns.exclude(box_type = BoxType.to_i('slider'))

        res_list = [self.column_and_videos_info_for_api(column, options) for column in columns]


        return {'results': res_list}

    def column_and_videos_info_for_api(self, column, options):
        if options['show_slider'] and column.box_type == BoxType.to_i('slider'):
            #contents = self.objects.filter(box_id=column.id, is_delete=0, state=1)
            contents = AndroidBoxVideo.objects.filter(box_id=column.id, is_delete=0, state=1)
            if not options['show_live_broadcast']:
                contents = contents.exclude(video_type=VideoType.to_i('live_broadcast'))
            if options['ver']<'4.4':
                contents = contents.exclude(video_type = VideoType.to_i('game_gift'))
            contents = contents.order_by('-position')[0:10]
            column_info = self.column_info_for_api(column)
            column_info['comments'] = '滚动图,只针对android3.5以上版本有效.用了它,请无视column_id=100中的第一个视频.'
            column_info['videos'] = [self._content_hash(content, 0, options) for content in contents]
        else:
            #unit_count = 1 if ((options['for_phone'] and column.is_phone_use_multiply_units == 1)) else 2
            unit_count = 2 if ((column.video_count_for_phone == 8 and column.video_count_for_pad == 8)) else 1
            column_info = self.column_info_for_api(column)
            column_info['units'] = self.unit_array([0]*unit_count, column, options)
        column_title_tag  = AndroidHomeBoxTag.objects.get(is_delete=False, box_id=column.id, tag_type='title')
        column_title_tag_info = column_title_tag.details_for_interface()
        if column_title_tag_info['type'] == 'jump_to_channel':
            cid = column_title_tag_info['cid']
            column_info.update({'cid': cid})

        return column_info


    def unit_array(self, units, column, options):
        array = []
        for i in range(len(units)):
            array.append({
                'unit_id': 0,
                'layout': self.unit_layout(column, i),
                'contents': self.api_contents(column, i, options)
            })
        return array

    def api_contents(self, column, i, options):
        under_slider_first_video_id = 0

        if column.box_type  == BoxType.to_i('under_slider'):
            under_slider_first_video_id = AndroidHomePublishedVideo.objects.filter(box_id=column.id).order_by('-position')[0].id

            first_cell_video_count = 1
            second_cell_video_count = 4
            if i == 0:
                contents = self.contents_limit_offset({'column_id':column.id, 'limit': first_cell_video_count, 'offset':0, 'origin_options':options})
            elif i == 1:
                contents = self.contents_limit_offset({'column_id':column.id, 'limit': second_cell_video_count, 'offset':1, 'origin_options':options})
        else:
            if i == 0:
                contents = self.contents_limit_offset({'column_id':column.id, 'limit': 4, 'offset':0, 'origin_options':options})
            elif i == 1:
                contents = self.contents_limit_offset({'column_id':column.id, 'limit': 4, 'offset':4, 'origin_options':options})

        result = [content._content_hash(content, under_slider_first_video_id, options) for content in contents]
        return result

    def contents_limit_offset(self, params_dict):
        column_id = params_dict['column_id']
        contents = AndroidHomePublishedVideo.objects.filter(is_delete=0, state=1, box_id=column_id)
        if not params_dict['origin_options']['show_game_information']:
            contents = contents.exclude(video_type = VideoType.to_i("game_list"))
            contents = contents.exclude(video_type = VideoType.to_i("game_download"))
            contents = contents.exclude(video_type = VideoType.to_i("game_details"))

        if not params_dict['origin_options']['show_live_broadcast']:
            contents = contents.exclude(video_type=VideoType.to_i("live_broadcast"))

        if params_dict['origin_options']['ver'] < '4.4':
            contents = contents.exclude(video_type = VideoType.to_i("game_gift"))


        contents = contents.order_by("-position")[params_dict['offset']:(params_dict['limit']+params_dict['offset'])]

        return contents


    def unit_layout(self, column, count):
        if column.box_type == BoxType.to_i('under_slider'):
            if count == 0:
                result = 1
            elif count == 1:
                result = 8
        else:
            result = 8
        return result


    def column_info_for_api(self,column):
        return {
            'column_id': column.box_id_for_android_api,
            'title': column.title,
            'cid': ''
        }


    def _content_hash(self, content, under_slider_first_video_id, options):

        if options['show_video_list'] and content.video_list_id:
            res = self.video_list_hash(content, options)
        else:
            res = self.video_hash(content, options)
        if content.id == under_slider_first_video_id and under_slider_first_video_id!=0:
            res['image_size'] = 1
        return res


    def video_list_hash(self, content, options):
        video_list_module = get_object_or_none(AndroidVideoListModule, id=content.video_list_id)
        if not video_list_module:
            return self.video_hash(content, options)
        return{
            'content_type': [str(VideoType.to_i('video_list'))],
            'content_id': [video_list_module.id],
            'title': [content.title],
            'image': [content.h_image],
            'intro': [content.intro],
            'playlist_videoid':'',
            'url':[''],
            'pv':0,
            'image_size': 4,
            'second_title_in_front': content.subtitle,
            'second_title_in_back': ''
        }

    def video_hash(self, content, options):

        video={
            'content_id': [content.video_id or ''],
            'content_type': [str(content.video_type or '')],
            'title': [content.title or ''],
            'image': [content.h_image or ''],
            'intro': [content.intro or ''],
            'url': [content.url or ''],
            # TODO: realize pv should
            'pv': [content.first_episode_video_pv or 0],
            'playlist_videoid': content.first_episode_video_id or '',
            'image_size': 4,
            'paid': content.paid,
            'second_title_in_front': content.subtitle,
            'second_title_in_back': '',
        }
        if content.video_type in [VideoType.to_i('game_list'), VideoType.to_i('game_download'), VideoType.to_i('game_details')]:
            video['game_information'] = self.game_information_hash(content.game_id)
            video['content_type'] = [str(self.content_type_compatible_with_previous_version(content, options))]
            video['second_title_in_front'] = '安装:' + str(self.game_download_count(content))


        return video

    def content_type_compatible_with_previous_version(self, content, options):
        if options['show_game_information']:
            return content.video_type
        else:
            #TODO: make sure what itis?
            return VideoType.to_i('game_list')

    def game_information_hash(self, game_app_id):
        try:
            game_app = AndroidGame.objects.get(id=game_app_id)
        except Exception,e:
            game_app = None
        if not game_app:
            return {}

        game_id = game_app.original_game_id
        game_type = self.game_type_for_interface()
        return {
            'game_type': game_type,
            'game_id': game_id,
            'game_name': game_app.name,
            'game_description': game_app.description,
            'game_package_name': game_app.package_name,
            'game_logo': game_app.logo,
            'game_version_code': game_app.version_code,
            'game_version_name': game_app.version_name,
            'game_url': game_app.url,
            'game_type_name': game_app.category_name,
            'game_class_name': game_app.category_name,
            'game_score': game_app.score or '0'

        }



    def game_type_for_interface(self):
        game_type = self.attached_game_type
        if game_type:
            if game_type == 'game_list':
                return 'show_list'
            elif game_type == 'game_download':
                return 'download_game'
            elif game_type == 'game_details':
                return 'show_details'
            else:
                return 'unknown'
        elif self.video_type in [7,8,9]:
            if self.video_type == 7:
                return 'show_list'
            elif self.video_type == 8:
                return 'download_game'
            elif self.video_type == 9:
                return 'show_details'
        else:
            return 'unknown'




class IpadHomePublishedVideo(BaseVideo):
    box_id = models.IntegerField(verbose_name='所属的盒子ID', default=0)
    pass

class WinPhonePublishedVideo(BaseVideo):
    box_id = models.IntegerField(verbose_name='所属的盒子ID', default=0)
    pass


