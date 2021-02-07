#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             04/02/2021               *
*       Skin by MMark                  *
****************************************
'''
from __future__ import print_function
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.PluginList import *
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.InfoBarGenerics import *
from Screens.InfoBar import MoviePlayer, InfoBar
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Tools.Directories import *
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, fileExists
from enigma import *
from enigma import RT_HALIGN_LEFT, getDesktop, RT_HALIGN_RIGHT, RT_HALIGN_CENTER
from enigma import eTimer, eListboxPythonMultiContent, eListbox, eConsoleAppContainer, gFont
from os import path, listdir, remove, mkdir, chmod
from twisted.web.client import downloadPage, getPage
from xml.dom import Node, minidom
import base64
import os
import re
import sys
import shutil
import ssl
import glob
from Tools.LoadPixmap import LoadPixmap

global isDreamOS, regioni, vid
global skin_path, pluglogo, pngx, pngl, pngs

regioni = False

isDreamOS = False
try:
    from enigma import eMediaDatabase
    isDreamOS = True
except:
    isDreamOS = False

'''
PY3 = sys.version_info.major >= 3
'''
PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlparse
    from urllib.parse import urlencode, quote
    from urllib.request import urlretrieve
else:
    from urllib2 import urlopen, Request
    from urllib2 import URLError, HTTPError
    from urlparse import urlparse
    from urllib import urlencode, quote
    from urllib import urlretrieve


if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None

def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)

try:
    from enigma import eDVBDB
except ImportError:
    eDVBDB = None

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def checkStr(txt):
    if PY3:
        if type(txt) == type(bytes()):
            txt = txt.decode('utf-8')
    else:
        if type(txt) == type(unicode()):
            txt = txt.encode('utf-8')
    return txt

def checkInternet():
    try:
        response = checkStr(urlopen("http://google.com", None, 5))
        response.close()
    except HTTPError:
        return False
    except URLError:
        return False
    except socket.timeout:
        return False
    else:
        return True

def checkUrl(url):
    try:
        response = checkStr(urlopen(url, None, 5))
        response.close()
    except HTTPError:
        return False
    except URLError:
        return False
    except socket.timeout:
        return False
    else:
        return True

def getUrl(url):
    print(" Here in getUrl url =", url)
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = checkStr(urlopen(req))
    link = response.read()
    response.close()
    return link


DESKHEIGHT = getDesktop(0).size().height()
currversion = '1.0'
title_plug = '..:: TiVuDream V. %s ::..' % currversion
plugin_path = os.path.dirname(sys.modules[__name__].__file__)
skin_path = plugin_path
pluglogo = plugin_path + '/res/pics/logo.png'
pngx = plugin_path + '/res/pics/plugins.png'
pngl = plugin_path + '/res/pics/plugin.png'
pngs = plugin_path + '/res/pics/setting.png'
HD = getDesktop(0).size()
vid = plugin_path + '/vid.txt'

if HD.width() > 1280:
    if isDreamOS:
        skin_path = plugin_path + '/res/skins/fhd/dreamOs/'
    else:
        skin_path = plugin_path + '/res/skins/fhd/'
else:
    if isDreamOS:
        skin_path = plugin_path + '/res/skins/hd/dreamOs/'
    else:
        skin_path = plugin_path + '/res/skins/hd/'

Panel_Dlist = [
 ('TVD Regioni'),
 ('TVD Paesi'),
 ('TVD Italia'),
 ('ITALIAN VOD MOVIE')
 ]

Panel_Dlist2 = [
 ("Rai"),
 ("Mediaset"),
 ("La7"),
 # ("Dplay")
 ]

Panel_Dlist3 = [
 ("Programmi Tv"),
 ("Teche") 
 ]

class SetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 20))
        self.l.setFont(1, gFont('Regular', 22))
        self.l.setFont(2, gFont('Regular', 24))
        self.l.setFont(3, gFont('Regular', 26))
        self.l.setFont(4, gFont('Regular', 28))
        self.l.setFont(5, gFont('Regular', 30))
        self.l.setFont(6, gFont('Regular', 32))
        self.l.setFont(7, gFont('Regular', 34))
        self.l.setFont(8, gFont('Regular', 36))
        self.l.setFont(9, gFont('Regular', 40))
        if HD.width() > 1280:
            self.l.setItemHeight(50)
        else:
            self.l.setItemHeight(50)

def DListEntry(name, idx):
    res = [name]
    if HD.width() > 1280:

        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(pngs)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1900, 50), font = 7, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:

        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 6), size=(34, 25), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos = (60, 5), size = (1000, 50), font = 1, text = name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT))
    return res

class OneSetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if HD.width() > 1280:
            self.l.setItemHeight(50)
            textfont = int(34)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(50)
            textfont = int(22)
            self.l.setFont(0, gFont('Regular', textfont))

def OneSetListEntry(name):

    res = [name]
    if HD.width() > 1280:
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(pngx)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1200, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 6), size = (34, 25), png = loadPNG(pngx)))
        res.append(MultiContentEntryText(pos = (60, 5), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT))
    return res

def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(OneSetListEntry(name))
        icount = icount+1
        list.setList(plist)


class MainSetting(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('MainSetting')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self['text'] = SetList([])
        self.working = False
        self.selection = 'all'
        self['title'] = Label(title_plug)
        self['info'] = Label('')
        self['info'].setText(_('Please select ...'))
        self['key_yellow'] = Button(_(''))
        self['key_yellow'].hide()
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Exit'))
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self['actions'] = NumberActionMap(['SetupActions', 'ColorActions', ], {'ok': self.okRun,
         'green': self.okRun,
         'back': self.closerm,
         'red': self.closerm,
         'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def closerm(self):
        self.close()

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        for x in Panel_Dlist:
            list.append(DListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1
        self['text'].setList(list)
        self['info'].setText(_('Please select ...'))

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        global regioni
        sel = self.menu_list[idx]
        if sel == _('TVD Paesi'):
            regioni = False
            self.session.open(State)
        elif sel == _('TVD Regioni'):
            regioni = True
            self.session.open(tvRegioni)
        elif sel == ('TVD Italia'):
            name = 'Italia'
            url = "https://www.tvdream.net/web-tv/paesi/italia/"
            self.session.open(tvItalia, name, url)
            
        elif sel == ('ITALIAN VOD MOVIE'):
            self.session.open(Vod)

class Vod(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('ITALIAN VOD MOVIE')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self['text'] = SetList([])
        self.working = False
        self.selection = 'all'
        self['title'] = Label(title_plug)
        self['info'] = Label('')
        self['info'].setText(_('Please select ...'))
        self['key_yellow'] = Button(_(''))
        self['key_yellow'].hide()
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Exit'))
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self['actions'] = NumberActionMap(['SetupActions', 'ColorActions', ], {'ok': self.okRun,
         'green': self.okRun,
         'back': self.closerm,
         'red': self.closerm,
         'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def closerm(self):
        self.close()

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        for x in Panel_Dlist2:
            list.append(DListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1
        self['text'].setList(list)

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        if sel == _('Rai'):
            self.session.open(Rai)
        elif sel == _('Mediaset'):
            self.session.open(Mediaset)
        elif sel == _('La7'):
            self.session.open(La7)
        # elif sel == _('Dplay'):
            # self.session.open(Dplay)

'''
mediaset start
'''
class Mediaset(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        self.names.append("Programmitv")
        self.urls.append("https://www.mediasetplay.mediaset.it/programmitv")
        '''
        on family and film no work play
        '''
        self.names.append("Film")
        self.urls.append("https://www.mediasetplay.mediaset.it/film")
        self.names.append("Family")
        self.urls.append("https://www.mediasetplay.mediaset.it/family")

        self.names.append("Fiction")
        self.urls.append("https://www.mediasetplay.mediaset.it/fiction")
        self.names.append("Kids")
        self.urls.append("https://www.mediasetplay.mediaset.it/kids")
        self.names.append("Documentari")
        self.urls.append("https://www.mediasetplay.mediaset.it/documentari")
        showlist(self.names, self['text'])
        self['info'].setText(_('Please select ...'))

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        self.session.open(Mediaset2, name, url)



class Mediaset2(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.name = name
        self.url = url
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        datas = getUrl(url)
        print('datas :  ', datas)
        self.names = []
        self.urls = []
        if "fiction" in url:
            regexcat = 'a href="/fiction/(.*?)".*?class="_2_UgV">(.*?)</p'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            print ("_gotPageLoad match =", match)
            for url , name in match:
                pic = " "
                name = name.replace("&#x27;","'").replace("&amp;","&") #url
                url = "https://www.mediasetplay.mediaset.it/fiction/" + url
                '''
                https://www.mediasetplay.mediaset.it/programmi-tv/alltogethernow_b100003640
                '''
                print('name : ', name)
                print('url:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
            
        elif "family" in url:
            regexcat = 'class="_3G-Rv undefined "><a href="(.*?)".*?class="_1ovAG">(.*?)<'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            print ("_gotPageLoad match =", match)
            for url, name in match:
                pic = " "
                name = name.replace("&#x27;","'").replace("&amp;","&")# url
                url = "https://www.mediasetplay.mediaset.it" + url
                '''
                https://www.mediasetplay.mediaset.it/browse/film-per-tutta-la-famiglia_e5e6a15c523eec6001de37eac
                '''
                print('name : ', name)
                print('url:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])      
            
        elif "film" in url:
            regexcat = 'a href="/movie/(.*?)".*?class="_2_UgV">(.*?)</p'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            print ("_gotPageLoad match =", match)
            for url, name in match:
                pic = " "
                name = name.replace("&#x27;","'").replace("&amp;","&") #url
                url = "https://www.mediasetplay.mediaset.it/movie/" + url
                '''
                https://www.mediasetplay.mediaset.it/programmi-tv/alltogethernow_b100003640
                '''
                print('name : ', name)
                print('url:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])            
            
        elif "programmi" in url:
            regexcat = 'a href="/programmi-tv/(.*?)".*?class="_2_UgV">(.*?)</p'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            print ("_gotPageLoad match =", match)
            for url , name in match:
                pic = " "
                name = name.replace("&#x27;","'").replace("&amp;","&")# url
                url = "https://www.mediasetplay.mediaset.it/programmi-tv/" + url
                '''
                https://www.mediasetplay.mediaset.it/programmi-tv/alltogethernow_b100003640
                '''
                print('name : ', name)
                print('url:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])

        elif "kids" in url:
            regexcat = 'a href="/video/(.*?)".*?class="_2_UgV">(.*?)</p'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            print ("kids _gotPageLoad match =", match)
            for url, name in match:
                pic = " "
                name = name.replace("&#x27;","'").replace("&amp;","&") # url
                url = "https://www.mediasetplay.mediaset.it/video/" + url
                '''
                https://www.mediasetplay.mediaset.it/kids
                '''
                print('name : ', name)
                print('url:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])

        elif "documentari" in url:
            regexcat = 'a href="/playlist/(.*?)".*?class="_2_UgV">(.*?)</p'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            print ("_gotPageLoad match =", match)
            for url, name in match:
                pic = " "
                name = name.replace("&#x27;","'").replace("&amp;","&") #url
                url = "https://www.mediasetplay.mediaset.it/playlist/" + url
                '''
                https://www.mediasetplay.mediaset.it/programmi-tv/alltogethernow_b100003640
                '''
                print('name : ', name)
                print('url:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        else:
             pass

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        # print('url:  ', url)
        if ("movie" in url) or ("video" in url):
            try:
                print("In playVideo2 url =", url)
                from youtube_dl import YoutubeDL
                '''
                ydl_opts = {'format': 'best'}
                ydl_opts = {'format': 'bestaudio/best'}
                '''
                ydl_opts = {'format': 'best'}
                ydl = YoutubeDL(ydl_opts)
                ydl.add_default_info_extractors()
                result = ydl.extract_info(url, download=False)
                print ("mediaset result =", result)
                url = result["url"]
                print ("mediaset final url =", url)
                self.session.open(Playstream2, name, url)
            except:
                return
        else:
               self.session.open(Mediaset3, name, url)

class Mediaset3(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.name = name
        self.url = url
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        datas = getUrl(url)
        print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            regexcat = '/video/(.*?)".*?"_1ovAG">(.*?)</'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            print ("_gotPageLoad match =", match)
            for url, name  in match:
                pic = " "
                name = name.replace("&#x27;","'").replace("&amp;","&") #url
                url1 = "https://www.mediasetplay.mediaset.it/video/" + url
                print('name : ', name)
                print('url1:  ', url1)
                self.urls.append(url1)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing ...'))
            pass

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        try:
            print("In playVideo2 url =", url)
            from youtube_dl import YoutubeDL
            ydl_opts = {'format': 'best'}
            '''
            ydl_opts = {'format': 'bestaudio/best'}
            '''
            ydl = YoutubeDL(ydl_opts)
            ydl.add_default_info_extractors()
            result = ydl.extract_info(url, download=False)
            print ("mediaset result =", result)
            url = result["url"]
            print ("mediaset final url =", url)

            self.session.open(Playstream2, name, url)
        except:
            self['info'].setText(_('Nothing ...'))
            pass
'''
mediaset end
'''
'''
rai start
'''
class Rai(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        self.names.append("Film")
        self.urls.append("https://www.raiplay.it/film/")
        self.names.append("Serietv")
        self.urls.append("https://www.raiplay.it/serietv/")
        self.names.append("Fiction")
        self.urls.append("https://www.raiplay.it/fiction/")
        self.names.append("Documentari")
        self.urls.append("https://www.raiplay.it/documentari/")
        self.names.append("Bambini")
        self.urls.append("https://www.raiplay.it/bambini/")
        self.names.append("Teen")
        self.urls.append("https://www.raiplay.it/teen/")
        self.names.append("Tgr")
        self.urls.append("http://www.tgr.rai.it/dl/tgr/mhp/home.xml")        
        showlist(self.names, self['text'])

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        if 'Tgr' in name:
            self.session.open(tgrRai)
        else:
            self.session.open(tvRai2, name, url)

class tvRai2(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []

        self.name = name
        self.url = url

        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        content = getUrl(url)

        self.names = []
        self.urls = []
        pic = " "
        regexcat = 'data-video-json="(.*?)".*?<img alt="(.*?)"'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print("showContent2 match =", match)
        print('name : ', name)
        for url, name in match:
            try:
                url1 = "https://www.raiplay.it" + url
                content2 = getUrl(url1)
                print ("showContent321 content2 =", content2)
                regexcat2 = '"/video/(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                print ("showContent321 match2 =", match2)
                url2 = match2[0].replace("json", "html")
                url3 = "https://www.raiplay.it/video/" + url2
                name = name.replace("&#x27;","'").replace("&amp;","&") #url2
                self.names.append(name)
                self.urls.append(url3)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('nameok : ', name)
        print('urlok:  ', url)
        # try:
        print("In playVideo2 url =", url)
        from youtube_dl import YoutubeDL
        ydl_opts = {'format': 'best'}
        '''
        ydl_opts = {'format': 'bestaudio/best'}
        '''
        ydl = YoutubeDL(ydl_opts)
        ydl.add_default_info_extractors()
        result = ydl.extract_info(url, download=False)
        print ("rai result =", result)
        url = result["url"]
        print ("rai final url =", url)
        self.session.open(Playstream2, name, url)
        # except:
            # self['info'].setText(_('Nothing ...'))
            # pass







class tgrRai(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        self.pics = []
        # self.urls.append("http://www.tgr.rai.it/dl/tgr/mhp/home.xml")        
        self.names.append("TG")
        self.urls.append("http://www.tgr.rai.it/dl/tgr/mhp/regioni/Page-0789394e-ddde-47da-a267-e826b6a73c4b.html?tgr")   
        self.pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/tgr.png")
        self.names.append("METEO")
        self.urls.append("http://www.tgr.rai.it/dl/tgr/mhp/regioni/Page-0789394e-ddde-47da-a267-e826b6a73c4b.html?meteo")        
        self.pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/meteo.png")
        self.names.append("BUONGIORNO ITALIA")
        self.urls.append("http://www.tgr.rai.it/dl/rai24/tgr/rubriche/mhp/ContentSet-88d248b5-6815-4bed-92a3-60e22ab92df4.html")  
        self.pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/buongiorno%20italia.png")        
        self.names.append("BUONGIORNO REGIONE")
        self.urls.append("http://www.tgr.rai.it/dl/tgr/mhp/regioni/Page-0789394e-ddde-47da-a267-e826b6a73c4b.html?buongiorno")         
        self.pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/buongiorno%20regione.png")         
        self.names.append("IL SETTIMANALE")
        self.urls.append("http://www.tgr.rai.it/dl/rai24/tgr/rubriche/mhp/ContentSet-b7213694-9b55-4677-b78b-6904e9720719.html")   
        self.pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/il%20settimanale.png")         
        self.names.append("RUBRICHE")
        self.urls.append("http://www.tgr.rai.it/dl/rai24/tgr/rubriche/mhp/list.xml")  
        self.pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/rubriche.png")         
        showlist(self.names, self['text'])
        self['info'].setText(_('Please select ...'))
    
    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        self.session.open(tgrRai2, name, url)

class tgrRai2(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = name
        self.url = url
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        getPage(url).addCallback(self._gotPageLoad2).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))

    def _gotPageLoad2(self, data):
        content = data.replace("\r", "").replace("\t", "").replace("\n", "")
        name = self.name
        self.names = []
        self.urls = []
        self.pics = []
        pic = " "
        try:
            if 'type="video">' in content:
                print('content1 : ', content)
                regexcat = '<label>(.*?)</label>.*?type="video">(.*?)</url>' #relinker
                self["key_green"].setText('Play')
                
            elif 'type="list">' in content: 
                print('content2 : ', content)
                regexcat = '<label>(.*?)</label>.*?type="list">(.*?)</url>'
            else:
                print('passsss')
                pass
            match = re.compile(regexcat, re.DOTALL).findall(content)
            print("showContent2 match =", match)
            print('name : ', name)
            for name, url in match:
                if url.startswith('http'):
                    url1=url
                else:
                    url1 = "http://www.tgr.rai.it" + url
                # pic = image
                self.names.append(name)
                self.urls.append(url1)
                # self.pics.append(pic)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])            
        except:
            pass

        
    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        
        if 'relinker' in url:
            self.session.open(Playstream2, name, url)
        else:
            self.session.open(tgrRai3, name, url)

            
class tgrRai3(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = name
        self.url = url
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        
        getPage(url).addCallback(self._gotPageLoad2).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        
    def _gotPageLoad2(self, data):
        content = data.replace("\r", "").replace("\t", "").replace("\n", "")
        name = self.name        
        self.names = []
        self.urls = []
        self.pics = []
        pic = " "
        try:
            if 'type="video">' in content:
                print('content10 : ', content)
                regexcat = '<label>(.*?)</label>.*?type="video">(.*?)</url>' #relinker
                self["key_green"].setText('Play')
                    
            elif 'type="list">' in content: 
                print('content20 : ', content)
                regexcat = '<label>(.*?)</label>.*?type="list">(.*?)</url>'
            else:
                print('passsss')
                pass
            match = re.compile(regexcat, re.DOTALL).findall(content)
            print("showContent21 match =", match)
            for name, url in match:
                print('name : ', name)
                print('url : ', url)
                if url.startswith('http'):
                    url1=url
                else:
                    url1 = "http://www.tgr.rai.it" + url
                # pic = image 
                self.names.append(name)
                self.urls.append(url1)
                # self.pics.append(pic)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
          
        except:
            pass            
            

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        try:
            print("In playVideo2 url =", url)
            self.session.open(Playstream2, name, url)
        except:
            self['info'].setText(_('Nothing ...'))
            pass












class La7(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        self.names.append("Programmi")
        self.urls.append("https://www.la7.it/programmi")
        self.names.append("Teche")
        self.urls.append("https://www.la7.it/i-protagonisti")        
        
        showlist(self.names, self['text'])

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        self.session.open(tvLa2, name, url)

class tvLa2(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []

        self.name = name
        self.url = url

        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        content = getUrl(url)

        self.names = []
        self.urls = []
        self.pics = []
        pic = " "
        regexcat = '"list-item list-item-.*?a href="(.*?)".*?data-background-image="(.*?)".*?class="titolo">(.*?)<'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print("showContent2 match =", match)
        print('name : ', name)
        for url, pic, name in match:
            try:
                url1 = "https://www.la7.it" + url
                name = name.replace("&#x27;","'").replace("&amp;","&").replace("&#039;","'")
                pic1 = "http:" + pic
                self.names.append(name)
                self.urls.append(url1)
                self.pics.append(pic1)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        self.session.open(tvLa3, name, url)

class tvLa3(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []

        self.name = name
        self.url = url

        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        content = getUrl(url)

        self.names = []
        self.urls = []
        self.pics = []
        pic = " "
        
        if 'protagonisti' in url:
            regexcat = '<div class="list.*?a href="/(.*?)/video(.*?)".*?data-background-image="(.*?)".*?class="title">(.*?)<'        
        else:
            regexcat = '</div><div class="item.*?a href="/(.*?)/video(.*?)".*?data-background-image="(.*?)".*?class="title">(.*?)</'        
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print("showContent2 match =", match)
        print('name : ', name)
        for url1, url2, pic, name in match:
            try:
                url3 = "https://www.la7.it/" + url1 + "/video" + url2
                print("showContent341 url3 =", url3)
                pic1 = "http:" + pic
                name = name.replace("&#x27;","'").replace("&amp;","&").replace("&#039;","'")
                self.names.append(name)
                self.urls.append(url3)
                self.pics.append(pic1)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('tvLa3 name : ', name)
        print('tvLa3 url:  ', url)

        regex2 = '/content/(.*?).mp4'
        regex3 = 'm3u8: "(.*?)"'
        content2 = getUrl(url)
        print('tvLa3 content2:  ', content2)
        x1 = 0
        if x1 == 0:
            if re.findall(regex2, content2):
                 link_video = 'https://awsvodpkg.iltrovatore.it/local/hls/,/content/'+re.findall(regex2, content2)[0]+'.mp4.urlset/master.m3u8'
                 print('tvLa3 link_video:  ', link_video)
            elif re.findall(regex3, content2):
                 link_video = re.findall(regex3, content2)[0]
                 print('tvLa3 link_video 2:  ', link_video)
            print('tvLa3 link_video 3:  ', link_video)
            self.session.open(Playstream2, name, link_video)

class Dplay(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)


    def _gotPageLoad(self):
        # url = "https://it.dplay.com/generi/"
        url = "https://www.discoveryplus.it/generi/"
        content = getUrl(url)
        print("showContent35 content =", content)

        self.names = []
        self.urls = []

        regexcat = 'a href="/genere/(.*?)"'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print("showContent2 match =", match)
        for url in match:
            try:
                # url1 = "https://it.dplay.com/genere/" + url
                url1 = "https://www.discoveryplus.it/generi" + url
                name = url
                self.names.append(name)
                self.urls.append(url1)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        self.session.open(Dplay2, name, url)

class Dplay2(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []

        self.name = name
        self.url = url

        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        content = getUrl(url)

        self.names = []
        self.urls = []
        self.pics = []
        pic = " "
        regexcat = '<div class="b-show-list__single-show">.*?<a href="(.*?)".*?lazy-src="(.*?)".*?alt="(.*?)"'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print("showContent2 match =", match)
        for url, pic, name in match:
            try:
                # url1 = "https://it.dplay.com" + url
                url1 = "https://www.discoveryplus.it" + url
                name = name.replace("&#x27;","'").replace("&amp;","&").replace("&#039;","'")
                self.names.append(name)
                self.urls.append(url1)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        self.session.open(Dplay3, name, url)

class Dplay3(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []

        self.name = name
        self.url = url

        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        content = getUrl(url)

        self.names = []
        self.urls = []
        pic = " "
        regexcat = 'div class="carousel-cell.*?<a href="(.*?)".*?lazyload="(.*?)".*?alt="(.*?)"'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print("showContent2 match =", match)
        print('name : ', name)
        for url, pic, name in match:
            try:
                # url1 = "https://it.dplay.com" + url
                url1 = "https://www.discoveryplus.it" + url
                name = name.replace("&#x27;","'").replace("&amp;","&").replace("&#039;","'")
                self.names.append(name)
                self.urls.append(url1)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        try:
            print("In playVideo2 url =", url)
            from youtube_dl import YoutubeDL
            '''
            ydl_opts = {'format': 'best'}
            '''
            ydl_opts = {'format': 'bestaudio/best'}
            ydl = YoutubeDL(ydl_opts)
            ydl.add_default_info_extractors()
            result = ydl.extract_info(url, download=False)
            print ("rai result =", result)
            url = result["url"]
            print ("rai final url =", url)
            self.session.open(Playstream2, name, url)
        except:
            self['info'].setText(_('Nothing ...'))
            pass



'''
rai end
'''


class State(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = 'http://www.tvdream.net/web-tv/paesi/'
        datas = getUrl(url)
        print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            icount = 0
            start = 0
            n1 = datas.find('menu-sub">', 0)
            if n1 < 0:
                return
            n2 = datas.find("</ul>", n1)
            data2 = datas[n1:n2]
            print("data A2 =", data2)
            pic = " "
            regexcat = 'href="(.*?)">(.*?)<'
            match = re.compile(regexcat, re.DOTALL).findall(data2)
            for url, name in match:
                print('name : ', name)
                print('url:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing ...'))
            pass

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        self.session.open(tvItalia, name, url)

class tvRegioni(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = 'https://www.tvdream.net/web-tv/regioni/'
        datas = getUrl(url)
        print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            icount = 0
            start = 0
            n1 = datas.find('menu-sub">', 0)
            if n1 < 0:
                return
            n2 = datas.find("</ul>", n1)
            data2 = datas[n1:n2]
            print("data A2 =", data2)
            pic = " "
            regexcat = 'href="(.*?)">(.*?)<'
            match = re.compile(regexcat, re.DOTALL).findall(data2)
            for url, name in match:
                print('name : ', name)
                print('url:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing ...'))
            pass

    def okRun(self):
        selection = str(self['text'].getCurrent())
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name : ', name)
        print('url:  ', url)
        self.session.open(tvItalia, name, url)



class tvItalia(Screen):

    def __init__(self, session, name, url ):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.name = name
        self.url = url
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        name = self.name
        url = self.url
        datas = getUrl(url)
        print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            pages = [1, 2 ]
            for page in pages:
                url1 = url + "page/" + str(page) + "/"
                name = "Page " + str(page)
                print('name it : ', name)
                print('url it:  ', url1)
                self.urls.append(url1)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            pass

    def okRun(self):
        try:
            selection = str(self['text'].getCurrent())
            idx = self["text"].getSelectionIndex()
            name = self.names[idx]
            url = self.urls[idx]
            print('name it3: ', name)
            print('url it3: ', url)
            if checkUrl(url):
                self.session.open(tvCanal, name, url)
            else:
                self['info'].setText(_('Nothing ...'))
        except:
            pass

class tvCanal(Screen):

    def __init__(self, session, name, url ):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = OneSetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.name = name
        self.url = url
        self.timer = eTimer()
        self.timer.start(1500, True)
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        datas = getUrl(url)
        print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            icount = 0
            start = 0
            data2 = datas
            print("data A5 =", data2)
            pic = " "
            regexcat = '<div class="item-head.*?href="(.*?)".*?bookmark">(.*?)<'
            '''
            regexcat   = '<div class="item-head.*?a href="(.*?)".*?bookmark">(.*?)<'
            '''
            match = re.compile(regexcat, re.DOTALL).findall(data2)
            for url, name in match:
                print('name ch1: ', name)
                print('url ch1:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing ...'))
            pass

    def okRun(self):
        try:
            selection = str(self['text'].getCurrent())
            idx = self["text"].getSelectionIndex()
            name = self.names[idx]
            url = self.urls[idx]
            content = getUrl(url)
            print('content :  ', content)
            regexcat = '"player".*?href="(.*?)"'
            if regioni == True:
                regexcat = '<iframe src="(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            print("getVideos2 match =", match)
            url2 = match[0]
            content2 = getUrl(url2)
            print("getVideos2 content2 =", content2)
            if ("rai" in url.lower()) or ("rai" in name.lower()):
                regexcat2 = 'liveVideo":{"mediaUrl":"(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                print("getVideos match2 =", match2)
                url = match2[0]
                pic = ""
                print(" Here in playVideo url2 =", url)
                self.session.open(Playstream2, name, url)
            else:
                n1 = content2.find(".m3u8")
                n2 = content2.rfind("http", 0, n1)
                url = content2[n2:(n1+5)]
                print("getVideos2 url3 =", url)
                pic = ""
                print(" Here in playVideo url2 =", url)
                self.session.open(Playstream2, name, url)
        except:
            self['info'].setText(_('Nothing ...'))
            pass



class Playstream2(Screen, InfoBarMenu, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarShowHide):

    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.skinName = 'MoviePlayer'
        title = 'Play'
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self)
        InfoBarShowHide.__init__(self)
        self['actions'] = ActionMap(['WizardActions',
         'MoviePlayerActions',
         'EPGSelectActions',
         'MediaPlayerSeekActions',
         'ColorActions',
         'InfobarShowHideActions',
         'InfobarActions'], {'leavePlayer': self.cancel,
         'back': self.cancel}, -1)
        self.allowPiP = False
        InfoBarSeek.__init__(self, actionmap='MediaPlayerSeekActions')
        url = url.replace(':', '%3a')
        self.url = url
        self.name = name
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.openTest)

    def openTest(self):
        url = self.url
        name = self.name
        print("Here in Playvid name A =", name)
        name = name.replace(":", "-")
        name = name.replace("&", "-")
        name = name.replace(" ", "-")
        name = name.replace("/", "-")
        name = name.replace("›", "-")
        name = name.replace(",", "-")
        print("Here in Playvid name B2 =", name)

        if url is not None:
            url = str(url)
            url = url.replace(":", "%3a")
            url = url.replace("\\", "/")
            print("url final= ", url)
            ref = "4097:0:1:0:0:0:0:0:0:0:" + url
            print("ref= ", ref)
            sref = eServiceReference(ref)
            sref.setName(self.name)
            self.session.nav.stopService()
            self.session.nav.playService(sref)
        else:
           return

    def openTestX(self):
        ref = '4097:0:1:0:0:0:0:0:0:0:' + self.url
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cancel(self):
        if os.path.exists('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(self.srefOld)
        self.close()

    def keyLeft(self):
        self['text'].left()

    def keyRight(self):
        self['text'].right()

    def keyNumberGlobal(self, number):
        self['text'].number(number)

def main(session, **kwargs):
    if checkInternet():
        session.open(MainSetting)
    else:
        session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)

def StartSetup(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('TiVuDream'), main, 'TiVuDream', 15)]
    else:
        return []

def Plugins(**kwargs):
    ico_path = 'logo.png'
    if not isDreamOS:
        ico_path = plugin_path + '/res/pics/logo.png'
    desc_plugin = (_('..:: TiVu Dream Net Player by Lululla %s ::.. ' % currversion))
    name_plugin = (_('TiVuDream'))
    main_menu = PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_MENU, fnc = StartSetup, needsRestart = True)
    extensions_menu = PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = main, needsRestart = True)
    result = [PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_PLUGINMENU, icon = ico_path, fnc = main)]
    result.append(extensions_menu)
    result.append(main_menu)
    return result
