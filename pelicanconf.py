#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = 'Megan Karabin'
SITENAME = 'cyberlingual'
SITEURL = 'https://megankarabin.github.io/my-blog'

PATH = 'content'
# BIO = 'Hi, I\'m Megan. I\'m a full-time Master\'s student in cognitive science of language,  part-time programmer/data scientist. 🐍'
STATIC_PATHS = ['images']
# DISPLAY_PAGES_ON_MENU = True

THEME_STATIC_DIR = 'theme/static' 
SOCIAL = (
    ('github', 'https://github.com/megankarabin'),
    ('linkedin', 'https://www.linkedin.com/in/megan-karabin-08413aa9/'),
    ('feed', 'https://pseudowordz.herokuapp.com/')
)
PROFILE_IMAGE = 'cow.jpg'

TIMEZONE = 'America/Toronto'
DEFAULT_LANG = 'en'
DEFAULT_PAGINATION = 10
RELATIVE_URLS = True
# ALT_URL = 'https://pseudowordz.herokuapp.com/'
# set to False for Production, True for Development
if os.environ.get('PELICAN_ENV') == 'DEV':
    RELATIVE_URLS = True
else:
    RELATIVE_URLS = False
