#coding=utf-8

from base import BaseApi
import settings

class PlaylistApi(BaseApi):

    """
    Get PlayList API
    """

    HOST = settings.OpenAPI_HOST
    client_id= settings.OpenAPIClientID


    @classmethod
    def get_playlist_info(cls, playlist_id ,count=1, **kwargs):
        """
        类方法

        :param str playlist_id: youku playlist id
        :param str fd: field description default cls.fd
        :param int count: limit select count
        :param dict kwargs: params
        :raises ValueError: if the playlist_id is None
        :return wiki: http://wiki.1verge.net/webdev:openapi:v2:playlists:videos?s[]=v2&s[]=playlists&s[]=videos&s[]=json
        get video info api code sample::
            PlaylistApi.get_playlist_info("18969513")

        """
        PATH = '/v2/playlists/videos.json'
        params = {"playlist_id": playlist_id, "count": count, "client_id": cls.client_id}
        headers = {'X-Forwarded-For': kwargs.get("ip")}
        info = cls.get_json(cls.HOST, PATH, params, headers)
        return info.get('videos', [{},])[0]

    
if __name__=='__main__':
    ret = PlaylistApi.get_playlist_info('18969513')
    print ret
    import json
    print json.dumps(ret, ensure_ascii=False, sort_keys=True, indent=4)
