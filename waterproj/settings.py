# -*- coding: utf-8 -*-
"""
Django 配置 for waterproj project.

"""

import os
import wewater
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z(d^c!%f2yip&*qzj)bqcq*9lc=ch78(=5n3$79be6xs7om_$i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wewater',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'waterproj.urls'

WSGI_APPLICATION = 'waterproj.wsgi.application'


# Mysql数据库连接信息

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "wewater",
        'USER': 'root',
        'PASSWORD': 'wewater2014',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# 模板文件目录

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'wewater/templates'),
)

# 静态资源如图像等文件目录

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,  'wewater/images')
)
