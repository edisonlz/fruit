#coding=utf-8
from django.db import models
from platform import Platform, Status
from wi_cache.base import CachingManager


class AndroidGame(models.Model):
    objects = CachingManager()
    name = models.CharField(max_length=100, default=u'', blank=True)
    description = models.TextField(verbose_name=u'描述', default='', blank=True)
    package_name = models.CharField(max_length=100, verbose_name=u'包名', default='', blank=True)
    logo = models.CharField(max_length=255, verbose_name=u'logo', default='', blank=True)
    version_code = models.CharField(max_length=100, verbose_name=u'version code', default='', blank=True)
    version_name = models.CharField(max_length=100, verbose_name=u'version name', default='', blank=True)
    url = models.CharField(max_length=255, verbose_name=u'下载url', default='', blank=True)
    category_name = models.CharField(max_length=100, verbose_name=u'分类名', default='', blank=True)
    download_count = models.CharField(max_length=100, verbose_name=u'下载数', default='', blank=True)
    original_game_id = models.IntegerField(verbose_name=u'游戏id', default=0, db_index=True)
    size = models.CharField(max_length=100, verbose_name=u'apk大小', default='', blank=True)
    score = models.CharField(max_length=100, verbose_name=u'评分', default='', blank=True)
    tags = models.CharField(max_length=255, verbose_name=u'游戏tags', default='', blank=True)
    type_name = models.CharField(max_length=100, verbose_name=u'app.type.chinese_name', default='', blank=True)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    # 创建游戏，如果已存在即更新游戏
    @classmethod
    def create_or_update(cls, params, game_id_field='original_game_id'):
        original_game_id = params.get(game_id_field)
        if original_game_id:
            try:
                game = cls.objects.get(original_game_id=original_game_id)
            except cls.DoesNotExist:
                game = cls()

            game.original_game_id = original_game_id
            game.name = params.get("game_name", '')
            game.version_code = params.get("game_version_code", '')
            game.version_name = params.get("game_version_name", '')
            game.description = params.get("game_description", '')
            game.package_name = params.get("game_apk_package", '')
            game.logo = params.get("game_logo", '')
            game.url = params.get("game_url", '')
            game.score = params.get("game_score", '')
            game.category_name = params.get("game_category_name", '')
            game.download_count = params.get("game_download_count", '')
            game.size = params.get("game_size", '')
            game.is_delete = False
            game.save()
            return game
        else:
            return None

    class Meta:
        verbose_name = u"Android游戏"
        verbose_name_plural = verbose_name
        app_label = "content"


class IosGame(models.Model):
    objects = CachingManager()
    scroller = models.CharField(max_length=255, verbose_name=u'游戏滚动图(大图)', default=u'', blank=True)
    logo = models.CharField(max_length=255, verbose_name=u'logo', default='', blank=True)
    itunesid = models.CharField(max_length=255, verbose_name=u'游戏对应的itunes的id', default='', blank=True)
    categories = models.CharField(max_length=255, verbose_name=u'游戏分类', default='', blank=True)
    desc = models.TextField(verbose_name=u'应用简介', default='')
    upload_time = models.CharField(max_length=255, verbose_name=u'游戏上架时间', default='', blank=True)
    score = models.CharField(max_length=255, verbose_name=u'评分', default='', blank=True)
    appname = models.CharField(max_length=255, verbose_name=u'游戏的app名称', default='', blank=True)
    url = models.CharField(max_length=255, verbose_name=u'下载url', default='', blank=True)
    original_game_id = models.IntegerField(verbose_name=u'游戏id', default=0, db_index=True)
    version = models.CharField(max_length=255, verbose_name=u'版本', default='', blank=True)
    size = models.CharField(max_length=255, verbose_name=u'大小', default='', blank=True)
    charge = models.CharField(max_length=255, verbose_name=u'收费类型', default='', blank=True)
    redirect_type = models.CharField(max_length=255, verbose_name=u'推荐类型', default='', blank=True)
    redirect_url = models.CharField(max_length=255, verbose_name=u'跳转类型', default='', blank=True)
    recommend_type = models.CharField(max_length=255, verbose_name=u'外链URL', default='', blank=True)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    class Meta:
        verbose_name = u"Ios游戏"
        verbose_name_plural = verbose_name
        app_label = "content"

    # 创建游戏，如果已存在即更新游戏
    @classmethod
    def create_or_update(cls, params, game_id_field='original_game_id'):
        original_game_id = params.get(game_id_field)
        if original_game_id:
            try:
                game = cls.objects.get(original_game_id=original_game_id)
            except cls.DoesNotExist:
                game = cls()
            game.original_game_id = original_game_id
            game.appname = params.get("game_appname", '')
            game.version = params.get("game_version", '')
            game.itunesid = params.get("game_itunesid", '')
            game.logo = params.get("game_logo", '')
            game.scroller = params.get("game_scroller", '')
            game.score = params.get("game_score", '')
            game.url = params.get("game_url", '')
            game.desc = params.get("game_desc", '')
            game.upload_time = params.get("game_upload_time", '')
            game.size = params.get("game_size", '')
            game.charge = params.get("game_charge", '')
            game.redirect_type = params.get("game_redirect_type", '')
            game.redirect_url = params.get("game_redirect_url", '')
            game.recommend_type = params.get("game_recommend_type", '')
            game.is_delete = False
            game.save()
            return game
        else:
            return None

    # deprecated method, please change to create_or_update
    @classmethod
    def create_or_update_ios_game(cls, *args, **kwargs):
        http_post = kwargs.get('http_post', '')
        args_dict = http_post if http_post else kwargs  # 兼容可以直接传HTTP POST对象
        original_game_id = args_dict.get('game_id', '')
        if original_game_id:
            # 游戏已存在就更新游戏，否则新建游戏
            try:
                game = cls.objects.get(original_game_id=original_game_id)
            except cls.DoesNotExist:
                game = cls()
            game.original_game_id = original_game_id
            game.logo = args_dict.get('logo', '')
            game.scroller = args_dict.get('scroll', '')
            game.itunesid = args_dict.get('itunes_id', '')
            game.categories = args_dict.get('categories', '')
            game.upload_time = args_dict.get('upload_time', '')
            game.score = args_dict.get('score', '')
            game.appname = args_dict.get('game_name', '')
            game.url = args_dict.get('url', '')
            game.version = args_dict.get('game_version', '')
            game.size = args_dict.get('size', '')
            game.charge = args_dict.get('charge_type', '')
            game.redirect_type = args_dict.get('redirect_type', '')
            game.redirect_url = args_dict.get('redirect_url', '')
            game.recommend_type = args_dict.get('recommend_type', '')
            game.desc = args_dict.get('desc', '')
            game.is_delete = True
            game.save()
            return game.id
        else:
            return None
