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
import json
import six
	
# from Tools.LoadPixmap import LoadPixmap
# from lxml import html
global isDreamOS, regioni 
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

# try:
    # _create_unverified_http_context = ssl._create_unverified_context
# except AttributeError:
    # pass
# else:
    # ssl._create_default_http_context = _create_unverified_http_context
# def clear_Title(txt):
    # txt = re.sub('<.+?>', '', txt)
    # txt = txt.replace("&quot;", "\"").replace('()', '').replace("&#038;", "&").replace('&#8211;', ':')
    # txt = txt.replace("&amp;", "&").replace('&#8217;', "'").replace('&#039;', ':').replace('&#;', '\'')
    # txt = txt.replace("&#38;", "&").replace('&#8221;', '"').replace('&#8216;', '"').replace('&#160;', '')
    # txt = txt.replace('&#x27;', "'").replace("&#39;", "'").replace("&nbsp;", "").replace('&#8220;', '"').replace('\t', ' ').replace('\n', ' ')
    # # txt = txt.replace(":", "-").replace("&", "-").replace(" ", "-")
    # # txt = txt.replace("›", "-").replace(",", "-").replace("/", "-")
    
    # # txt = txt.decode('utf8').encode('latin-1','ignore')
    # return txt
    
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

try:
    from OpenSSL import SSL
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False

if sslverify:
    try:
        from urlparse import urlparse
    except:
        from urllib.parse import urlparse

    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx
            
UserAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
# MediapolisUserAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"

    
def getUrl(url):
    try:
        if url.startswith("https") and sslverify:
            parsed_uri = urlparse(url)
            domain = parsed_uri.hostname
            sniFactory = SNIFactory(domain)
        if PY3 == 3:
            url = url.encode()
                
        req = Request(url)
        # req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0')
        req.add_header('User-Agent', UserAgent)        
        response = urlopen(req)
        link = response.read()
        response.close()
        print("link =", link)
        return link
    except:
        e = URLError
        print('We failed to open "%s".' % url)
        if hasattr(e, 'code'):
            print('We failed with error code - %s.' % e.code)
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            

DESKHEIGHT = getDesktop(0).size().height()
currversion = '1.0'

plugin_path = os.path.dirname(sys.modules[__name__].__file__)
skin_path = plugin_path
pluglogo = plugin_path + '/res/pics/logo.png'
pngx = plugin_path + '/res/pics/plugins.png'
pngl = plugin_path + '/res/pics/plugin.png'
pngs = plugin_path + '/res/pics/setting.png'
b7 = 'aHR0cHM6Ly9mZWVkLmVudGVydGFpbm1lbnQudHYudGhlcGxhdGZvcm0uZXUvZi9QUjFHaEMvbWVkaWFzZXQtcHJvZC1hbGwtc3RhdGlvbnM='
host_b7 = base64.b64decode(b7)
HD = getDesktop(0).size()
vid = plugin_path + '/vid.txt'
desc_plugin = '..:: TiVu Dream Net Player by Lululla %s ::.. ' % currversion
name_plugin = 'TiVuDream Player'


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
        res.append(MultiContentEntryText(pos = (60, 0), size = (1000, 50), font = 1, text = name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT))
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
        res.append(MultiContentEntryText(pos = (60, 2), size = (1000, 50), font = 0, text = name, color = 0xa6d1fe, flags = RT_HALIGN_LEFT))
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
            url = "http://www.tvdream.net/web-tv/paesi/italia/"
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
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        '''
        on kids and film no work play
        '''
        
        self.names.append("Live") 
        self.urls.append("https://feed.entertainment.tv.theplatform.eu/f/PR1GhC/mediaset-prod-all-stations") 
        
        self.names.append("Film")
        self.urls.append("http://www.mediasetplay.mediaset.it/film")
        # self.urls.append("https://www.mediasetplay.mediaset.it/browse/film-della-settimana_e5ed8badba6f547001beae4d2")
        self.names.append("Kids")
        self.urls.append("http://www.mediasetplay.mediaset.it/kids")
        '''
        on kids and film no work play
        '''
        self.names.append("Documentari")
        self.urls.append("http://www.mediasetplay.mediaset.it/documentari") #ok
        self.names.append("Family")
        self.urls.append("http://www.mediasetplay.mediaset.it/family") #ok
        self.names.append("Fiction")
        self.urls.append("http://www.mediasetplay.mediaset.it/fiction") #ok
        self.names.append("Programmitv")
        self.urls.append("http://www.mediasetplay.mediaset.it/programmitv") #ok

        showlist(self.names, self['text'])
        self['info'].setText(_('Please select ...'))

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        
        if 'Live' in str(name):
            self.session.open(Mediaset1, name, url)            
        else:
            self.session.open(Mediaset2, name, url)

class Mediaset1(Screen):
    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
            self.timer_conn = self.timer.timeout.connect(self.search)
        else:
            self.timer.callback.append(self.search)
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)
        
    def search(self):
        content = getUrl(host_b7)
        content = six.ensure_str(content)
        print("content A =", content)
        self.names = []
        self.urls = []
        items = []
        d = json.loads(content)
        for i in d:
              k= i
              v= d[i]
              print("key =", k    )
              print("value=", v   )
              if k == "entries":
                      d1 = v
                      break
        print("\n\n##########")
        for a in d1:
              for i in a:
                     k= i
                     v= a[i]
                     print("key1 =", k    )
                     print("value1 =", v  )
                     if "title" in k:
                             self.names.append(str(v))
                     if k == "tuningInstruction":
                             v1 = str(v)
                             n1 = v1.find("publicUrls", 0)
                             n2 = v1.find("http", n1)
                             n3 = v1.find("'", n2)
                             url = v1[n2:n3]
                             self.urls.append(url)
        j = 0
        for name in self.names:
                url = self.urls[j]
                j = j+1
                pic = " "
                print("showContent name =", name)
                print("showContent url =", url)
        self.urls.append(url)
        self.names.append(name)
        showlist(self.names, self['text'])
      
    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(Playstream2, name, url)

class Mediaset2(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        datas = getUrl(url)
        datas = six.ensure_str(datas)
        self.names = []
        self.urls = []
        # icount = 0
        # start = 0
        # n1 = datas.find(' <body>', 0)
        # # if n1 < 0:
           # # return
        # n2 = datas.find("</script>", n1)
        # datas = datas[n1:n2]
        # print("data A2 =", datas)

        if "fiction" in url:
            regexcat = 'a href="/fiction/(.*?)".*?class="_2_UgV">(.*?)</p'      #ok
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            # print ("_gotPageLoad match =", match)
            for url , name in match:
                pic = " "
                name = decodeHtml(name)
                url = "http://www.mediasetplay.mediaset.it/fiction/" + url
                '''
                http://www.mediasetplay.mediaset.it/programmi-tv/alltogethernow_b100003640
                '''
                # print('name : ', name)
                # print('url:  ', url)
                if not url in self.urls:
                    self.urls.append(url)
                    self.names.append(name)

            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])

        elif "family" in url:
            regexcat = 'href="/movie/(.*?)".*?class="_1ovAG">(.*?)</h3'    #ok
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            # print ("_gotPageLoad match =", match)
            for url, name in match:
                pic = " "
                name = decodeHtml(name)
                url = "http://www.mediasetplay.mediaset.it/movie/" + url
                '''
                http://www.mediasetplay.mediaset.it/browse/film-per-tutta-la-famiglia_e5e6a15c523eec6001de37eac
                '''
                # print('name : ', name)
                # print('url:  ', url)
                if not url in self.urls:
                    self.urls.append(url)
                    self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])

        elif "programmi" in url:
            regexcat = 'a href="/programmi-tv/(.*?)".*?class="_2_UgV">(.*?)</p'    #ok
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            # print ("_gotPageLoad match =", match)
            for url , name in match:
                pic = " "
                name = decodeHtml(name)
                url = "http://www.mediasetplay.mediaset.it/programmi-tv/" + url
                '''
                http://www.mediasetplay.mediaset.it/programmi-tv/alltogethernow_b100003640
                '''
                # print('name : ', name)
                # print('url:  ', url)
                if not url in self.urls:
                    self.urls.append(url)
                    self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])

        elif "documentari" in url:
            regexcat = 'href="/playlist/(.*?)">.*?class="P4EQe _1ovAG">(.*?)</h4'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            # print ("_gotPageLoad match =", match)
            for url, name in match:
                pic = " "
                name = decodeHtml(name)
                url = "http://www.mediasetplay.mediaset.it/playlist/" + url
                # print('name : ', name)
                # print('url:  ', url)
                if not url in self.urls:
                    self.urls.append(url)
                    self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])

        elif "film" in url:
            regexcat = 'a href="/movie/(.*?)".*?class="_2_UgV">(.*?)</p'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            # print ("_gotPageLoad match =", match)
            for url, name in match:
                pic = " "
                name = decodeHtml(name)                
                url = "http://www.mediasetplay.mediaset.it/movie/" + url
                '''
                http://www.mediasetplay.mediaset.it/programmi-tv/alltogethernow_b100003640
                '''
                # print('name : ', name)
                # print('url:  ', url)
                if not url in self.urls:
                    self.urls.append(url)
                    self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])

        elif "kids" in url:
            regexcat = 'href="/video/(.*?)".*?class="_2s7uR"><span>(.*?)</span'      #ok
            #https://www.mediasetplay.mediaset.it/video/tomjerryshow/il-topo-mascherato_F310175801005201
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            # print ("kids _gotPageLoad match =", match)
            for url, name in match:
                pic = " "
                name = name.replace("&#x27;","'").replace("&amp;","&")
                name = name.replace('&quot;','"').replace('&#39;',"'")
                url = "http://www.mediasetplay.mediaset.it/video/" + url
                '''
                http://www.mediasetplay.mediaset.it/kids
                '''
                # print('name : ', name)
                # print('url:  ', url)
                if not url in self.urls:
                    self.urls.append(url)
                    self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        else:
             pass

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        try:        
            if ("movie" in url) or ("video" in url):
                # print("In playVideo2 url =", url)
                from youtube_dl import YoutubeDL
                '''
                ydl_opts = {'format': 'best'}
                ydl_opts = {'format': 'bestaudio/best'}
                '''
                ydl_opts = {'format': 'best'}
                ydl = YoutubeDL(ydl_opts)
                ydl.add_default_info_extractors()
                result = ydl.extract_info(url, download=False)
                # print ("mediaset result =", result)
                url = result["url"]
                # print ("mediaset final url =", url)
                self.session.open(Playstream2, name, url)
            else:
                self.session.open(Mediaset3, name, url)
        except:
            return                
                

class Mediaset3(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        datas = getUrl(url)
        datas = six.ensure_str(datas)
        # print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            regexcat = 'href="/video/(.*?)".*?class="_1ovAG">(.*?)</h4>'
            if ("playlist" in url):
                regexcat = 'url":.*?"https://www.mediasetplay.mediaset.it/video/(.*?)".*?"name": "(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            # print ("_gotPageLoad match =", match)
            for url, name  in match:
                pic = " "
                name = decodeHtml(name)
                url = "http://www.mediasetplay.mediaset.it/video/" + url
                # print('name : ', name)
                # print('url1:  ', url)
                if not url in self.urls:
                    self.urls.append(url)
                    self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing Dok...'))
            pass

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        try:
            # print("In playVideo2 url =", url)
            from youtube_dl import YoutubeDL
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
        except:
            self['info'].setText(_('Nothing KO ...'))
            pass

'''not used'''
class Mediaset4(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        datas = getUrl(url)
        datas = six.ensure_str(datas)
        # print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            #https://vod05.msf.cdn.mediaset.net/farmunica/2020/01/527829_16f8582f2437d2/dashrcclean/hd_no_mpl.mpd
            regexcat = 'url":.*?"https://www.mediasetplay.mediaset.it/video/(.*?)".*?"name": "(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(datas)
            # print ("_gotPageLoad match docs=", match)
            for url, name  in match:
                pic = " "
                name = decodeHtml(name)
                url = "https://www.mediasetplay.mediaset.it/video/" + url
                # print('name : ', name)
                # print('url1:  ', url)
                if not url in self.urls:
                    self.urls.append(url)
                    self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing ...'))
            pass

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        try:
            # print("In playVideo2 url =", url)
            from youtube_dl import YoutubeDL
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
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        self.names.append("Film")
        self.urls.append("http://www.raiplay.it/film/")
        self.names.append("Serietv")
        self.urls.append("http://www.raiplay.it/serietv/")
        self.names.append("Fiction")
        self.urls.append("http://www.raiplay.it/fiction/")
        self.names.append("Documentari")
        self.urls.append("http://www.raiplay.it/documentari/")
        self.names.append("Bambini")
        self.urls.append("http://www.raiplay.it/bambini/")
        self.names.append("Teen")
        self.urls.append("http://www.raiplay.it/teen/")
        self.names.append("Tgr")
        self.urls.append("http://www.tgr.rai.it/dl/tgr/mhp/home.xml")
        showlist(self.names, self['text'])

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
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
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        content = getUrl(url)
        content = six.ensure_str(content)
        # items = []
        self.names = []
        self.urls = []
        pic = " "
        regexcat = 'data-video-json="(.*?)".*?<img alt="(.*?)"'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        # print("showContent2 match =", match)
        # print('name : ', name)
        for url, name in match:
            try:
                # if 'raiplay' in url.lower():
                    url1 = "http://www.raiplay.it" + url
                    content2 = getUrl(url1)
                    content2 = six.ensure_str(content2)
                    # print ("showContent321 content2 =", content2)
                    regexcat2 = '"/video/(.*?)"'
                    match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                    # print ("showContent321 match2 =", match2)
                    url2 = match2[0].replace("json", "html")
                    url3 = "http://www.raiplay.it/video/" + url2
                    name = decodeHtml(name)
                    # name = name.replace("&#x27;","'").replace("&amp;","&")
                    # name = name.replace('&quot;','"').replace('&#39;',"'")
                    # item = name + "###" + url3
                    # items.append(item)
                # items.sort()
                # for item in items:
                    # name = item.split("###")[0]
                    # url3 = item.split("###")[1]
                    self.names.append(name)
                    self.urls.append(url3)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('nameok : ', name)
        # print('urlok:  ', url)
        try:
            # print("In playVideo2 url =", url)
            from youtube_dl import YoutubeDL
            ydl_opts = {'format': 'best'}
            '''
            ydl_opts = {'format': 'bestaudio/best'}
            '''
            ydl = YoutubeDL(ydl_opts)
            ydl.add_default_info_extractors()
            result = ydl.extract_info(url, download=False)
            # print ("rai result =", result)
            url = result["url"]
            # print ("rai final url =", url)
            self.session.open(Playstream2, name, url)
        except:
            self['info'].setText(_('Nothing ...'))
            pass

class tgrRai(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
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
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        self.session.open(tgrRai2, name, url)

class tgrRai2(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
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
        data = six.ensure_str(data)
        content = data.replace("\r", "").replace("\t", "").replace("\n", "")
        name = self.name
        self.names = []
        self.urls = []
        self.pics = []
        pic = " "
        try:
            if 'type="video">' in content:
                # print('content1 : ', content)
                regexcat = '<label>(.*?)</label>.*?type="video">(.*?)</url>' #relinker
                self["key_green"].setText('Play')
            elif 'type="list">' in content:
                # print('content2 : ', content)
                regexcat = '<label>(.*?)</label>.*?type="list">(.*?)</url>'
            else:
                print('passsss')
                pass
            match = re.compile(regexcat, re.DOTALL).findall(content)
            # print("showContent2 match =", match)
            # print('name : ', name)
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
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
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
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
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
        data = six.ensure_str(data)
        content = data.replace("\r", "").replace("\t", "").replace("\n", "")
        name = self.name
        self.names = []
        self.urls = []
        self.pics = []
        pic = " "
        try:
            if 'type="video">' in content:
                # print('content10 : ', content)
                regexcat = '<label>(.*?)</label>.*?type="video">(.*?)</url>' #relinker
                self["key_green"].setText('Play')

            elif 'type="list">' in content:
                # print('content20 : ', content)
                regexcat = '<label>(.*?)</label>.*?type="list">(.*?)</url>'
            else:
                print('passsss')
                pass
            match = re.compile(regexcat, re.DOTALL).findall(content)
            # print("showContent21 match =", match)
            for name, url in match:
                # print('name : ', name)
                # print('url : ', url)
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
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        try:
            # print("In playVideo2 url =", url)
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
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        self.names.append("Programmi")
        self.urls.append("http://www.la7.it/programmi")
        self.names.append("Teche")
        self.urls.append("http://www.la7.it/i-protagonisti")
        showlist(self.names, self['text'])

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        self.session.open(tvLa2, name, url)

class tvLa2(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        content = getUrl(url)
        content = six.ensure_str(content)
        self.names = []
        self.urls = []
        self.pics = []
        pic = " "
        regexcat = '"list-item list-item-.*?a href="(.*?)".*?data-background-image="(.*?)".*?class="titolo">(.*?)<'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        # print("showContent2 match =", match)
        # print('name : ', name)
        for url, pic, name in match:
            try:
                url1 = "http://www.la7.it" + url
                name = decodeHtml(name)
                pic1 = "http:" + pic
                self.names.append(name)
                self.urls.append(url1)
                self.pics.append(pic1)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):

        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        self.session.open(tvLa3, name, url)

class tvLa3(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        content = getUrl(url)
        content = six.ensure_str(content)
        self.names = []
        self.urls = []
        self.pics = []
        pic = " "
        if 'protagonisti' in url:
            regexcat = '<div class="list.*?a href="/(.*?)/video(.*?)".*?data-background-image="(.*?)".*?class="title">(.*?)<'
        else:
            regexcat = '</div><div class="item.*?a href="/(.*?)/video(.*?)".*?data-background-image="(.*?)".*?class="title">(.*?)</'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        # print("showContent2 match =", match)
        # print('name : ', name)
        for url1, url2, pic, name in match:
            try:
                url3 = "http://www.la7.it/" + url1 + "/video" + url2
                # print("showContent341 url3 =", url3)
                pic1 = "http:" + pic
                name = decodeHtml(name)
                self.names.append(name)
                self.urls.append(url3)
                self.pics.append(pic1)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('tvLa3 name : ', name)
        # print('tvLa3 url:  ', url)
        regex2 = '/content/(.*?).mp4'
        regex3 = 'm3u8: "(.*?)"'
        content2 = getUrl(url)
        content2 = six.ensure_str(content2)
        # print('tvLa3 content2:  ', content2)
        x1 = 0
        if x1 == 0:
            if re.findall(regex2, content2):
                 link_video = 'http://awsvodpkg.iltrovatore.it/local/hls/,/content/'+re.findall(regex2, content2)[0]+'.mp4.urlset/master.m3u8'
                 # print('tvLa3 link_video:  ', link_video)
            elif re.findall(regex3, content2):
                 link_video = re.findall(regex3, content2)[0]
                 # print('tvLa3 link_video 2:  ', link_video)
            # print('tvLa3 link_video 3:  ', link_video)
            self.session.open(Playstream2, name, link_video)

class Dplay(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)


    def _gotPageLoad(self):
        # url = "http://it.dplay.com/generi/"
        url = "http://www.discoveryplus.it/generi/"
        content = getUrl(url)
        content = six.ensure_str(content)
        # print("showContent35 content =", content)
        self.names = []
        self.urls = []
        regexcat = 'a href="/genere/(.*?)"'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        # print("showContent2 match =", match)
        for url in match:
            try:
                # url1 = "http://it.dplay.com/genere/" + url
                url1 = "http://www.discoveryplus.it/generi" + url
                name = url
                self.names.append(name)
                self.urls.append(url1)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        self.session.open(Dplay2, name, url)

class Dplay2(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        content = getUrl(url)
        content = six.ensure_str(content)
        self.names = []
        self.urls = []
        self.pics = []
        pic = " "
        regexcat = '<div class="b-show-list__single-show">.*?<a href="(.*?)".*?lazy-src="(.*?)".*?alt="(.*?)"'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        # print("showContent2 match =", match)
        for url, pic, name in match:
            try:
                # url1 = "http://it.dplay.com" + url
                url1 = "http://www.discoveryplus.it" + url
                name = decodeHtml(name)
                # name = name.replace("&#x27;","'").replace("&amp;","&").replace('&quot;','"').replace('&#39;',"'")
                self.names.append(name)
                self.urls.append(url1)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        self.session.open(Dplay3, name, url)

class Dplay3(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        content = getUrl(url)
        content = six.ensure_str(content)
        self.names = []
        self.urls = []
        pic = " "
        regexcat = 'div class="carousel-cell.*?<a href="(.*?)".*?lazyload="(.*?)".*?alt="(.*?)"'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        # print("showContent2 match =", match)
        # print('name : ', name)
        for url, pic, name in match:
            try:
                # url1 = "http://it.dplay.com" + url
                url1 = "http://www.discoveryplus.it" + url
                name = decodeHtml(name)
                # name = name.replace("&#x27;","'").replace("&amp;","&").replace('&quot;','"').replace('&#39;',"'")
                self.names.append(name)
                self.urls.append(url1)
            except:
                continue
        self['info'].setText(_('Please select ...'))
        showlist(self.names, self['text'])

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        try:
            # print("In playVideo2 url =", url)
            from youtube_dl import YoutubeDL
            '''
            ydl_opts = {'format': 'best'}
            '''
            ydl_opts = {'format': 'bestaudio/best'}
            ydl = YoutubeDL(ydl_opts)
            ydl.add_default_info_extractors()
            result = ydl.extract_info(url, download=False)
            # print ("rai result =", result)
            url = result["url"]
            # print ("rai final url =", url)
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
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = 'http://www.tvdream.net/web-tv/paesi/'
        datas = getUrl(url)
        datas = six.ensure_str(datas)
        # print('datas :  ', datas)
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
            # print("data A2 =", data2)
            pic = " "
            regexcat = 'href="(.*?)">(.*?)<'
            match = re.compile(regexcat, re.DOTALL).findall(data2)
            for url, name in match:
                # print('name : ', name)
                # print('url:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing ...'))
            pass

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        self.session.open(tvItalia, name, url)

class tvRegioni(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = 'http://www.tvdream.net/web-tv/regioni/'
        datas = getUrl(url)
        datas = six.ensure_str(datas)
        # print('datas :  ', datas)
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
            # print("data A2 =", data2)
            pic = " "
            regexcat = 'href="(.*?)">(.*?)<'
            match = re.compile(regexcat, re.DOTALL).findall(data2)
            for url, name in match:
                # print('name : ', name)
                # print('url:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing ...'))
            pass

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        # print('name : ', name)
        # print('url:  ', url)
        self.session.open(tvItalia, name, url)

class tvItalia(Screen):

    def __init__(self, session, name, url ):
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        name = self.name
        url = self.url
        datas = getUrl(url)
        datas =six.ensure_str(datas)
        # print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            pages = [1, 2 ]
            for page in pages:
                url1 = url + "page/" + str(page) + "/"
                name = "Page " + str(page)
                # print('name it : ', name)
                # print('url it:  ', url1)
                self.urls.append(url1)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            pass

    def okRun(self):
        try:
            idx = self["text"].getSelectionIndex()
            name = self.names[idx]
            url = self.urls[idx]
            # print('name it3: ', name)
            # print('url it3: ', url)
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
        self.setTitle(desc_plugin)
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
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        datas = getUrl(url)
        datas = six.ensure_str(datas)
        # print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            icount = 0
            start = 0
            data2 = datas
            # print("data A5 =", data2)
            pic = " "
            regexcat = '<div class="item-head.*?href="(.*?)".*?bookmark">(.*?)<'
            '''
            regexcat   = '<div class="item-head.*?a href="(.*?)".*?bookmark">(.*?)<'
            '''
            match = re.compile(regexcat, re.DOTALL).findall(data2)
            for url, name in match:
                # print('name ch1: ', name)
                # print('url ch1:  ', url)
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing ...'))
            pass

    def okRun(self):
        try:
            idx = self["text"].getSelectionIndex()
            name = self.names[idx]
            url = self.urls[idx]
            content = getUrl(url)
            content = six.ensure_str(content)
            # print('content :  ', content)
            regexcat = '"player".*?href="(.*?)"'
            if regioni == True:
                regexcat = '<iframe src="(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            # print("getVideos2 match =", match)
            url2 = match[0]
            content2 = getUrl(url2)
            content2 = six.ensure_str(content2)
            # print("getVideos2 content2 =", content2)
            if ("rai" in url.lower()) or ("rai" in name.lower()):
                regexcat2 = 'liveVideo":{"mediaUrl":"(.*?)"'
                match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
                url = match2[0]
                pic = ""
                self.session.open(Playstream2, name, url)
            else:
                n1 = content2.find(".m3u8")
                n2 = content2.rfind("http", 0, n1)
                url = content2[n2:(n1+5)]
                pic = ""
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
        name = decodeHtml(name)
        # name = name.replace(":", "-").replace("&", "-").replace(" ", "-")
        # name = name.replace("›", "-").replace(",", "-").replace("/", "-")
        if url is not None:
            url = str(url)
            url = url.replace(":", "%3a")
            url = url.replace("\\", "/")
            ref = "4097:0:1:0:0:0:0:0:0:0:" + url
            sref = eServiceReference(ref)
            sref.setName(self.name)
            self.session.nav.stopService()
            self.session.nav.playService(sref)
        else:
           return

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
    # main_menu = PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_MENU, fnc = StartSetup, needsRestart = True)
    extensions_menu = PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = main, needsRestart = True)
    result = [PluginDescriptor(name = name_plugin, description = desc_plugin, where = PluginDescriptor.WHERE_PLUGINMENU, icon = ico_path, fnc = main)]
    result.append(extensions_menu)
    # result.append(main_menu)
    return result


def decodeUrl(text):
	text = text.replace('%20',' ')
	text = text.replace('%21','!')
	text = text.replace('%22','"')
	text = text.replace('%23','&')
	text = text.replace('%24','$')
	text = text.replace('%25','%')
	text = text.replace('%26','&')
	text = text.replace('%2B','+')
	text = text.replace('%2F','/')
	text = text.replace('%3A',':')
	text = text.replace('%3B',';')
	text = text.replace('%3D','=')
	text = text.replace('&#x3D;','=')
	text = text.replace('%3F','?')
	text = text.replace('%40','@')
	return text

def decodeHtml(text):
	text = text.replace('&auml;','ä')
	text = text.replace('\u00e4','ä')
	text = text.replace('&#228;','ä')
	text = text.replace('&oacute;','ó')
	text = text.replace('&eacute;','e')
	text = text.replace('&aacute;','a')
	text = text.replace('&ntilde;','n')

	text = text.replace('&Auml;','Ä')
	text = text.replace('\u00c4','Ä')
	text = text.replace('&#196;','Ä')
	
	text = text.replace('&ouml;','ö')
	text = text.replace('\u00f6','ö')
	text = text.replace('&#246;','ö')
	
	text = text.replace('&ouml;','Ö')
	text = text.replace('\u00d6','Ö')
	text = text.replace('&#214;','Ö')
	
	text = text.replace('&uuml;','ü')
	text = text.replace('\u00fc','ü')
	text = text.replace('&#252;','ü')
	
	text = text.replace('&Uuml;','Ü')
	text = text.replace('\u00dc','Ü')
	text = text.replace('&#220;','Ü')
	
	text = text.replace('&szlig;','ß')
	text = text.replace('\u00df','ß')
	text = text.replace('&#223;','ß')
	
	text = text.replace('&amp;','&')
	text = text.replace('&quot;','\"')
	text = text.replace('&quot_','\"')

	text = text.replace('&gt;','>')
	text = text.replace('&apos;',"'")
	text = text.replace('&acute;','\'')
	text = text.replace('&ndash;','-')
	text = text.replace('&bdquo;','"')
	text = text.replace('&rdquo;','"')
	text = text.replace('&ldquo;','"')
	text = text.replace('&lsquo;','\'')
	text = text.replace('&rsquo;','\'')
	text = text.replace('&#034;','\'')
	text = text.replace('&#038;','&')
	text = text.replace('&#039;','\'')
	text = text.replace('&#39;','\'')
	text = text.replace('&#160;',' ')
	text = text.replace('\u00a0',' ')
	text = text.replace('&#174;','')
	text = text.replace('&#225;','a')
	text = text.replace('&#233;','e')
	text = text.replace('&#243;','o')
	text = text.replace('&#8211;',"-")
	text = text.replace('\u2013',"-")
	text = text.replace('&#8216;',"'")
	text = text.replace('&#8217;',"'")
	text = text.replace('#8217;',"'")
	text = text.replace('&#8220;',"'")
	text = text.replace('&#8221;','"')
	text = text.replace('&#8222;',',')
	text = text.replace('&#x27;',"'")
	text = text.replace('&#8230;','...')
	text = text.replace('\u2026','...')
	text = text.replace('&#41;',')')
	text = text.replace('&lowbar;','_')
	text = text.replace('&rsquo;','\'')
	text = text.replace('&lpar;','(')
	text = text.replace('&rpar;',')')
	text = text.replace('&comma;',',')
	text = text.replace('&period;','.')
	text = text.replace('&plus;','+')
	text = text.replace('&num;','#')
	text = text.replace('&excl;','!')
	text = text.replace('&#039','\'')
	text = text.replace('&semi;','')
	text = text.replace('&lbrack;','[')
	text = text.replace('&rsqb;',']')
	text = text.replace('&nbsp;','')
	text = text.replace('&#133;','')
	text = text.replace('&#4','')
	text = text.replace('&#40;','')

	text = text.replace('&atilde;',"'")
	text = text.replace('&colon;',':')
	text = text.replace('&sol;','/')
	text = text.replace('&percnt;','%')
	text = text.replace('&commmat;',' ')
	text = text.replace('&#58;',':')

	return text	
