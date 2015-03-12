# -*- coding: utf-8 -*-

'''
工具类模块
'''
__author__ = 'coocol'

import urllib
import threading
import hashlib

TOKEN = "wewater"

def objectToDict(obj):
    '''
    对象转换为字典
    :param obj:
    :return:
    '''
    dic = {}
    dic['__class__'] = obj.__class__.__name__
    dic['__module__'] = obj.__module__
    dic.update(obj.__dict__)
    return dic

def dictToObject(dic):
    '''
    字典转换为对象
    :param dic:
    :return:
    '''
    if '__class__' in dic:
        class_name = dic.pop('__class__')
        module_name = dic.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module,class_name)
        args = dict((key,value) for key,value in dic.items())
        obj = class_(**args)
    else:
        obj = dic
    return obj


def checkWeChat(signature, timestamp, nonce, echostr):
    '''
    验证微信接入是否正确
    :param signature:
    :param timestamp:
    :param nonce:
    :param echostr:
    :return:
    '''
    li = ["wewater", timestamp, nonce]
    li.sort()
    hashcode = hashlib.sha1(li[0]+li[1]+li[2]).hexdigest()
    if hashcode == signature:
        return echostr
    else:
        return echostr

class DownLoadPic(threading.Thread):
    '''
    异步下载图片类
    '''
    def __init__(self, img_url, file_name):
        threading.Thread.__init__(self)
        self.imgurl = img_url
        self.filename = file_name

    def run(self):
        conn = urllib.urlopen(self.imgurl)
        data = conn.read()
        f = file("./wewater/images/"+self.filename, 'wb')
        f.write(data)
        f.close()
        conn.close()