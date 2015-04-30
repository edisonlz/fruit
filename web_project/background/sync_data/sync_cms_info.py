# coding: utf-8
from MySQLdb import connect
from pymongo import Connection
from bson import json_util
from random import randint
from datetime import datetime
import json
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

_DB_RUBY_MYSQL = dict(
    host='10.103.88.20',
    user='wireless-admin',
    passwd='1LytSCuf5tFZ',
    db='mos',
    charset='utf8'
)
_DB_RUBY_MONGO = dict(
    host='10.103.28.94',
    port=27037
)
_DB_ONLINE = dict(
    host="10.10.140.20",
    user='cms-user',
    passwd='cms-123',
    db='cms_development',
    charset='utf8',
)
_DB_LOCAL = dict(
    host='127.0.0.1',
    user='root',
    passwd='',
    db='cms_platform_new',
    # db='cms_platform',
    charset='utf8'
)


def get_connection(db):
    conn = connect(**db)
    return conn


def print_beauty(obj):
    beauty_str = json.dumps(obj, indent=4, default=json_util.default)
    print beauty_str


def del_old_videos_of_all_platform(conn):
    cur = conn.cursor()
    table_list = [
        'ipadsubchannelitem', 'ipadsubchannelmoduleitem', 'iphonesubchannelvideo', 'iphonesubchannelmodulevideo',
        'androidsubchannelvideo', 'androidsubchannelmodulevideo'
    ]
    for table in table_list:
        sql = "delete from %s" % ('content_' + table)
        cur.execute(sql)

    print '[INFO] delete all old videos finished!'


class FetchPlan(object):
    _conf = dict(
        host='10.103.28.94',
        port=27037
    )
    _user = 'fetCMS'
    _passwd = 'fdsee22'

    _cls_dict = {
        2: ('ipadsubchannel', 'ipadsubchannelmodule'),
        3: ('iphonesubchannel', 'iphonesubchannelmodule'),
        1: ('androidsubchannel', 'androidsubchannelmodule')
    }

    def __init__(self, py_conn):
        conn = Connection(**self._conf)
        db = conn.m_video_fetcher
        db.authenticate(self._user, self._passwd)
        self.db = db
        self.conn = py_conn

    @property
    def _cls_list(self):
        return [value for tup in self._cls_dict.values() for value in tup]

    def is_jump_plan(self, plan):
        flag = False
        if not plan['website_virtual_name'] or plan['website_virtual_name'].isspace():
            flag = True

        dest_cls = plan['cms_category_class'].lower()
        platform_context = {'ipad': 2, 'iphone': 3, 'android': 1}
        plat = None
        for k, v in platform_context.iteritems():
            if dest_cls.startswith(k) and dest_cls in self._cls_list:
                plat = v

        return flag, plat

    def work(self, delete=False):
        if delete:
            cur = self.conn.cursor()
            sql = "delete from content_syncjob"
            cur.execute(sql)

        self.get_old_plans_and_insert()
        print '[INFO] plans insert finish!'
    
    def get_old_plans_and_insert(self):
        accounts = self.db.plans.find()
        for item in accounts:
            jump_tag, plat = self.is_jump_plan(item)
            if not jump_tag and plat:
                tmp = {'platform': plat}
            else:
                continue

            dest_cls = item['cms_category_class'].lower()
            if 'module' in dest_cls:
                tmp['is_sub'] = False
            else:
                tmp['is_sub'] = True
            tmp['virtual_name'] = item['website_virtual_name'].encode('utf8')
            tmp['is_auto_published'] = True if item['is_auto_publish'] else False
            tmp['max_fetch_count'] = item.get('max_fetch_video_count') or 0
            tmp['category_name'] = item['cms_category_name']
            tmp['category_id'] = item['cms_category_id']
            tmp['is_delete'] = False
            tmp['state'] = 1
            tmp['runatonce'] = 0
            tmp['sha1_of_last_fetch'] = ''
            tmp['category_class'] = ''
            tmp.update(self.convert_schedule_to_new(item['schedule']))

            self.insert_single_plan(tmp)

    def insert_single_plan(self, plan):
        cur = self.conn.cursor()
        cls_dict = self._cls_dict
        sub_channel_sql = 'select subchannel_id from content_%s where id = %s'
        channel_sql = 'select channel_id from content_%s where id = %s'
        if plan['is_sub']:
            sql = channel_sql % (cls_dict[plan['platform']][0], plan['category_id'])
            cur.execute(sql)
            result = cur.fetchall()
            if self.is_empty(result):
                return
            plan['subchannel_id'] = plan['category_id']
            plan['channel_id'] = result[0][0]
        else:
            sql_1 = sub_channel_sql % (cls_dict[plan['platform']][1], plan['category_id'])
            cur.execute(sql_1)
            result_1 = cur.fetchall()
            if self.is_empty(result_1):
                return
            sql_2 = channel_sql % (cls_dict[plan['platform']][0], result_1[0][0])
            cur.execute(sql_2)
            result_2 = cur.fetchall()

            if self.is_empty(result_2):
                return
            plan['module_id'] = plan['category_id']
            plan['subchannel_id'] = result_1[0][0]
            plan['channel_id'] = result_2[0][0]

        plan.pop('is_sub', None)
        plan.pop('category_id', None)
        name_str = '(' + ("%s," * len(plan))[:-1] + ')'
        final_sql = ("insert into content_syncjob " + name_str + ' ') % tuple(plan.keys())
        cur.execute(final_sql + ' values ' + name_str, plan.values())

    @staticmethod
    def convert_schedule_to_new(sche):
        pat = re.compile(r'cron 0 ((\d+)|(\d+(,\d+){1,})) \* \* \*')
        sche = sche.strip()
        if sche.startswith('every'):
            time_num = sche.split(' ')[-1]
            sec = 0
            if time_num[-1] == 'm':
                sec = 60 * int(time_num[:-1])
            elif time_num[-1] == 'h':
                sec = 3600 * int(time_num[:-1])
            return {
                'content_syncjob.interval': sec,
                'cron': None
            }
        elif sche.startswith('cron'):
            if not sche.endswith(' * * *'):
                sche += ' *'
	    sche = sche.replace('，', ',')
            m = pat.match(sche)
            if m:
                num_list = m.groups()[0].split(',')
                num_list = map(lambda x: x + ':00', num_list)
                return {
                    'content_syncjob.interval': 0,
                    'cron': ';'.join(num_list)
                }
        else:
	    print 'wrong sche', sche
	    return {}

    @staticmethod
    def is_empty(res):
        if not res or not res[0]:
            return True
        else:
            return False


class IpadFactory(object):
    _channel_dict = {
        'id': 'id', 'title': 'title', 'cid': 'cid', 'state': 'state', 'position': 'position',
        'choiceness_state': 'switch_choiceness', 'all_videos_state': 'switch_all',
        'image_state_for_choiceness': 'image_type_choiceness', 'image_state_for_all': 'image_type_all',
        'image_state_for_marking': 'image_type_sale', 'small_normal_icon': 'icon_small',
        'small_selected_icon': 'icon_small_selected', 'big_normal_icon': 'icon_big',
        'big_selected_icon': 'icon_big_selected', 'for_marking': 'for_sale'
    }
    _subchannel_dict = {
        'id': 'id', 'title': 'title', 'sub_channel_type': 'type', 'image_state': 'image_type', 'position': 'position',
        'video_count_for_pad': 'video_count', 'state': 'state', 'filter': 'filter_collection',
        'channel_entity_id': 'channel_id', 'is_choiceness': 'is_choiceness', 'for_membership': 'for_membership'
    }
    _module_dict = {
        'id': 'id', 'title': 'title', 'module_type': 'module_type', 'state': 'state', 'sub_channel_id': 'subchannel_id',
        'video_count_for_pad': 'video_count', 'position': 'position'
    }

    IMG_TYPE_DICT = {
        'horizontal': 1,
        'vertical': 2
    }
    SUB_TYPE_DICT = {
        'editable_box': 1,
        'editable_video_list': 2,
        'filter': 3
    }

    _fixed_attrs = {
        'is_delete': 0,
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    @property
    def _contrast(self):
        contrast = [
            ('cms_i_pad3_channels', 'content_ipadchannel', self._channel_dict),
            ('cms_ipad_sub_channels', 'content_ipadsubchannel', self._subchannel_dict),
            ('cms_ipad_sub_channel_modules', 'content_ipadsubchannelmodule', self._module_dict)
        ]
        return contrast

    def __init__(self, ruby_conn, py_conn):
        self.ruby_conn = ruby_conn
        self.py_conn = py_conn

    def generate_new_cms_data(self, contrast, table_name):
        """
        contrast keys are ruby fields, values are python schema fields
        results are a list contains dicts of new cms field and values info
        """
        sql = 'select * from %s;' % table_name
        cur = self.ruby_conn.cursor()
        cur.execute(sql)
        des = cur.description
        result = [{contrast[des[index][0]]: v for index, v in enumerate(value) if des[index][0] in contrast.keys()}
                  for value in cur.fetchall()]
        return result

    def make_insert(self, res, table):
        if res:
            fields_len = len(res[0])
            key_list = res[0].keys()
            fill_str = " (" + ("%s," * fields_len)[:-1] + ") "
            first_sql = ("insert into %s" % table + fill_str) % tuple(key_list)
            sql = first_sql + "values " + fill_str
            cur = self.py_conn.cursor()
            for item in res:
                cur.execute(sql, item.values())

            self.py_conn.commit()

    def delete_table(self, table):
        sql = "delete from %s" % table
        cur = self.py_conn.cursor()
        cur.execute(sql)

    def work(self, delete=False):
        self.get_and_insert_info(delete)
        print '[INFO] ipad cms info convert finished!'

    def get_and_insert_info(self, delete_tables=False):
        if delete_tables:
            for tup in self._contrast:
                self.delete_table(tup[1])
        if self._contrast:
            for item in self._contrast:
                res = self.generate_new_cms_data(item[2], item[0])
                if 'subchannelmodule' in item[1]:
                    res = self.makeup_module(res)
                elif 'subchannel' in item[1]:
                    res = self.makeup_subchannel(res)
                elif 'channel' in item[1]:
                    res = self.makeup_channel(res)
                self.make_insert(res, item[1])

    def makeup_channel(self, res):
        for item in res:
            if item['position'] is None:
                item['position'] = 0

            item['content_type'] = item['show_type'] = 1
            item.update(self._fixed_attrs)

        return res

    def makeup_subchannel(self, res):
        for item in res:
            for key in ['position', 'video_count', 'state']:
                if item[key] is None:
                    item[key] = 0
            if item['filter_collection']:
                item['filter_collection'] = item['filter_collection']#.replace('|', ';')
            else:
                item['filter_collection'] = ''
            item['image_type'] = self.IMG_TYPE_DICT[item['image_type']]
            item['type'] = self.SUB_TYPE_DICT[item['type']]
            item.update(self._fixed_attrs)

        return res

    def makeup_module(self, res):
        mod_type_dict = {
            'headline': 1,
            'normal': 0
        }
        for item in res:
            for key in ['position', 'video_count', 'state']:
                if item[key] is None:
                    item[key] = 0
            item['module_type'] = mod_type_dict[item['module_type']]
            item.update(self._fixed_attrs)

        return res


class AndroidFactory(IpadFactory):
    _channel_dict = {
        'id': 'id', 'title': 'title', 'channel_id': 'cid', 'state': 'state', 'position': 'position', 'color': 'color',
        'icon': 'icon', 'button_bg': 'icon_bg', 'content_type': 'content_type',
        'channel_type': 'channel_type',  # channel_type for temp use
    }
    _subchannel_dict = {
        'id': 'id', 'title': 'title', 'sub_channel_type': 'type', 'image_state': 'image_type', 'position': 'position',
        'filter': 'filter_collection', 'channel_entity_id': 'channel_id', 'highlight': 'highlight', 'state': 'state'
    }
    _module_dict = {
        'id': 'id', 'title': 'title', 'module_type': 'module_type', 'position': 'position',
        'sub_channel_id': 'subchannel_id', 'unit_type_collection': 'unit_type_collection', 'jump_type': 'jump_type',
        'sub_channel_id_for_link': 'sub_channel_id_for_link', 'filter_for_link': 'filter_for_link',
        'slider_video_count': 'slider_video_count', 'is_phone_use_only_one_unit': 'phone_one_unit', 'state': 'state'
    }

    @property
    def _contrast(self):
        contrast = [
            ('cms_android_channels', 'content_androidchannel', self._channel_dict),
            ('cms_android_sub_channels', 'content_androidsubchannel', self._subchannel_dict),
            ('cms_android_sub_channel_modules', 'content_androidsubchannelmodule', self._module_dict)
        ]
        return contrast

    def work(self, delete=False):
        self.get_and_insert_info(delete)
        print '[INFO] android cms info convert finished!'

    def makeup_channel(self, res):
        color_board = ('#6bb9dd', '#e36767', '#f6cb7d', '#6ba374')
        remove_keys = []
        for index, item in enumerate(res):
            if item['channel_type'] != 0:
                remove_keys.append(index)
                continue
            item.pop('channel_type', None)
            if item['position'] is None:
                item['position'] = 0

            item['show_type'] = 1
            item['color'] = color_board[randint(0, 3)]
            item.update(self._fixed_attrs)

        for k in reversed(remove_keys):
            del res[k]
        return res

    def makeup_subchannel(self, res):
        remove_keys = []
        for index, item in enumerate(res):
            # TODO: fix 'all' bug
            if item['type'] in ['all', 'recommend_to_me', 'rank']:
                remove_keys.append(index)
                continue
            else:
                item['type'] = self.SUB_TYPE_DICT[item['type']]
            for key in ['position', 'state', 'highlight', 'channel_id']:
                if item[key] is None:
                    item[key] = 0
            if item['filter_collection']:
                item['filter_collection'] = item['filter_collection']#.replace('|', ';')
            else:
                item['filter_collection'] = ''
            item['image_type'] = self.IMG_TYPE_DICT[item['image_type']]
            item['video_count'] = 50 if item['type'] == 2 else 0
            item.update(self._fixed_attrs)

        for k in reversed(remove_keys):
            del res[k]
        return res

    def makeup_module(self, res):
        mod_type_dict = {'normal': 0, 'headline': 1, 'game': 2, 'game_banner': 3}
        for item in res:
            for key in ['position', 'state', 'phone_one_unit']:
                if item[key] is None:
                    item[key] = 0
            for key in ['filter_for_link', 'unit_type_collection']:
                if item[key] is None:
                    item[key] = ''
            item['module_type'] = mod_type_dict[item['module_type']]
            item['filter_for_link'] = item['filter_for_link'].replace('|', ';')
            item['unit_type_collection'] = item['unit_type_collection'].replace(';', ',')
            if item['slider_video_count'] is None:
                item['slider_video_count'] = 5
            if item['sub_channel_id_for_link'] is None:
                item['sub_channel_id_for_link'] = -1
            if not item['jump_type']:
                item['jump_type'] = 'no_jump'

            item.update(self._fixed_attrs)
        return res


class IphoneFactory(IpadFactory):
    _channel_dict = {
        'id': 'id', 'title': 'title', 'state': 'state', 'position': 'position', 'cid': 'cid', 'title_color': 'color',
        'image_state': 'image_type_choiceness', 'choiceness_state': 'switch_choiceness',
        'all_videos_state': 'switch_all', 'state_for_iphone_3_2': 'state_iphone_3_2', 'icon': 'icon',
        'icon_fifty_two': 'icon_52', 'all_image_state': 'image_type_all',
        'icon_for_normal_state': 'icon_3_2', 'icon_for_selected_state': 'icon_3_2_selected',
        # 'image_type' the same with image_type_choiceness
    }
    _subchannel_dict = {
        'id': 'id', 'title': 'title', 'sub_channel_type': 'type', 'image_state': 'image_type', 'position': 'position',
        'filter': 'filter_collection', 'channel_entity_id': 'channel_id', 'state': 'state',
        'is_choiceness': 'is_choiceness', 'module_with_units': 'module_with_units'
    }
    _module_dict = {
        'id': 'id', 'title': 'title', 'module_type': 'module_type', 'position': 'position',
        'sub_channel_id': 'subchannel_id', 'video_count_for_phone': 'iphone_video_count',
        'video_count_for_pad': 'ipad_video_count', 'state': 'state'
    }

    @property
    def _contrast(self):
        contrast = [
            ('cms_ios_channels', 'content_iphonechannel', self._channel_dict),
            ('cms_iphone_sub_channels', 'content_iphonesubchannel', self._subchannel_dict),
            ('cms_iphone_sub_channel_modules', 'content_iphonesubchannelmodule', self._module_dict)
        ]
        return contrast

    def work(self, delete=False):
        self.get_and_insert_info(delete)
        print '[INFO] iphone cms info convert finished!'

    def makeup_channel(self, res):
        for item in res:
            if item['position'] is None:
                item['position'] = 0
            for key in ['position', 'state']:
                if item[key] is None:
                    item[key] = 0

            item['content_type'] = item['show_type'] = 1
            item['channel_id'] = 0
            item['image_type'] = 0
            item.update(self._fixed_attrs)

        return res

    def makeup_subchannel(self, res):
        for item in res:
            for key in ['position', 'state']:
                if item[key] is None:
                    item[key] = 0
            if item['filter_collection']:
                item['filter_collection'] = item['filter_collection']#.replace('|', ';')
            else:
                item['filter_collection'] = ''
            item['image_type'] = self.IMG_TYPE_DICT[item['image_type']]
            item['type'] = self.SUB_TYPE_DICT[item['type']]
            item.update(self._fixed_attrs)

        return res

    def makeup_module(self, res):
        mod_type_dict = {
            'headline': 1,
            'normal': 0
        }
        for item in res:
            for key in ['position', 'state', 'ipad_video_count']:
                if item[key] is None:
                    item[key] = 0
            item['module_type'] = mod_type_dict[item['module_type']]
            item.update(self._fixed_attrs)

        return res


if __name__ == '__main__':
    ruby_conn = get_connection(_DB_RUBY_MYSQL)
    py_conn = get_connection(_DB_LOCAL)

    # below function will delete all videos
    #del_old_videos_of_all_platform(py_conn)

    # delete=True represents the old tables of channels, subchannels and modules will be deleted!
    ipad_factory = IpadFactory(ruby_conn, py_conn)
    ipad_factory.work(delete=True)
    android_factory = AndroidFactory(ruby_conn, py_conn)
    android_factory.work(delete=True)
    iphone_factory = IphoneFactory(ruby_conn, py_conn)
    iphone_factory.work(delete=True)
    fetch_plan = FetchPlan(py_conn)
    fetch_plan.work(delete=True)

    sys.exit()
