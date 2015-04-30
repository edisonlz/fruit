#coding=utf-8

from base import BaseApi
from show import ShowApi
from util import encodevid
import settings

class VideoApi(BaseApi):
    """
    读取视频API
    """
    FD = [
        'videoid', 'title', 'thumburl',
        'thumburl_v2', 'desc', 'deschead',
        'seconds', 'total_vv', 'state', 'device_limit',
        'isoriginal', 'copyright_status', 'show_id', 'show_videotype',
        'show_videoseq', 'userid', 'username', 'publishtime',
    ]
    fd = ' '.join(FD)

    HOST = settings.SHOW_HOST

    @classmethod
    def get_video_info(cls, video_id, fd=None, **kwargs):
        """
        :param str video_id: youku video id
        :param str fd: field description default cls.fd
        :param dict kwargs: params
        :raises ValueError: if the video_id is None
        :return wiki: http://wiki.1verge.net/webdev:ds:video#show_节目视频
        get video info api code sample::
            VideoApi.get_video_info("xasdtmmdx12")
        """
        if not fd:
            fd = cls.fd
        path='/video'
        ft='json'
        q = {}
        q.update({'videoid': video_id})
        q.update(kwargs)
        q_str = ' '.join(["{k}:{v}".format(k=k, v=v) for k, v in q.iteritems()])
        params = {"ft": ft, "q": q_str, "fd": fd}
        headers = {'X-Forwarded-For': kwargs.get("ip")}
        info = cls.get_json(cls.HOST, path, params, headers)
        if info.get('results') is False:
                return {}

        video_info = info.get('results', [{},])[0]
        show_id = video_info.get('show_id', '')
        # add show fields
        if show_id:
            show_info = ShowApi.get_show_info(show_id)
            video_info['showname'] = show_info.get('showname', '')
            video_info['showid'] = show_info.get('showid', '')
            video_info['paid'] = show_info.get('paid', 0)
            video_info['pay_type'] = show_info.get('pay_type', [])
        return  video_info

if __name__ == '__main__':
    print VideoApi.get_video_info('XNzg1MjI4ODA0')
    ret = VideoApi.get_video_info('XNzg1MjI4ODA0')
    import json
    print json.dumps(ret, ensure_ascii=False, sort_keys=True, indent=4)
    # print json.dumps(ret, ensure_ascii=False, sort_keys=True, indent=4)