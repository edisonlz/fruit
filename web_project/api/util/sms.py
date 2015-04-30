# -*- coding: utf-8 -*-
import logging
import urllib
import urllib2
import xml.etree.ElementTree as ET
from app.sdk.exceptions import SMS_ERROR
from django.conf import settings

class SMS(object):

    CODE = {
        '00': u'批量短信提交成功（批量短信待审批)',
        '01': u'批量短信提交成功（批量短信跳过审批环节）',
        '02': u'IP限制',
        '03': u'单条短信提交成功',
        '04': u'用户名错误',
        '05': u'密码错误',
        '06': u'剩余条数不足',
        '07': u'信息内容中含有限制词(违禁词)',
        '08': u'信息内容为黑内容',
        '09': u'该用户的该内容 受同天内，内容不能重复发 限制',
        '10': u'批量下限不足',
        '97': u'短信参数有误',
        '98': u'防火墙无法处理这种短信',
        '99': u'短信参数无法解析',
    }

    SUCCESS_CODE_LIST = ['00', '01', '03']

    @classmethod
    def send_sms_message(cls, content, mobiles):

        path = 'http://{host}/QxtSms/QxtFirewall'.format(host='221.179.180.158:9007')
        params = {
            'OperID': settings.GUODO_SMS_ACCOUNT,
            'OperPass': settings.GUODO_SMS_PASSWORD,
            'SendTime': '',
            'ValidTime': '',
            'AppendID': '',
            'DesMobile': ','.join(mobiles),
            'Content': unicode(content).encode('gbk'),
            'ContentType': 8
        }
        url = path + "?" + urllib.urlencode(params)
        logging.debug(url)
        try:
            request = urllib2.Request(url) 
            response = urllib2.urlopen(request, timeout=30).read()
            code = cls.parase_response(body=response).get('code', -1)
            if code not in cls.SUCCESS_CODE_LIST:
                raise SMS_ERROR
        except Exception, e:
            logging.error(e)
            raise SMS_ERROR


    @classmethod
    def parase_response(cls, body):
        ret = {}
        body = body.replace('encoding="gbk"','encoding="utf8"')
        root = ET.fromstring(body)
        code = root.find('code').text
        ret['code'] = code
        ret['desc'] = cls.CODE.get(code)
        return ret

class SMSMessage(object):

    @classmethod
    def register_message(cls,nickname,password):
        msg = u'您申请的优酷游戏账号{nickname}已注册成功，请牢记初始密码密码：{password}。【优酷游戏】'.format(
            nickname=nickname, password=password)
        return msg

    @classmethod
    def verifycode_message(cls, code):
        msg = u'{code}是您本次身份验证码，30分钟内有效，优酷工作人员绝不会向您索取此验证码，切勿告知他人。【优酷游戏】'.format(
            code=code)
        return msg


if __name__ == '__main__':
    print SMS.send_sms_message(content=u'ddadsadsafsda',mobiles=['18701680642',])