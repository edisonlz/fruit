#coding=utf-8
from base import BaseApi
import settings
from util import decodevid
class UserApi(BaseApi):
    '''
    get user info
    '''

    HOST = settings.USER_HOST

    @classmethod
    def get_user_info(cls, user_id, **kwargs):
        '''
        :param str user_id: youku user id
        :param dict kwargs: params
        :raises ValueError: if user_id is None
        :return wiki: http://wiki.1verge.net/webdev:ds:video#show_节目视频
        '''
        uid = decodevid(user_id) # use decodevid as decodeuid
        path = '/users/show'
        params = {"uid": uid}
        headers = {'X-Forwarded-For': kwargs.get("ip")}
        info = cls.get_json(cls.HOST, path, params, headers)
        return info.get('user', [{},])

if __name__ == '__main__':
    # print UserApi.get_user_info(76835099)
    print UserApi.get_user_info('UNDAyMjMxNzM2')
