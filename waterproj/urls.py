# -*- coding: utf-8 -*-

'''
请求URL与处理接口映射
'''


from django.conf.urls import patterns, include, url
from django.contrib import admin
import waterproj
from wewater.views import *

# 请求URL

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^allNews/$', getAllNews),
    url(r'^weChat/$', weChat),
    url(r'^login/$', login),
    url(r'^notified/$', checkNotification),
    url(r'^solvedNews/$', getSolvedNews),
    url(r'^solveNews/$', solveNews),
    url(r'^feedback/$', feedNews),
    url(r'^unsolvedNews/$', getUnsolvedNews),
    url(r'^wechat/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': waterproj.settings.STATICFILES_DIRS, 'show_indexes': True}),

)
