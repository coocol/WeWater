# -*- coding: utf-8 -*-

'''
views 请求访问接口
以下方法会被请求触发
'''


from django.shortcuts import render
from utils.util import *
import json
from django.http import HttpResponse
from xml.etree import ElementTree
from msghandler.msghandler import *
from dbaction.dbaction import *


dbaction = DBAction() # 数据库操作对象

msgHandler = HandleMessages() # 微信消息响应对象

def getAllNews(request):
    '''
    请求所有举报
    :param request: http request
    :return: json
    '''
    news = list(dbaction.getAllNews())
    for new in news:
         t = time.localtime(float(new['time']))
         new['time'] = time.strftime("%Y-%m-%d %H:%M:%S", t)
         img = list(dbaction.getNewsImages(news_id=new['id']))
         new["imgurls"] = img
    return outToCliet({"newsList": news})


def getSolvedNews(request):
    '''
    请求已经被解决的举报
    :param request: http request
    :return: json
    '''
    news = list(dbaction.getNews(news_flag=1))
    for new in news:
         t = time.localtime(float(new['time']))
         new['time'] = time.strftime("%Y-%m-%d %H:%M:%S", t)
         img = list(dbaction.getNewsImages(news_id=new['id']))
         new["imgurls"] = img
    return outToCliet({"newsList": news})

def getUnsolvedNews(request):
    '''
    请求还未被解决的举报
    :param request: http request
    :return: json
    '''
    news = list(dbaction.getNews(news_flag=0))
    for new in news:
         t = time.localtime(float(new['time']))
         new['time'] = time.strftime("%Y-%m-%d %H:%M:%S", t)
         img = list(dbaction.getNewsImages(news_id=new['id']))
         new["imgurls"] = img
    return outToCliet({"newsList": news})

def login(request):
    '''
    管理员登录
    :param request: http request
    :return: True or False
    '''
    d = json.loads(request.POST['para'])
    res = dbaction.checkLogin(admin_name=d.get("adminname").encode('utf8'),
                              admin_passwd=d.get("password").encode('utf8'))
    return outToCliet(res)

def solveNews(request):
    '''
    管理员受理举报
    :param request: http request
    :return: json
    '''
    try:
        d = json.loads(request.POST['para'])
        dbaction.updateNewsFlag(news_id=d,news_flag=1)
        return outToCliet(True)
    except Exception, e:
        print e.message
        return outToCliet(False)

def feedNews(request):
    '''
    管理员发来解决的反馈
    :param http request:
    :return:
    '''
    try:
        print request.POST['para']
        d = json.loads(request.POST['para'])
        d['time'] = str(int(time.time()))
        print 'd', d
        res = dbaction.addFeedBack(d)
        return outToCliet(res)
    except:
        return outToCliet(False)

def weChat(request):
    '''
    微信消息处理
    :param http request:
    :return:
    '''
    if request.method == "GET":# 微信接入验证
        echo = checkWeChat(request.GET.get('signature'), request.GET.get('timestamp'),
                               request.GET.get('nonce'), request.GET.get('echostr'))
        return HttpResponse(echo)
    elif request.method == "POST":# 微信用户消息
        d = request.body
        root = ElementTree.fromstring(d)
        try:
            return HttpResponse(handleMessages(root))
        except Exception, e:
            return HttpResponse(getErrorTemplate(root, e.message))


def handleMessages(root):
    '''
    处理微信消息
    :param root: xml数据根节点
    :return:
    '''
    type = root.find(MSG_TYPE).text
    # 按照消息类型进行分发处理
    if type == "text":
        return msgHandler.handleTxtMsg(root)
    elif type == "image":
        return msgHandler.handleImgMsg(root)
    elif type == "event":
        if root.find("Event").text == "subscribe":
            return msgHandler.handleSubscribe(root)
    elif type == "location":
        return msgHandler.handleLocationMsg(root)

def getErrorTemplate(root, msg):
    '''
    得到默认异常响应
    :param root: xml数据根节点
    :param msg:
    :return:
    '''
    context = Context({TEMPLATE_TO_USER: root.find(FROM_USER).text, TEMPLATE_FROM_USER: root.find(TO_USER).text,
                               TEMPLATE_CONTENT: "错了" + msg,
                               TEMPLATE_CREATE_TIME: time.time()})
    template = get_template("res_txt_msg.xml")
    return template.render(context)


def outToCliet(res):
    '''
    返回json数据的http response
    :param res:
    :return:
    '''
    return HttpResponse(json.dumps(res))