#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             25/02/2022               *
*       Skin by MMark                  *
****************************************
#--------------------#
#Info http://t.me/tivustream
'''
from __future__ import print_function
from Components.AVSwitch import AVSwitch
# from Screens.InfoBarGenerics import *
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.config import ConfigSubsection, config, configfile, ConfigText, ConfigDirectory, ConfigSelection,ConfigYesNo, ConfigEnableDisable
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.PluginList import *
from Components.ScrollLabel import ScrollLabel
from Components.SelectionList import SelectionList, SelectionEntryComponent
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.List import List
from Components.Sources.Source import Source
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.InfoBar import InfoBar
from Screens.InfoBar import MoviePlayer
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop, Standby
from Screens.InfoBarGenerics import InfoBarShowHide, InfoBarSubtitleSupport, InfoBarSummarySupport, \
	InfoBarNumberZap, InfoBarMenu, InfoBarEPG, InfoBarSeek, InfoBarMoviePlayerSummarySupport, \
	InfoBarAudioSelection, InfoBarNotifications, InfoBarServiceNotifications
from ServiceReference import ServiceReference
from Tools.Directories import SCOPE_PLUGINS
from Tools.Directories import *
from Tools.Directories import resolveFilename
from Tools.LoadPixmap import LoadPixmap
from Tools.Notifications import AddPopup
from enigma import *
from enigma import RT_HALIGN_CENTER, RT_VALIGN_CENTER
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT
from enigma import eListbox, eTimer
from enigma import eListboxPythonMultiContent, eConsoleAppContainer
from enigma import eServiceCenter
from enigma import eServiceReference
from enigma import eSize, ePicLoad
from enigma import iPlayableService
from enigma import gFont
from enigma import iServiceInformation
from enigma import loadPNG
from enigma import quitMainloop
from os import path, listdir, remove, mkdir, chmod
from twisted.web.client import downloadPage, getPage
from xml.dom import Node, minidom
import base64
import glob
import hashlib
import json
import os
import re
import shutil
import six
import ssl
import sys
from sys import version_info                                 
import time
try:
    from Plugins.Extensions.tvDream.Utils import *
except:
    from . import Utils

global regioni, skin_dream
regioni = False

PY3 = sys.version_info.major >= 3
print('Py3: ',PY3)
if PY3:
    from urllib.request import urlopen
    from urllib.request import Request
else:
    from urllib2 import Request
    from urllib2 import urlopen

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
    from OpenSSL import SSL
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False
if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx

currversion = '1.2'
plugin_path = os.path.dirname(sys.modules[__name__].__file__)
res_plugin_path = plugin_path + '/res/'
# host_b7 = 'https://feed.entertainment.tv.theplatform.eu/f/PR1GhC/mediaset-prod-all-stations'
desc_plugin = '..:: TiVu Dream Net Player by Lululla %s ::.. ' % currversion
name_plugin = 'TiVuDream Player'
skin_dream = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/hd/".format('tvDream'))
if isFHD():
    skin_dream = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/fhd/".format('tvDream'))
if DreamOS():
    skin_dream = skin_dream + 'dreamOs/'
twxtv = 'aHR0cH+M6Ly9+wYXRidXdlY+i5oZXJva3V+hcHAuY29tL2Fw+aS9wbGF5+P3VybD0='

Panel_Dlist = [
 ('TVD Regions'),
 ('TVD State'),
 ('TVD Italia'),
 ('TVD Category'),
 ('TVD New'),
 ]

class SetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        self.l.setItemHeight(50)
        textfont = int(24)
        self.l.setFont(0, gFont('Regular', textfont))        
        if isFHD():
            self.l.setItemHeight(50)
            textfont = int(34)
            self.l.setFont(0, gFont('Regular', textfont))

def DListEntry(name, idx):
    res = [name]
    pngs = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/setting.png".format('tvDream'))
    res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(pngs)))
    res.append(MultiContentEntryText(pos = (60, 0), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))    
    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(pngs)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1900, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:    
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))           
    return res

def OneSetListEntry(name):
    res = [name]
    pngx = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/plugins.png".format('tvDream'))
  
    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(pngx)))
        res.append(MultiContentEntryText(pos = (60, 0), size = (1200, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos = (10, 12), size = (34, 25), png = loadPNG(pngx)))
        res.append(MultiContentEntryText(pos = (60, 2), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER))      
        
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
        skin = skin_dream + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('MainSetting')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self['text'] = SetList([])
        self.working = False
        self.selection = 'all'
        self['title'] = Label(desc_plugin)
        self['info'] = Label('')
        self['info'].setText(_('Please select ...'))
        self['key_yellow'] = Button(_(''))
        self['key_yellow'].hide()
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Exit'))
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions', ], {'ok': self.okRun,
         'green': self.okRun,
         'back': self.closerm,
         'red': self.closerm,
         'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def closerm(self):
        deletetmp()
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
        if sel == _('TVD State'):
            regioni = False
            self.session.open(State)
        elif sel == _('TVD Regions'):
            regioni = True
            self.session.open(tvRegioni)
        elif sel == ('TVD Italia'):
            name = 'Italia'
            url = "http://www.tvdream.net/web-tv/paesi/italia/"
            self.session.open(tvItalia, name, url)
        elif sel == ('TVD Category'):
            name = 'Category'
            # regioni = True
            url = "https://www.tvdream.net/web-tv/categorie/"
            self.session.open(tvCategory, name, url)
        elif sel == ('TVD New'):
            name = 'New'
            url = "https://www.tvdream.net/web-tv/nuovi/"
            self.session.open(tvNew, name, url)

class State(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_dream + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['text'] = SetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)    
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        url = 'http://www.tvdream.net/web-tv/paesi/'
        if check(url):
            datas = getUrl(url)
            if PY3:
                datas = six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                icount = 0
                start = 0
                n1 = datas.find('menu-sub">', 0)
                if n1 < 0:
                    return
                n2 = datas.find("</ul>", n1)
                data2 = datas[n1:n2]
                # print("data A2 =", data2)
                pic = " "
                regexcat = 'href="(.*?)">(.*?)<'
                match = re.compile(regexcat, re.DOTALL).findall(data2)
                for url, name in match:
                    print('name : ', name)
                    print('url:  ', url)
                    url = url
                    name = checkStr(name)
                    self.urls.append(url)
                    self.names.append(name)
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ',i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(tvItalia, name, url)

class tvRegioni(Screen):
    def __init__(self, session):
        self.session = session
        skin = skin_dream + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['text'] = SetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)    
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        url = 'http://www.tvdream.net/web-tv/regioni/'
        if check(url):
            datas = getUrl(url)
            if PY3:
                datas = six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                icount = 0
                start = 0
                n1 = datas.find('menu-sub">', 0)
                if n1 < 0:
                    return
                n2 = datas.find("</ul>", n1)
                data2 = datas[n1:n2]
                # print("data A2 =", data2)
                pic = " "
                regexcat = 'href="(.*?)">(.*?)<'
                match = re.compile(regexcat, re.DOTALL).findall(data2)
                for url, name in match:
                    print('name : ', name)
                    print('url:  ', url)
                    if 'Logo di TVdream' in name:
                        continue
                    url = url
                    name = checkStr(name)
                    self.urls.append(url)
                    self.names.append(name)
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ',i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(tvItalia, name, url)

class tvItalia(Screen):
    def __init__(self, session, name, url ):
        self.session = session
        skin = skin_dream + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['text'] = SetList([])
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
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)            
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        name = self.name
        url = self.url
        if check(url):
            datas = getUrl(url)
            if PY3:
                datas =six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ]
                for page in pages:
                    url1 = url + "page/" + str(page) + "/"
                    name = "Page " + str(page)
                    print('name it : ', name)
                    print('url it:  ', url1)
                    self.urls.append(url1)
                    self.names.append(name)
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ',i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(tvCanal, name, url)

class tvCanal(Screen):
    def __init__(self, session, name, url ):
        self.session = session
        skin = skin_dream + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['text'] = SetList([])
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
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)            
        self['title'] = Label(desc_plugin)
        global SREF
        SREF = self.session.nav.getCurrentlyPlayingServiceReference()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        datas = getUrl(url)
        # print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            icount = 0
            start = 0
            data2 = datas
            # print("data A5 =", data2)
            pic = " "
            regexcat = '<div class="item__.*?href="(.*?)".*?alt="(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(data2)
            for url, name in match:
                # print('name ch1: ', name)
                # print('url ch1:  ', url)
                if 'Logo di TVdream' in name:
                    continue                
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing ... Retry'))
            
    def okRun(self):
        i = len(self.names)
        print('iiiiii= ',i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name okRun: ', name)
        print('url okRun:  ', url)
        if check(url):
            content = getUrl(url)
            if PY3:
                content = six.ensure_str(content)
            print('content okRun ====================:  ', content)
            try:
                regexcat = 'item__.*?href="(.*?)"'
                # regexcat = 'class="player.*?href="(.*?)"'
                # if content.find('iframe src='):
                    # regexcat = 'player-video.*?iframe src="(.*?)"'
                    
                if regioni == True:  
                    regexcat = '<iframe src="(.*?)"'       
                else:
                    regexcat = 'item__.*?href="(.*?)"'

                if '"btn-site"' in content:
                    print('content btn-site')
                    regexcat = '"btn-site".*?href="(.*?)"'
                    
                if 'player-ext" href="' in content:
                    print('content btn-site')
                    regexcat = '"btn-site".*?href="(.*?)"'
                    
                if 'player-video"' in content:
                    print('content btn-site')
                    if content.find('iframe src='):
                        regexcat = 'player-video.*?iframe.*?src="(.*?)"'
   

                match = re.compile(regexcat, re.DOTALL).findall(content)
                print("get regexcat =", regexcat)
                url = match[0]
                print("get url2 =", url)
                content2 = getUrl(url)
                if PY3:
                    content2 = six.ensure_str(content2)                                               
                print("getVideos2 content2 =", content2)

                if '.m3u8' in content2:
                    print('content .m3u8')
                    n1 = content2.find(".m3u8")
                    n2 = content2.rfind("http", 0, n1)
                    url = content2[n2:(n1+5)]
                    pic = ""
                    self.session.open(Playstream2, name, url)
                    
                elif 'source src="' in content2:
                    print('content .mp4')
                    regexcat2 = 'source src="(.*?)"'
                    match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                    url = match2[0]                    
                    n1 = url.find(".mp4")
                    n2 = url.rfind("http", 0, n1)
                    url = url[n2:(n1+5)]
                    pic = ""
                    self.session.open(Playstream2, name, url)

                elif '<a class="player-' in content2:
                    print("In player url =", url)
                    regexcat2 = '<a class="player-.*?href="(.*?)"'
                    match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                    url = match2[0]                    
                    pic = ""
                    content3 = getUrl(url)
                    if PY3:
                        content3 = six.ensure_str(content3)                                               
                    print("getVideos2 content2 =", content3)
                    if '.m3u8' in content3:
                        print('content .m3u8')
                        n1 = content3.find(".m3u8")
                        n2 = content3.rfind("http", 0, n1)
                        url = content3[n2:(n1+5)]
                        pic = ""
                        # self.session.open(Playstream2, name, url)                    
                        self.session.open(Playstream2, name, url)

                elif '<a class="player_' in content2:
                    print("In player url =", url)
                    regexcat2 = '<a class="player_.*?href="(.*?)"'
                    match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                    url = match2[0]                    
                    pic = ""
                    content3 = getUrl(url)
                    if PY3:
                        content3 = six.ensure_str(content3)                                               
                    print("getVideos2 content2 =", content3)
                    if '.m3u8' in content3:
                        print('content .m3u8')
                        n1 = content3.find(".m3u8")
                        n2 = content3.rfind("http", 0, n1)
                        url = content3[n2:(n1+5)]
                        pic = ""
                        self.session.open(Playstream2, name, url)
                    
                elif ("rai" in url.lower()) or ("rai" in name.lower()):
                    print("In rai url =", url)
                    regexcat2 = 'liveVideo":{"mediaUrl":"(.*?)"'
                    match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                    url = match2[0]
                    pic = ""
                    self.session.open(Playstream2, name, url)

                elif "youtube" in url.lower():   
                    print("In youtube url =", content2)
                    from Plugins.Extensions.tvDream.youtube_dl import YoutubeDL
                    ydl_opts = {'format': 'best'}
                    '''
                    ydl_opts = {'format': 'bestaudio/best'}
                    '''
                    ydl = YoutubeDL(ydl_opts)
                    ydl.add_default_info_extractors()
                    result = ydl.extract_info(url, download=False)
                    # print ("mediaset result =", result)
                    url = result["url"]
                    # print ("mediaset final url =", url)
                    self.session.open(Playstream2, name, url)    
                    
                else:
                    regexcat = '<iframe.*?src="(.*?)"'
                    match = re.compile(regexcat, re.DOTALL).findall(content)
                    print("getVideos2 match =", match)
                    url2 = match[0]
                    print("getVideos2 url2 =", url2)
                    # twitch = url2.find('twitch.tv')
                    # twitch = url2.find('player.twitch')
                    
                    if not 'player.twitch' in content:
                        self.testinpl(name,url2)
                        
                    elif content.find('player.twitch'):
                    # if twitch:
                        match = re.compile(regexcat, re.DOTALL).findall(content)
                        print("get regexcat =", regexcat)
                        url2 = match[0]
                        print("get url2 =", url2)
                    # twitch = url2.find('player.twitch')
                    # if twitch:
                        url3 = url2.replace('https://player.twitch.tv/?channel=','').replace('&parent=www.tvdream.net','')
                        urlx = twxtv.replace('+','')
                        url = b64decoder(urlx) + 'https://www.twitch.tv/' + url3
                        self.session.open(Playstream2, name, url)
                    else:
                        self.testinpl(name, url)
                    return
                    
                return
                    

            except:
                self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)
                self['info'].setText(_('Nothing ... Retry'))
            return
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)

    def testinpl(self, name, url):
        try:
            content2 = getUrl(url)
            if PY3:
                content2 = six.ensure_str(content2)                                               
            print("getVideos2 content2 =", content2)
            if '.m3u8' in content2:
                print('content .m3u8')
                n1 = content2.find(".m3u8")
                n2 = content2.rfind("http", 0, n1)
                url = content2[n2:(n1+5)]
                pic = ""
                self.session.open(Playstream2, name, url)
                
            elif 'source src="' in content2:
                print('content .mp4')
                regexcat2 = 'source src="(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                url = match2[0]                    
                n1 = url.find(".mp4")
                n2 = url.rfind("http", 0, n1)
                url = url[n2:(n1+5)]
                pic = ""
                self.session.open(Playstream2, name, url)

            elif '<a class="player-' in content2:
                print("In player url =", url)
                regexcat2 = '<a class="player-.*?href="(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                url = match2[0]                    
                pic = ""
                content3 = getUrl(url)
                if PY3:
                    content3 = six.ensure_str(content3)                                               
                print("getVideos2 content2 =", content3)
                if '.m3u8' in content3:
                    print('content .m3u8')
                    n1 = content3.find(".m3u8")
                    n2 = content3.rfind("http", 0, n1)
                    url = content3[n2:(n1+5)]
                    pic = ""
                    # self.session.open(Playstream2, name, url)                    
                    self.session.open(Playstream2, name, url)

            elif '<a class="player_' in content2:
                print("In player url =", url)
                regexcat2 = '<a class="player_.*?href="(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                url = match2[0]                    
                pic = ""
                content3 = getUrl(url)
                if PY3:
                    content3 = six.ensure_str(content3)                                               
                print("getVideos2 content2 =", content3)
                if '.m3u8' in content3:
                    print('content .m3u8')
                    n1 = content3.find(".m3u8")
                    n2 = content3.rfind("http", 0, n1)
                    url = content3[n2:(n1+5)]
                    pic = ""
                    self.session.open(Playstream2, name, url)
                
            elif ("rai" in url.lower()) or ("rai" in name.lower()):
                print("In rai url =", url)
                regexcat2 = 'liveVideo":{"mediaUrl":"(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                url = match2[0]
                pic = ""
                self.session.open(Playstream2, name, url)

            elif "youtube" in url.lower():   
                print("In youtube url =", content2)
                from Plugins.Extensions.tvDream.youtube_dl import YoutubeDL
                ydl_opts = {'format': 'best'}
                '''
                ydl_opts = {'format': 'bestaudio/best'}
                '''
                ydl = YoutubeDL(ydl_opts)
                ydl.add_default_info_extractors()
                result = ydl.extract_info(url, download=False)
                # print ("mediaset result =", result)
                url = result["url"]
                # print ("mediaset final url =", url)
                self.session.open(Playstream2, name, url) 
            return
        except:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)
            self['info'].setText(_('Nothing ... Retry'))

class tvCategory(Screen):
    def __init__(self, session, name, url ):
        self.session = session
        skin = skin_dream + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['text'] = SetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.timer = eTimer()
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)            
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        url = 'https://www.tvdream.net/web-tv/categorie/'
        if check(url):
            datas = getUrl(url)
            if PY3:
                datas = six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                icount = 0
                start = 0
                n1 = datas.find('menu-sub">', 0)
                if n1 < 0:
                    return
                n2 = datas.find("</ul>", n1)
                data2 = datas[n1:n2]
                # print("data A2 =", data2)
                pic = " "
                regexcat = 'href="(.*?)">(.*?)<'
                match = re.compile(regexcat, re.DOTALL).findall(data2)
                for url, name in match:
                    if 'Logo di TVdream' in name:
                        continue                
                    print('name : ', name)
                    print('url:  ', url)
                    url = url
                    name = checkStr(name)
                    self.urls.append(url)
                    self.names.append(name)
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ',i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(subCategory, name, url)

class subCategory(Screen):
    def __init__(self, session, name, url ):
        self.session = session
        skin = skin_dream + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['text'] = SetList([])
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
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)            
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        name = self.name
        url = self.url
        if check(url):
            datas = getUrl(url)
            if PY3:
                datas =six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ]
                for page in pages:
                    url1 = url + "page/" + str(page) + "/"
                    name = "Page " + str(page)
                    print('name it : ', name)
                    print('url it:  ', url1)
                    self.urls.append(url1)
                    self.names.append(name)
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ',i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(tvCanal, name, url)

class tvNew(Screen):
    def __init__(self, session, name, url ):
        self.session = session
        skin = skin_dream + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['text'] = SetList([])
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
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)            
        global SREF
        SREF = self.session.nav.getCurrentlyPlayingServiceReference()
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        url = self.url
        name = self.name
        if check(url):
            datas = getUrl(url)
            if PY3:
                datas = six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                icount = 0
                start = 0
                # print("data A5 =", data2)
                pic = " "
                regexcat = 'item-featured__thumb.*?href="(.*?)".*?alt="(.*?)"'
                '''
                regexcat   = '<div class="item-head.*?a href="(.*?)".*?bookmark">(.*?)<'
                '''
                match = re.compile(regexcat, re.DOTALL).findall(datas)
                for url, name in match:
                    print('name ch1: ', name)
                    print('url ch1:  ', url)
                    if 'Logo di TVdream' in name:
                        continue
                    url = url
                    name = checkStr(name)
                    self.urls.append(url)
                    self.names.append(name)
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])                
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)


    def okRun(self):
        i = len(self.names)
        print('iiiiii= ',i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        if check(url):
            content = getUrl(url)
            if PY3:
                content = six.ensure_str(content)
            print('content :  ', content)
            try:
                regexcat = '<iframe.*?src="(.*?)"'
                # yt = content.find('youtube')
                # if yt:
                    # regexcat = 'player-video.*?src="(.*?)"'
                match = re.compile(regexcat, re.DOTALL).findall(content)
                print("getVideos2 match =", match)
                url2 = match[0]
                print("getVideos2 url2 =", url2)
                # twitch = content.find('player.twitch')
                if not 'player.twitch' in content:
                    self.testinpl(name,url2)
                    
                elif content.find('player.twitch'):
                    url3 = url2.replace('https://player.twitch.tv/?channel=','').replace('&parent=www.tvdream.net','')
                    urlx = twxtv.replace('+','')
                    url = b64decoder(urlx) + 'https://www.twitch.tv/' + url3
                    self.session.open(Playstream2, name, url)
                else:        
                    self.testinpl(name,url2)
                # return
                        
            except:
                # self.testinpl(name,url2)
                self['info'].setText(_('Nothing ... Retry'))
            return
                
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)

    def testinpl(self, name, url2):
        try:
            content2 = getUrl(url2)
            if PY3:
                content2 = six.ensure_str(content2)                                               
            print("getVideos2 content2 =", content2)
            if '.m3u8' in content2:
                print('content .m3u8')
                n1 = content2.find(".m3u8")
                n2 = content2.rfind("http", 0, n1)
                url = content2[n2:(n1+5)]
                pic = ""
                self.session.open(Playstream2, name, url)

            elif "youtube" in url.lower():   
                print("In youtube url =", content2)
                from Plugins.Extensions.tvDream.youtube_dl import YoutubeDL
                ydl_opts = {'format': 'best'}
                '''
                ydl_opts = {'format': 'bestaudio/best'}
                '''
                ydl = YoutubeDL(ydl_opts)
                ydl.add_default_info_extractors()
                result = ydl.extract_info(url, download=False)
                # print ("mediaset result =", result)
                url = result["url"]
                # print ("mediaset final url =", url)
                self.session.open(Playstream2, name, url)  
                
            elif 'source src="' in content2:
                print('content .mp4')
                regexcat2 = 'source src="(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                url = match2[0]                    
                n1 = url.find(".mp4")
                n2 = url.rfind("http", 0, n1)
                url = url[n2:(n1+5)]
                pic = ""
                self.session.open(Playstream2, name, url)

            elif '<a class="player-' in content2:
                print("In player url =", url)
                regexcat2 = '<a class="player-.*?href="(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                url = match2[0]                    
                pic = ""
                content3 = getUrl(url)
                if PY3:
                    content3 = six.ensure_str(content3)                                               
                print("getVideos2 content2 =", content3)
                if '.m3u8' in content3:
                    print('content .m3u8')
                    n1 = content3.find(".m3u8")
                    n2 = content3.rfind("http", 0, n1)
                    url = content3[n2:(n1+5)]
                    pic = ""
                    self.session.open(Playstream2, name, url)

            elif '<a class="player_' in content2:
                print("In player url =", url)
                regexcat2 = '<a class="player_.*?href="(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                url = match2[0]                    
                pic = ""
                content3 = getUrl(url)
                if PY3:
                    content3 = six.ensure_str(content3)                                               
                print("getVideos2 content2 =", content3)
                if '.m3u8' in content3:
                    print('content .m3u8')
                    n1 = content3.find(".m3u8")
                    n2 = content3.rfind("http", 0, n1)
                    url = content3[n2:(n1+5)]
                    pic = ""
                    self.session.open(Playstream2, name, url)
                
            elif ("rai" in url.lower()) or ("rai" in name.lower()):
                print("In rai url =", url)
                regexcat2 = 'liveVideo":{"mediaUrl":"(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                url = match2[0]
                pic = ""
                self.session.open(Playstream2, name, url)

            return

        except:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)
            self['info'].setText(_('Nothing ... Retry'))



class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3
    skipToggleShow = False

    def __init__(self):
        self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {"toggleShow": self.OkPressed,
         "hide": self.hide}, 0)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted})
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(self.doTimerHide)
        except:
            self.hideTimer.callback.append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def OkPressed(self):
        self.toggleShow()

    def toggleShow(self):
        if self.skipToggleShow:
            self.skipToggleShow = False
            return
        if self.__state == self.STATE_HIDDEN:
            self.show()
            self.hideTimer.stop()
        else:
            self.hide()
            self.startHideTimer()

    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            self.hideTimer.stop()
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1500, True)

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def doShow(self):
        self.hideTimer.stop()
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()
    def lockShow(self):
        try:
            self.__locked += 1
        except:
            self.__locked = 0
        if self.execing:
            self.show()
            self.hideTimer.stop()
            self.skipToggleShow = False

    def unlockShow(self):
        try:
            self.__locked -= 1
        except:
            self.__locked = 0
        if self.__locked < 0:
            self.__locked = 0
        if self.execing:
            self.startHideTimer()

    def debug(obj, text = ""):
        print(text + " %s\n" % obj)


class Playstream1(Screen):
    def __init__(self, session, name, url):
        self.session = session
        skin = skin_dream + 'Playstream1.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['list'] = SetList([])
        self['info'] = Label('Select Player')
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Select'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'TimerEditActions'], {'red': self.cancel,
         'green': self.okClicked,
         'back' : self.cancel,
         'cancel': self.cancel,
         'ok': self.okClicked}, -2)
        self.name1 = name
        self.url = url
        print('In Playstream2 self.url =', url)
        global srefInit
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        srefInit = self.initialservice
        self.onLayoutFinish.append(self.openTest)

    def openTest(self):
        url = self.url
        self.names = []
        self.urls = []
        self.names.append('Play Direct')
        self.urls.append(url)
        self.names.append('Play Hls')
        self.urls.append(url)
        self.names.append('Play Ts')
        self.urls.append(url)
        showlist(self.names, self['text']) 

    def okClicked(self):
        idx = self['list'].getSelectionIndex()
        if idx != '':
            self.name = self.names[idx]
            self.url = self.urls[idx]
            if idx == 0:
                self.name = self.names[idx]
                self.url = self.urls[idx]
                print('In playVideo url D=', self.url)
                self.play()
            elif idx == 1:
                print('In playVideo url B=', self.url)
                self.name = self.names[idx]
                self.url = self.urls[idx]
                try:
                    os.remove('/tmp/hls.avi')
                except:
                    pass
                header = ''
                cmd = 'python "/usr/lib/enigma2/python/Plugins/Extensions/tvDream/lib/hlsclient.py" "' + self.url + '" "1" "' + header + '" + &'
                print('In playVideo cmd =', cmd)
                os.system(cmd)
                os.system('sleep 3')
                self.url = '/tmp/hls.avi'
                self.play()
            elif idx == 2:
                print('In playVideo url A=', self.url)
                url = self.url
                try:
                    os.remove('/tmp/hls.avi')
                except:
                    pass

                cmd = 'python "/usr/lib/enigma2/python/Plugins/Extensions/tvDream/lib/tsclient.py" "' + url + '" "1" + &'
                print('ts cmd = ', cmd)
                os.system(cmd)
                os.system('sleep 3')
                self.url = '/tmp/hls.avi'
                self.name = self.names[idx]
                self.play()
            #preview
            elif idx == 3:
                self.name = self.names[idx]
                self.url = self.urls[idx]
                print('In playVideo url D=', self.url)
                self.play2()
            else:
                self.name = self.names[idx]
                self.url = self.urls[idx]
                print('In playVideo url D=', self.url)
                self.play()
            return
        else:
            return

    def playfile(self, serverint):
        self.serverList[serverint].play(self.session, self.url, self.name)

    def play(self):
        desc = ' '
        url = self.url
        name = self.name
        self.session.open(Playstream2, name, url)

    def play2(self):
        desc = ' '
        self['info'].setText(self.name)
        url = self.url
        url = url.replace(':', '%3a')
        print('In url =', url)
        ref = '4097:0:1:0:0:0:0:0:0:0:' + url
        sref = eServiceReference(ref)
        print('SREF: ', sref)
        sref.setName(self.name)
        self.session.nav.playService(sref)

    def cancel(self):
        self.session.nav.stopService()
        self.session.nav.playService(srefInit)
        self.close()

class Playstream2(
    InfoBarBase,
    InfoBarMenu,
    InfoBarSeek,
    InfoBarAudioSelection,
    InfoBarSubtitleSupport,
    InfoBarNotifications,
    TvInfoBarShowHide,
    Screen
):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 5000

    def __init__(self, session, name, url):
        global SREF, streaml
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.skinName = 'MoviePlayer'
        title = name
        streaml = False
        for x in InfoBarBase, \
                InfoBarMenu, \
                InfoBarSeek, \
                InfoBarAudioSelection, \
                InfoBarSubtitleSupport, \
                InfoBarNotifications, \
                TvInfoBarShowHide:
            x.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except:
            self.init_aspect = 0
        self.new_aspect = self.init_aspect
        self['actions'] = ActionMap(['MoviePlayerActions',
         'MovieSelectionActions',
         'MediaPlayerActions',
         'EPGSelectActions',
         'MediaPlayerSeekActions',
         'SetupActions',
         'ColorActions',
         'InfobarShowHideActions',
         'InfobarActions',
         'InfobarSeekActions'], {'stop': self.leavePlayer,
         'epg': self.showIMDB,
         'info': self.showinfo,
         # 'info': self.cicleStreamType,
         'tv': self.cicleStreamType,
         # 'stop': self.leavePlayer,
         'cancel': self.cancel,
         'back': self.cancel}, -1)
        self.allowPiP = False
        self.service = None
        service = None
        self.url = url
        self.pcip = 'None'
        self.name = decodeHtml(name)
        self.state = self.STATE_PLAYING
        SREF = self.session.nav.getCurrentlyPlayingServiceReference()
        if '8088' in str(self.url):
            # self.onLayoutFinish.append(self.slinkPlay)
            self.onFirstExecBegin.append(self.slinkPlay)
        else:
            # self.onLayoutFinish.append(self.cicleStreamType)
            self.onFirstExecBegin.append(self.cicleStreamType)
        self.onClose.append(self.cancel)

    def getAspect(self):
        return AVSwitch().getAspectRatioSetting()

    def getAspectString(self, aspectnum):
        return {0: _('4:3 Letterbox'),
         1: _('4:3 PanScan'),
         2: _('16:9'),
         3: _('16:9 always'),
         4: _('16:10 Letterbox'),
         5: _('16:10 PanScan'),
         6: _('16:9 Letterbox')}[aspectnum]

    def setAspect(self, aspect):
        map = {0: '4_3_letterbox',
         1: '4_3_panscan',
         2: '16_9',
         3: '16_9_always',
         4: '16_10_letterbox',
         5: '16_10_panscan',
         6: '16_9_letterbox'}
        config.av.aspectratio.setValue(map[aspect])
        try:
            AVSwitch().setAspectRatio(aspect)
        except:
            pass

    def av(self):
        temp = int(self.getAspect())
        temp = temp + 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)

    def showinfo(self):
        # debug = True
        sTitle = ''
        sServiceref = ''
        try:
            servicename, serviceurl = getserviceinfo(sref)
            if servicename != None:
                sTitle = servicename
            else:
                sTitle = ''
            if serviceurl != None:
                sServiceref = serviceurl
            else:
                sServiceref = ''
            currPlay = self.session.nav.getCurrentService()
            sTagCodec = currPlay.info().getInfoString(iServiceInformation.sTagCodec)
            sTagVideoCodec = currPlay.info().getInfoString(iServiceInformation.sTagVideoCodec)
            sTagAudioCodec = currPlay.info().getInfoString(iServiceInformation.sTagAudioCodec)
            message = 'stitle:' + str(sTitle) + '\n' + 'sServiceref:' + str(sServiceref) + '\n' + 'sTagCodec:' + str(sTagCodec) + '\n' + 'sTagVideoCodec:' + str(sTagVideoCodec) + '\n' + 'sTagAudioCodec : ' + str(sTagAudioCodec)
            self.mbox = self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        except:
            pass
        return

    def showIMDB(self):
        TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
        IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
        if os.path.exists(TMDB):
            from Plugins.Extensions.TMBD.plugin import TMBD
            text_clear = self.name
            text = charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif os.path.exists(IMDb):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = self.name
            text = charRemove(text_clear)
            HHHHH = text
            self.session.open(IMDB, HHHHH)

        else:
            text_clear = self.name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def slinkPlay(self, url):
        name = self.name
        ref = "{0}:{1}".format(url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openTest(self, servicetype, url):
        name = self.name
        ref = "{0}:0:0:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('reference:   ', ref)
        if streaml == True:
            url = 'http://127.0.0.1:8088/' + str(url)
            ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
            print('streaml reference:   ', ref)
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        global streml
        streaml = False
        from itertools import cycle, islice
        self.servicetype = '4097'
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        if str(os.path.splitext(self.url)[-1]) == ".m3u8":
            if self.servicetype == "1":
                self.servicetype = "4097"
        currentindex = 0
        streamtypelist = ["4097"]
        # if "youtube" in str(self.url):
            # self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
            # return
        if isStreamlinkAvailable():
            streamtypelist.append("5002")
            streaml = True
        if os.path.exists("/usr/bin/gstplayer"):
            streamtypelist.append("5001")
        if os.path.exists("/usr/bin/exteplayer3"):
            streamtypelist.append("5002")
        if os.path.exists("/usr/bin/apt-get"):
            streamtypelist.append("8193")
        for index, item in enumerate(streamtypelist, start=0):
            if str(item) == str(self.servicetype):
                currentindex = index
                break
        nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        self.servicetype = str(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openTest(self.servicetype, url)

    def up(self):
        pass

    def down(self):
        self.up()

    def doEofInternal(self, playing):
        self.close()

    def __evEOF(self):
        self.end = True

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback != None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def cancel(self):
        if os.path.isfile('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(SREF)
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except:
                pass
        streaml = False
        self.close()

    def leavePlayer(self):
        self.session.nav.stopService()
        self.session.nav.playService(srefInit)
        self.close()

def checks():
    from Plugins.Extensions.tvDream.Utils import checkInternet
    checkInternet()
    chekin= False
    if checkInternet():
        chekin = True
    return chekin

def main(session, **kwargs):
    if checks:
        try:
            from Plugins.Extensions.tvDream.Update import upd_done
            upd_done()
        except:
            pass
    session.open(MainSetting)

def Plugins(**kwargs):
    ico_path = 'logo.png'
    if not os.path.exists('/var/lib/dpkg/status'):
        ico_path = plugin_path + '/res/pics/logo.png'
    extensions_menu = PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = main, needsRestart = True)
    result = [PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_PLUGINMENU, icon = ico_path, fnc = main)]
    result.append(extensions_menu)
    return result


