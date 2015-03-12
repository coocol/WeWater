# -*- coding: utf-8 -*-

'''
数据库操作
'''

__author__ = 'coocol'

from wewater.models import *

class ReportQueue():
    '''
    处于正在举报状态中的用户队列
    '''
    def exists(self, user_id):
        '''
        队列中是否有此用户
        :param user_id:
        :return if exsits True, else False:
        '''
        b = Reporter.objects.filter(userid=user_id)
        return len(b) > 0

    def dequeue(self, user_id):
        '''
        用户出队列
        :param user_id:
        :return:
        '''
        b = Reporter.objects.filter(userid=user_id)
        b.delete()

    def enqueue(self, user_id, news_id):
        '''
        将用户加入队列
        :param user_id: 用户id
        :param news_id: 用户对应的当前举报消息的id
        :return:
        '''
        b = Reporter()
        b.userid = user_id
        b.newsid = news_id
        b.save()

    def update(self, user_id, news_id):
        '''
        更新用户对应的举报id
        :param user_id: 用户id
        :param news_id: 用户对应的当前举报消息的id
        :return:
        '''
        b = Reporter.objects.filter(userid=user_id)[0]
        b.newsid = news_id
        b.save()

    def get(self, user_id):
        '''
        根据用户id从队列获取正在举报的状态内容
        :param user_id:
        :return:
        '''
        return Reporter.objects.filter(userid=user_id)[0]



class DBAction():
    '''
    数据库处理类
    '''
    def checkLogin(self, admin_name, admin_passwd):
        '''
        检测登陆
        :param admin_name: 管理员名
        :param admin_passwd: 密码
        :return True or False:
        '''
        b = LakeAdmin.objects.filter(adminname=admin_name, password=admin_passwd)
        print b, type(b)
        return len(b) > 0

    def getAllNews(self):
        return News.objects.all().values()

    def getNews(self, news_flag):
        '''
        根据flag获取未解决或已经解决的举报
        :param news_flag:
        :return:
        '''
        return News.objects.filter(flag=news_flag).values()

    def getANews(self, news_id):
        '''
        根据id获得一条举报
        :param news_id:
        :return:
        '''
        try:
            return News.objects.filter(id=news_id)[0]
        except:
            return None

    def updateNewsLocation(self, news_id, location_x, location_y, location_label):
        '''
        更新举报的位置
        :param news_id:
        :param location_x:
        :param location_y:
        :param location_label:
        :return:
        '''
        b = News.objects.filter(id=news_id)[0]
        b.lat = location_x
        b.lng = location_y
        b.label = location_label
        b.save()

    def updateNewsFlag(self, news_id, news_flag):
        '''
        更新举报的状态
        :param news_id:
        :param news_flag:
        :return:
        '''
        b = News.objects.filter(id=news_id)[0]
        b.flag = news_flag
        b.save()

    def getNewsId(self, user_id, news_time):
        '''
        获取一个举报的id
        :param user_id:
        :param news_time:
        :return:
        '''
        b = News.objects.filter(time=news_time, userid=user_id)
        if len(b)>0:
            return b[0].id

    def createNews(self, user_id, news_time, news_content):
        '''
        新增一条举报
        :param user_id:
        :param news_time:
        :param news_content:
        :return:
        '''
        b = News()
        b.userid = user_id
        b.time = news_time
        b.content = news_content
        b.save()
        return self.getNewsId(user_id=user_id, news_time=news_time)

    def isNewsExists(self, news_id):
        '''
        根据id判断举报是否存在
        :param news_id:
        :return:
        '''
        b = News.objects.filter(id=news_id)[0]
        return len(b) > 0

    def getNewsImages(self, news_id):
        '''
        获取举报对应的图片路径
        :param news_id:
        :return:
        '''
        return ImgUrls.objects.filter(newsid=news_id).values()

    def addNewsImage(self, news_id, img_url):
        '''
        为当前举报添加一张图片
        :param news_id:
        :param img_url:
        :return:
        '''
        b = ImgUrls()
        b.imgurl = img_url
        b.newsid = news_id
        b.save()

    def addFeedBack(self, feed):
        '''
        为一条举报创建处理反馈内容
        :param feed:
        :return:
        '''
        try:
            b = FeedBack()
            b.content = feed.get("content")
            b.time = feed.get("time")
            b.newsid = feed.get("newsid")
            b.userid = self.getANews(news_id=b.newsid).userid
            b.admin = feed.get("admin")
            b.save()
            return True
        except:
            return False

    def getFeedBack(self, user_id):
        '''
        获取举报的反馈内容
        :param user_id:
        :return:
        '''
        return FeedBack.objects.filter(userid=user_id)
