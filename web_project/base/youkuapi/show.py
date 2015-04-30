#coding=utf-8

from base import BaseApi
import settings

class ShowApi(BaseApi):

    """
    节目API
    """
    FD = ['showid', 'pk_odshow', 'showname', 'showsubtitle', 'deschead', 'showdesc', 'show_thumburl', 'show_vthumburl',
          'show_bannerurl', 'showlength', 'copyright_status', 'paid', 'pay_type', 'onlinetime', 'hasvideotype',
          'firstepisode_videoid', 'firstepisode_videotitle', 'firstepisode_videorctitle', 'firstepisode_thumburl',
          'firstepisode_thumburl_v2', 'lastepisode_videoid', 'lastepisode_videotitle', 'lastepisode_videorctitle',
          'lastepisode_thumburl', 'lastepisode_thumburl', 'showtotal_vv', 'device_disabled', 'trailer_videoid',
          'episode_last', 'episode_total']
    fd = ' '.join(FD)

    HOST = settings.SHOW_HOST
    FORMAT = "json"

    @classmethod
    def get_show_info(cls, show_id, fd=None, **kwargs):
        """
        :param str show_id: youku video id
        :param str fd: field description default cls.fd
        :param dict kwargs: params
        :raises ValueError: if the show_id is None
        :return wiki: http://wiki.1verge.net/webdev:ds:show
        get video info api code sample::
            ShowApi.get_show_info("xasdtmmdx12")
        """
        if not fd:
            fd = cls.fd
            
        path='/show'
        q = {}
        q.update({'showid': show_id})
        q.update(kwargs)
        q_str = ' '.join(["{k}:{v}".format(k=k, v=v) for k, v in q.iteritems()])
        params = {"ft": cls.FORMAT, "q": q_str, "fd": fd}
        
        headers = {'X-Forwarded-For': kwargs.get("ip")}
        info = cls.get_json(cls.HOST, path, params, headers)
        try:
            if info.get('results') is False:
                return {}
            else:
                return info.get('results', [{}, ])[0]
        except TypeError:
            print 'fetch error'
            print info


if __name__ == '__main__':
    print ShowApi.get_show_info('f108ae9e270811e2b356')
    ret =  ShowApi.get_show_info('188d6318525711e3b8b7')
    import json
    print json.dumps(ret, ensure_ascii=False, sort_keys=True, indent=4)
