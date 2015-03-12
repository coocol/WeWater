# -*- coding: utf-8 -*-

'''
django 数据模型
每个Model对应Mysql中的表
'''

from django.db import models
from admin import admin

class News(models.Model):
    '''  用户产生的举报数据表  '''
    id = models.AutoField(primary_key=True, auto_created=True, verbose_name="ID", serialize=False)
    content = models.TextField()
    time = models.CharField(max_length=20)
    lat = models.FloatField(default=30.0)
    lng = models.FloatField(default=114.0)
    label = models.CharField(max_length=100, null=True, default="")
    userid = models.CharField(max_length=200)
    flag = models.IntegerField(default=0)

    def __unicode__(self):
        return "users' reports"

class ImgUrls(models.Model):
    '''  举报的图片URL  '''
    newsid = models.IntegerField()
    imgurl = models.CharField(max_length=50)

    def __unicode__(self):
        return "news' images"


class LakeAdmin(models.Model):
    '''  湖区管理员数据表  '''
    adminname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    tele = models.CharField(max_length=20)
    email = models.CharField(max_length=20)

    def __unicode__(self):
        return 'lake admin'

class Reporter(models.Model):
    '''
    当前举报用户队列表
    '''
    userid = models.CharField(max_length=100)
    newsid = models.IntegerField()

class FeedBack(models.Model):
    '''
    举报的反馈内容
    '''
    newsid = models.IntegerField()
    userid = models.CharField(max_length=100)
    time = models.CharField(max_length=20)
    content = models.TextField()
    admin = models.CharField(max_length=20)

# 向admin注册Model，便于管理
admin.site.register(News)
admin.site.register(LakeAdmin)
admin.site.register(ImgUrls)
admin.site.register(FeedBack)
