# -*- coding: utf-8 -*-

'''
微信消息响应
'''

__author__ = 'coocol@outlook.com'

from wewater import models
from xml.etree import ElementTree
from django.template import Template, Context
from django.template.loader import get_template
from wewater.dbaction.dbaction import *
import time
import wewater.utils.util

# 全局字符串对象

TO_USER = "ToUserName"
FROM_USER = "FromUserName"
CREATE_TIME = "CreateTime"
MSG_TYPE = "MsgType"
CONTENT = "Content"
LOCATION_X = "Location_X"
LOCATION_Y = 'Location_Y'
PIC_URL = "PicUrl"

TEMPLATE_TO_USER = "toUser"
TEMPLATE_FROM_USER = "fromUser"
TEMPLATE_CREATE_TIME = "createTime"
TEMPLATE_CONTENT = "content"

SORRY_STR = "非常抱歉，该微信帐号是武汉大学学生的实践项目，目前还处于开发阶段，开发完成后将首先服务于武汉市。所以我们目前无法受理您的举报，再次说声抱歉"
DEFAULT_STR = "回复1开始举报,回复2前往社区,回复00随时终止举报"
GOTO_COMMUNITY = "<a href=\"http://m.wsq.qq.com/263479264\">点击前往社区</a>"

REPORT_TEXT_STR = "请首先输入文字内容"
REPORT_IMAGE_STR = "请上传图片（可上传多张)"
REPORT_GET_IMAGE_STR = "你可以继续发送图片，最后请务必上传事件的位置或你当前所在的位置"
REPORT_GET_LOCATION_STR = "好了，此次举报已完成，谢谢"

# 服务器用户的微信ID

WECHAT_OPENID = "gh_d89312a42f7c"

class HandleMessages():
    '''
    处理微信消息
    '''
    def __init__(self):
        self.dbDao = DBAction()
        self.reportQueue = ReportQueue()
        self.response_str = ""

    def __getReqTxtAttr__(self, root):
        '''
        获取微信请求的文本消息参数
        :param root:
        :return:
        '''
        self.from_user = root.find(FROM_USER).text
        self.to_user = root.find(TO_USER).text
        self.content = root.find(CONTENT).text

    def __getReqImgAttr__(self, root):
        '''
        获取微信请求的图片消息参数
        :param root:
        :return:
        '''
        self.from_user = root.find(FROM_USER).text
        self.to_user = root.find(TO_USER).text
        self.pic_url = root.find(PIC_URL).text

    def __getReqSubAttr__(self, root):
        '''
        获取微信请求的关注事件参数
        :param root:
        :return:
        '''
        self.from_user = root.find(FROM_USER).text
        self.to_user = root.find(TO_USER).text

    def __getReqLocAttr__(self, root):
        '''
        获取微信请求的位置消息参数
        :param root:
        :return:
        '''
        self.from_user = root.find(FROM_USER).text
        self.to_user = root.find(TO_USER).text
        self.lat = root.find(LOCATION_X).text
        self.lng = root.find(LOCATION_Y).text
        self.label = root.find("Label").text
        if self.label is None:
            self.label = ""

    def __getResTxtXml__(self):
        '''
        获取响应微信用户的文本消息
        :param root:
        :return:
        '''
        context = Context(
            {TEMPLATE_TO_USER: self.from_user, TEMPLATE_FROM_USER: self.to_user, TEMPLATE_CONTENT: self.response_str,
             TEMPLATE_CREATE_TIME: time.time()})
        template = get_template("res_txt_msg.xml")
        r = template.render(context)
        return r

    def __getResNewsXml__(self):
        '''
        获取响应微信用户的图文消息
        :param root:
        :return: 渲染后的模板内容
        '''
        context = Context(
            {TEMPLATE_TO_USER: self.from_user, TEMPLATE_FROM_USER: self.to_user, TEMPLATE_CREATE_TIME: time.time()})
        template = get_template("res_init_news_.xml")
        return template.render(context)

    def __getResCommunityXml__(self):
        '''
        获取响应微信用户的前往社区文本消息
        :param root:
        :return:
        '''
        context = Context(
            {TEMPLATE_TO_USER: self.from_user, TEMPLATE_FROM_USER: self.to_user, TEMPLATE_CREATE_TIME: time.time()})
        template = get_template("res_community_msg.xml")
        return template.render(context)

    def handleTxtMsg(self, root):
        '''
        处理微信的文本消息请求
        :param root: xml数据根节点
        :return:
        '''
        try:
            # 获得请求参数
            self.__getReqTxtAttr__(root)

            if self.content == "00":# 终止举报，用户出队列
                self.response_str = DEFAULT_STR
                if self.reportQueue.exists(user_id=self.from_user):
                    self.reportQueue.dequeue(user_id=self.from_user)
                return self.__getResNewsXml__()
            elif self.content == "1" and not self.reportQueue.exists(user_id=self.from_user):
                # 新建用户举报，入队列
                self.response_str = REPORT_TEXT_STR
                self.reportQueue.enqueue(user_id=self.from_user, news_id=-100)
            elif self.content == "22":# 用户请求获取反馈内容
                fs = list(self.dbDao.getFeedBack(user_id=self.from_user))
                res = ""
                if len(fs) == 0:
                    res = "暂时没有针对你的举报产生的反馈信息"
                else:
                    res = "你的举报有了反馈内容\n"
                    ts = ""
                    for f in fs:
                        ts = str(f.content)+'\n'
                        res += ts
                self.response_str = res
            elif self.reportQueue.exists(user_id=self.from_user):
                # 数据库新增一条举报
                now_time = str(int(time.time()))
                self.dbDao.createNews(user_id=self.from_user, news_time=now_time, news_content=self.content)
                the_news_id = self.dbDao.getNewsId(news_time=now_time, user_id=self.from_user)
                self.reportQueue.update(user_id=self.from_user, news_id=the_news_id)
                self.response_str = REPORT_IMAGE_STR
            elif self.content == "2":# 前往社区
                return self.__getResCommunityXml__()
            else:# 其他情况均返回默认提示内容
                self.response_str = DEFAULT_STR
                return self.__getResNewsXml__()
            return self.__getResTxtXml__()
        except Exception, e:
            print e.message

    def handleSubscribe(self, root):
        '''
        处理微信的关注事件请求
        :param root: xml数据根节点
        :return:
        '''
        self.__getReqSubAttr__(root)
        return self.__getResNewsXml__()

    def handleImgMsg(self, root):
        '''
        处理微信的图片消息请求
        :param root: xml数据根节点
        :return:
        '''
        try:
            self.__getReqImgAttr__(root)
            if self.reportQueue.exists(user_id=self.from_user):
                # 这是举报的图片
                newsid = self.reportQueue.get(user_id=self.from_user).newsid
                picname = str(newsid) + "_" + str(time.time()).replace(".","")+".jpg"
                self.dbDao.addNewsImage(news_id=newsid, img_url=picname)
                # 将图片下载到服务器
                wewater.utils.util.DownLoadPic(img_url=self.pic_url, file_name=picname).start()
                self.response_str = REPORT_GET_IMAGE_STR
            else:# 不是举报图片，返回默认内容
                self.response_str = DEFAULT_STR
        except Exception, e:
            self.response_str = e.message
        return self.__getResTxtXml__()

    def handleLocationMsg(self, root):
        '''
        处理微信的位置消息请求
        :param root: xml数据根节点
        :return:
        '''
        try:
            self.__getReqLocAttr__(root)
            if self.reportQueue.exists(user_id=self.from_user):
                # 举报地点，更新数据库数据
                newsid = self.reportQueue.get(self.from_user).newsid
                self.dbDao.updateNewsLocation(news_id=newsid, location_label=self.label,
                                              location_x=self.lat, location_y=self.lng)
                self.response_str = REPORT_GET_LOCATION_STR
                self.reportQueue.dequeue(user_id=self.from_user)
            else:# 不是举报地点信息，返回默认内容
                self.response_str = DEFAULT_STR
        except Exception, e:
            self.response_str = e.message
        return self.__getResTxtXml__()

    def sendFeedBack(self):
        '''
        向用户返回举报的反馈结果
        :return:
        '''
        fs = list(self.dbDao.getFeedBack(user_id=self.from_user))
        res = "你的举报有了反馈内容\n"
        for f in fs:
            print f.content
            res += f.content + '\n\n'
        if fs is None or len(fs)==0:
            res = "暂时没有针对你的举报产生的反馈信息"
        context = Context(
            {TEMPLATE_TO_USER: self.from_user, TEMPLATE_FROM_USER: self.to_user, TEMPLATE_CONTENT: res,
             TEMPLATE_CREATE_TIME: time.time()})
        template = get_template("res_txt_msg.xml")
        return template.render(context)