# coding=utf-8
from view.api_doc import handler_define, api_define, Param
from view.base import BaseHandler, CachedPlusHandler
from app.content.models import Ranking, Platform


class RankBase(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    @staticmethod
    def collect_rank(platform, **kwargs):
        ranks = Ranking.objects.filter(state=1, is_delete=0, platform=Platform.to_i(platform)).order_by('-position')
        if kwargs:
            ranks = ranks.filter(**kwargs)
        results = []
        for rank in ranks:
            results.append({
                'cid': rank.cid,
                'title': rank.title
            })
        return results


@handler_define
class IpadRank(RankBase):

    @api_define("iPad Rank", uri=r'/interface/ranking_list/lists_for_youku_ipad3', description="IPAD排行榜")
    def get(self):
        self.write({'results': self.collect_rank('ipad')})


@handler_define
class IphoneRank(RankBase):
    def get_cache_key(self):
        return {
            'ver': self.get_argument('ver', '3.2'),
        }

    @api_define("iPhone Rank", r'/interface/ranking_list/lists_for_youku_factor', [
        Param('ver', True, str, '3.2', '3.2', u'版本号'),
    ], description="IPHONE排行榜")
    def get(self):
        ver = self.get_argument('ver', '3.2')
        if float(ver) < 3.2:
            self.write({'results': self.collect_rank('iphone', ver_diff=1)})
        else:
            self.write({'results': self.collect_rank('iphone', ver_diff=0)})


@handler_define
class AndroidRank(RankBase):
    def get_cache_key(self):
        return {
            'client_type': self.get_argument('client_type', '0'),
        }

    @api_define("Android Rank", r'/interface/ranking_list/lists.json', [
        Param('client_type', True, str, '0', '0', u'版本号'),
    ], description="ANDROID排行榜")
    def get(self):
        client_type = self.get_argument('client_type', '0')
        if client_type == '0':
            self.write({'results': self.collect_rank('android')})
        elif client_type == '1':
            # 为1时取iphone3.2以下的结果
            self.write({'results': IphoneRank.collect_rank('iphone', ver_diff=1)})
        elif client_type == '100000':
            # fixed result
            self.write({'results': [
                {
                    "cid": "96",
                    "title": "电影"
                },
                {
                    "cid": "85",
                    "title": "综艺"
                },
                {
                    "cid": "97",
                    "title": "电视剧"
                }
            ]})
