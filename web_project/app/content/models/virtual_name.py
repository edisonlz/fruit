# coding: utf8
import urllib2
import socket
import json
from app.content.management.commands.lib.youku_cms import generate_time_stamp, CMS_API_SECRET
from hashlib import md5
from wi_cache import function_cache


class VirtualNameFetch(object):
    _appkey = 300
    _secret = CMS_API_SECRET
    _url = 'http://10.103.88.78/cms/api/outernames/multi_get.json' \
           '?page={page}&count={count}&appkey={appkey}&timestamp={timestamp}&sign={sign}'
    _v_name_list = []
    _update_time = generate_time_stamp()

    @function_cache(prefix="virtual_name:resa", expire_time=60 * 60)
    def get_virtual_name_res(self, page_num=1, page_video_count=2000):
        time_s = generate_time_stamp()
        url_params = {
            'page': page_num,
            'count': page_video_count,
            'appkey': self._appkey,
            'sign': self.generate_sign(time_s),
            'timestamp': time_s,
        }
        url = self._url.format(**url_params)
        res = self.open_link(url)
        return res

    def v_name_list(self):
        #now_t = generate_time_stamp()
        #if not self._v_name_list or now_t - self._update_time > 3600*24:  # 更新时间设为一天
        #    self._update_time = now_t
        #    self._v_name_list = self.collect_virtual_names()
        res = self.get_virtual_name_res()
        return res.get('data', [])

    # def collect_virtual_names(self):
    #     total = self.get_virtual_name_count()
    #     return self.get_all_virtual_names(total)
    #
    # def get_virtual_name_count(self):
    #     res = self.get_virtual_name_res()
    #     data = res.get('data', [])
    #     if data:
    #         return res['total']
    #
    # def get_all_virtual_names(self, total):
    #     page, page_size = 1, 100
    #     n_list = []
    #     while total > 0:
    #         res = self.get_virtual_name_res(page_num=page, page_video_count=page_size)
    #         data = res.get('data', [])
    #         if data:
    #             n_list += data
    #         page += 1
    #         total -= len(data)
    #     return n_list

    @staticmethod
    def open_link(url):
        retry, content = 0, None
        while retry < 2 and content is None:
            try:
                content = urllib2.urlopen(url).read()
            except socket.timeout:
                retry += 1
            except Exception, e:
                print e
        if content:
            return json.loads(content)
        else:
            return []

    def generate_sign(self, timestamp):
        sign = md5('{appkey}&{appsecret}&{timestamp}'.
                   format(appkey=self._appkey, appsecret=self._secret, timestamp=timestamp))
        return sign.hexdigest()


if __name__ == '__main__':
    a = VirtualNameFetch()
    name_list = VirtualNameFetch().v_name_list()
    resort_names = sorted(name_list, cmp=lambda x, y: cmp(x['id'], y['id']))
    print resort_names[0]
    print len(name_list)
    for piece in name_list:
        if u"搞笑" in piece['name']:
            print piece['name']
