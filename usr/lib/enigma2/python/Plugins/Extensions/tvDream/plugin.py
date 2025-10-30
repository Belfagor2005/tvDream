#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             15/09/2023               *
*       Skin by MMark                  *
****************************************
#--------------------#
#Info http://t.me/tivustream
'''
from __future__ import print_function
from . import _
from . import Utils
from . import html_conv
from .Console import Console as xConsole

from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import (MultiContentEntryPixmapAlphaTest, MultiContentEntryText)
from Components.ServiceEventTracker import (ServiceEventTracker, InfoBarBase)
from Components.config import config
from Plugins.Plugin import PluginDescriptor
from Screens.InfoBarGenerics import (
    InfoBarSubtitleSupport,
    InfoBarSeek,
    InfoBarAudioSelection,
    InfoBarMenu,
    InfoBarNotifications,
)
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import (SCOPE_PLUGINS, resolveFilename)
from enigma import (
    RT_VALIGN_CENTER,
    RT_HALIGN_LEFT,
    eTimer,
    eListboxPythonMultiContent,
    eServiceReference,
    iPlayableService,
    gFont,
    loadPNG,
)
from datetime import datetime
import codecs
import os
import re
import six
import ssl
import sys
import json

global regioni, skin_dream
regioni = False
PY3 = False
PY3 = sys.version_info.major >= 3
print('Py3: ', PY3)

if PY3:
    from urllib.request import urlopen
    PY3 = True
else:
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

currversion = '1.3'
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/tvDream'
desc_plugin = '..:: TiVu Dream Player by Lululla %s ::.. ' % currversion
name_plugin = 'TiVuDream Player'
twxtv = 'aHR0cH+M6Ly9+wYXRidXdlY+i5oZXJva3V+hcHAuY29tL2Fw+aS9wbGF5+P3VybD0='

installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS90dkRyZWFtL21haW4vaW5zdGFsbGVyLnNo'
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvdHZEcmVhbQ=='

skin_dream = os.path.join(plugin_path, 'res/skins/hd')
if Utils.isFHD():
    skin_dream = os.path.join(plugin_path, 'res/skins/fhd')
if os.path.exists('/var/lib/dpkg/info'):
    skin_dream = os.path.join(skin_dream, 'dreamOs')


Panel_Dlist = [('TVD Regions'), ('TVD State'), ('TVD Italia'), ('TVD Category'), ('TVD New')]


class SetList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if Utils.isFHD():
            self.l.setItemHeight(50)
            textfont = int(30)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(30)
            textfont = int(24)
            self.l.setFont(0, gFont('Regular', textfont))


def DListEntry(name, idx=None):
    res = [name]
    pngs = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/setting.png".format('tvDream'))
    if Utils.isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(40, 40), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(70, 0), size=(1000, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(3, 3), size=(30, 30), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(50, 0), size=(500, 30), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


def showlist(datal, list):
    plist = []
    for name in datal:  # Iterazione più pythonica
        plist.append(DListEntry(name))
    list.setList(plist)


"""
def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(DListEntry(name, icount))
        icount += 1
        list.setList(plist)
"""


def returnIMDB(text_clear):
    TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
    tmdb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('tmdb'))
    IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
    text = html_conv.html_unescape(text_clear)
    if os.path.exists(TMDB):
        try:
            from Plugins.Extensions.TMBD.plugin import TMBD
            _session.open(TMBD.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] Tmdb: ", str(e))
        return True

    elif os.path.exists(tmdb):
        try:
            from Plugins.Extensions.tmdb.plugin import tmdb
            _session.open(tmdb.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] Tmdb: ", str(e))
        return True

    elif os.path.exists(IMDb):
        try:
            from Plugins.Extensions.IMDb.plugin import main as imdb
            imdb(_session, text)
        except Exception as e:
            print("[XCF] imdb: ", str(e))
        return True
    else:
        _session.open(MessageBox, text, MessageBox.TYPE_INFO)
        return True
    return False


class MainSetting(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_dream, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('MainSetting')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self['text'] = SetList([])
        self.selection = 'all'
        self['title'] = Label(desc_plugin)
        self['info'] = Label('')
        self['info'].setText(_('Please select ...'))
        self['key_yellow'] = Button(_('Update'))
        # self['key_yellow'].hide()
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Exit'))
        self['key_green'].hide()
        self.Update = False
        self['actions'] = ActionMap(['OkCancelActions',
                                     'HotkeyActions',
                                     'InfobarEPGActions',
                                     'ChannelSelectBaseActions',
                                     'DirectionActions'], {'ok': self.okRun,
                                                           'yellow': self.update_me,  # update_me,
                                                           'yellow_long': self.update_dev,
                                                           'info_long': self.update_dev,
                                                           'infolong': self.update_dev,
                                                           'showEventInfoPlugin': self.update_dev,
                                                           'green': self.okRun,
                                                           'cancel': self.closerm,
                                                           'red': self.closerm}, -1)

        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self.check_vers)
        else:
            self.timer.callback.append(self.check_vers)
        self.timer.start(500, 1)
        self.onLayoutFinish.append(self.updateMenuList)

    def check_vers(self):
        remote_version = '0.0'
        remote_changelog = ''
        req = Utils.Request(Utils.b64decoder(installer_url), headers={'User-Agent': 'Mozilla/5.0'})
        page = Utils.urlopen(req).read()
        if PY3:
            data = page.decode("utf-8")
        else:
            data = page.encode("utf-8")
        if data:
            lines = data.split("\n")
            for line in lines:
                if line.startswith("version"):
                    remote_version = line.split("=")
                    remote_version = line.split("'")[1]
                if line.startswith("changelog"):
                    remote_changelog = line.split("=")
                    remote_changelog = line.split("'")[1]
                    break
        self.new_version = remote_version
        self.new_changelog = remote_changelog
        # if currversion < remote_version:
        if float(currversion) < float(remote_version):
            self.Update = True
            # self['key_yellow'].show()
            # self['key_green'].show()
            self.session.open(MessageBox, _('New version %s is available\n\nChangelog: %s\n\nPress info_long or yellow_long button to start force updating.') % (self.new_version, self.new_changelog), MessageBox.TYPE_INFO, timeout=5)
        # self.update_me()

    def update_me(self):
        if self.Update is True:
            self.session.openWithCallback(self.install_update, MessageBox, _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?") % (self.new_version, self.new_changelog), MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox, _("Congrats! You already have the latest version..."),  MessageBox.TYPE_INFO, timeout=4)

    def update_dev(self):
        try:
            req = Utils.Request(Utils.b64decoder(developer_url), headers={'User-Agent': 'Mozilla/5.0'})
            page = Utils.urlopen(req).read()
            data = json.loads(page)
            remote_date = data['pushed_at']
            strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
            remote_date = strp_remote_date.strftime('%Y-%m-%d')
            self.session.openWithCallback(self.install_update, MessageBox, _("Do you want to install update ( %s ) now?") % (remote_date), MessageBox.TYPE_YESNO)
        except Exception as e:
            print('error xcons:', e)

    def install_update(self, answer=False):
        if answer:
            cmd1 = 'wget -q "--no-check-certificate" ' + Utils.b64decoder(installer_url) + ' -O - | /bin/sh'
            self.session.open(xConsole, 'Upgrading...', cmdlist=[cmd1], finishedCallback=self.myCallback, closeOnSuccess=False)
        else:
            self.session.open(MessageBox, _("Update Aborted!"),  MessageBox.TYPE_INFO, timeout=3)

    def myCallback(self, result=None):
        print('result:', result)
        return

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
        self['key_green'].show()
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
        skin = os.path.join(skin_dream, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['text'] = SetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_green'].hide()
        self['key_yellow'] = Button()
        self['key_yellow'].hide()
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(500, True)
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions'], {'ok': self.okRun,
                                                           'green': self.okRun,
                                                           'red': self.exit,
                                                           'cancel': self.exit}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        url = 'http://www.tvdream.net/web-tv/paesi/'
        if Utils.check(url):
            datas = Utils.getUrl(url)
            if PY3:
                datas = six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                n1 = datas.find('menu-sub">', 0)
                if n1 < 0:
                    return
                n2 = datas.find("</ul>", n1)
                data2 = datas[n1:n2]
                # print("data A2 =", data2)
                regexcat = 'href="(.*?)">(.*?)<'
                match = re.compile(regexcat, re.DOTALL).findall(data2)
                for url, name in match:
                    print('name : ', name)
                    print('url:  ', url)
                    self.urls.append(url)
                    self.names.append(html_conv.html_unescape(name))
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout=5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(tvItalia, name, url)

    def exit(self):
        Utils.deletetmp()
        self.close()


class tvRegioni(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_dream, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['text'] = SetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_green'].hide()
        self['key_yellow'] = Button()
        self['key_yellow'].hide()
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(500, True)
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions'], {'green': self.okRun,
                                                           'red': self.close,
                                                           'ok': self.okRun,
                                                           'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        url = 'http://www.tvdream.net/web-tv/regioni/'
        if Utils.check(url):
            datas = Utils.getUrl(url)
            if PY3:
                datas = six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                n1 = datas.find('menu-sub">', 0)
                if n1 < 0:
                    return
                n2 = datas.find("</ul>", n1)
                data2 = datas[n1:n2]
                # print("data A2 =", data2)
                regexcat = 'href="(.*?)">(.*?)<'
                match = re.compile(regexcat, re.DOTALL).findall(data2)
                for url, name in match:
                    print('name : ', name)
                    print('url:  ', url)
                    if 'Logo di TVdream' in name:
                        continue
                    self.urls.append(url)
                    self.names.append(html_conv.html_unescape(name))
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout=5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(tvItalia, name, url)


class tvItalia(Screen):
    def __init__(self, session, name, url):
        self.session = session
        skin = os.path.join(skin_dream, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self.name = name
        self.url = url
        self['text'] = SetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_green'].hide()
        self['key_yellow'] = Button()
        self['key_yellow'].hide()
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(500, True)
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions'], {'green': self.okRun,
                                                           'red': self.close,
                                                           'ok': self.okRun,
                                                           'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        name = self.name
        url = self.url
        if Utils.check(url):
            datas = Utils.getUrl(url)
            if PY3:
                datas = six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
                for page in pages:
                    url1 = url + "page/" + str(page) + "/"
                    name = "Page " + str(page)
                    print('name it : ', name)
                    print('url it:  ', url1)
                    self.urls.append(url1)
                    self.names.append(html_conv.html_unescape(name))
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout=5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(tvCanal, name, url)


class tvCanal(Screen):
    def __init__(self, session, name, url):
        self.session = session
        skin = os.path.join(skin_dream, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self.name = name
        self.url = url
        self['text'] = SetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_green'].hide()
        self['key_yellow'] = Button()
        self['key_yellow'].hide()
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(500, True)
        self['title'] = Label(desc_plugin)
        global SREF
        SREF = self.session.nav.getCurrentlyPlayingServiceReference()
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions'], {'green': self.okRun,
                                                           'red': self.close,
                                                           'ok': self.okRun,
                                                           'cancel': self.close}, -2)

    def _gotPageLoad(self):
        url = self.url
        name = self.name
        datas = Utils.getUrl(url)
        # print('datas :  ', datas)
        self.names = []
        self.urls = []
        try:
            data2 = datas
            # print("data A5 =", data2)
            regexcat = '<div class="item__thumb.*?href="(.*?)".*?alt="(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(data2)
            for url, name in match:
                # print('name ch1: ', name)
                # print('url ch1:  ', url)
                if 'Logo di TVdream' in name:
                    continue
                self.urls.append(url)
                self.names.append(html_conv.html_unescape(name))
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['text'])
        except:
            self['info'].setText(_('Nothing ... Retry'))

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print('name okRun: ', name)
        print('url okRun:  ', url)
        if Utils.check(url):
            content = Utils.getUrl(url)
            if PY3:
                content = six.ensure_str(content)
            print('content okRun ====================:  ', content)
            try:
                regexcat = 'item__.*?href="(.*?)"'

                if regioni is True:
                    regexcat = '<iframe src="(.*?)"'
                    print('iframe src=')
                else:
                    regexcat = 'item__.*?href="(.*?)"'
                    print('item__.*?href=')
                if '"btn-site"' in content:
                    print('content btn-site')
                    regexcat = '"btn-site".*?href="(.*?)"'

                if 'player-ext" href="' in content:
                    print('content player-ex')
                    regexcat = '"btn-site".*?href="(.*?)"'

                if 'player-video"' in content:
                    print('content player-video')
                    if content.find('iframe src='):
                        regexcat = 'player-video.*?iframe.*?src="(.*?)"'

                match = re.compile(regexcat, re.DOTALL).findall(content)
                print("get regexcat =", regexcat)
                url = match[0]
                print("get url2 =", url)
                content2 = Utils.getUrl(url)
                if PY3:
                    content2 = six.ensure_str(content2)
                print("getVideos2 content2 =", content2)
                '''
                # if "youtube" in url.lower():
                    # print("In youtube url =", content2)
                    # from Plugins.Extensions.tvDream.youtube_dl import YoutubeDL
                    # ydl_opts = {'format': 'best'}
                    #
                    # ydl_opts = {'format': 'bestaudio/best'}
                    #
                    # ydl = YoutubeDL(ydl_opts)
                    # ydl.add_default_info_extractors()
                    # result = ydl.extract_info(url, download=False)
                    # # print ("mediaset result =", result)
                    # url = result["url"]
                    # # print ("mediaset final url =", url)
                    # print('YoutubeDL name: ', name)
                    # print('YoutubeDL url: ', url)
                    # self.session.open(Playstream2, name, url)
                '''
                if '.m3u8' in content2:
                    print('content .m3u8')
                    n1 = content2.find(".m3u8")
                    n2 = content2.rfind("http", 0, n1)
                    url = content2[n2:(n1 + 5)]
                    self.session.open(Playstream2, name, url)

                elif 'source src="' in content2:
                    print('content source src= .mp4')
                    regexcat2 = 'source src="(.*?)"'
                    match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                    url = match2[0]
                    n1 = url.find(".mp4")
                    n2 = url.rfind("http", 0, n1)
                    url = url[n2:(n1 + 5)]
                    self.session.open(Playstream2, name, url)

                elif '<a class="player-' in content2:
                    print("In <a class=player- =")
                    regexcat2 = '<a class="player-.*?href="(.*?)"'
                    match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                    url = match2[0]
                    content3 = Utils.getUrl(url)
                    if PY3:
                        content3 = six.ensure_str(content3)
                    print("getVideos2 content2 =", content3)
                    if '.m3u8' in content3:
                        print('content .m3u8')
                        n1 = content3.find(".m3u8")
                        n2 = content3.rfind("http", 0, n1)
                        url = content3[n2:(n1 + 5)]
                        # self.session.open(Playstream2, name, url)
                        print('content3 name: ', name)
                        print('content3 url: ', url)
                        self.session.open(Playstream2, name, url)

                elif '<a class="player_' in content2:
                    print("In player url =", url)
                    regexcat2 = '<a class="player_.*?href="(.*?)"'
                    match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                    url = match2[0]
                    content4 = Utils.getUrl(url)
                    if PY3:
                        content4 = six.ensure_str(content4)
                    print("getVideos2 content4 =", content4)
                    if '.m3u8' in content4:
                        print('content4 .m3u8')
                        n1 = content4.find(".m3u8")
                        n2 = content4.rfind("http", 0, n1)
                        url = content4[n2:(n1 + 5)]
                        print('content4 name: ', name)
                        print('content4 url: ', url)
                        self.session.open(Playstream2, name, url)

                elif ("rai" in url.lower()) or ("rai" in name.lower()):
                    print("In rai url =", url)
                    regexcat2 = 'liveVideo":{"mediaUrl":"(.*?)"'
                    match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                    url = match2[0]
                    print('content2 rai name: ', name)
                    print('content2 rai url: ', url)
                    self.session.open(Playstream2, name, url)

                else:
                    regexcat = '<iframe.*?src="(.*?)"'
                    match = re.compile(regexcat, re.DOTALL).findall(content)
                    print("<iframe.*?src= match =", match)
                    url2 = match[0]
                    print("<iframe.*?src= url2 =", url2)
                    if 'player.twitch' not in content:
                        print('go testinpl')
                        self.testinpl(name, url2)
                    elif content.find('player.twitch'):

                        match = re.compile(regexcat, re.DOTALL).findall(content)
                        print("get player.twitch =", regexcat)
                        url2 = match[0]
                        print("get url2 =", url2)

                        url3 = url2.replace('https://player.twitch.tv/?channel=', '').replace('&parent=www.tvdream.net', '')
                        urlx = twxtv.replace('+', '')
                        url = Utils.b64decoder(urlx) + 'https://www.twitch.tv/' + url3
                        self.session.open(Playstream2, name, url)
                    else:
                        self.testinpl(name, url)
                    return
                return
            except:
                self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout=5)
                self['info'].setText(_('Nothing ... Retry'))
            return
        else:
            self.session.open(MessageBox, _("Sorry no found!!!"), MessageBox.TYPE_INFO, timeout=5)

    def testinpl(self, name, url):
        try:
            content2 = Utils.getUrl(url)
            if PY3:
                content2 = six.ensure_str(content2)
            print("testinpl content2 =", content2)
            if '.m3u8' in content2:
                print('content testinpl .m3u8')
                n1 = content2.find(".m3u8")
                n2 = content2.rfind("http", 0, n1)
                url = content2[n2:(n1 + 5)]
                self.session.open(Playstream2, name, url)

            elif 'source src="' in content2:
                print('content2 source .mp4')
                regexcat2 = 'source src="(.*?)"'
                match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                url = match2[0]
                n1 = url.find(".mp4")
                n2 = url.rfind("http", 0, n1)
                url = url[n2:(n1 + 5)]
                self.session.open(Playstream2, name, url)

            elif '<a class="player-' in content2:
                print("In player url =", url)
                regexcat2 = '<a class="player-.*?href="(.*?)"'
                match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                url = match2[0]
                content3 = Utils.getUrl(url)
                if PY3:
                    content3 = six.ensure_str(content3)
                print("getVideos3 content2 =", content3)
                if '.m3u8' in content3:
                    print('content3 .m3u8')
                    n1 = content3.find(".m3u8")
                    n2 = content3.rfind("http", 0, n1)
                    url = content3[n2:(n1 + 5)]
                    # self.session.open(Playstream2, name, url)
                    self.session.open(Playstream2, name, url)

            elif '<a class="player_' in content2:
                print("In playre 4 url =", url)
                regexcat2 = '<a class="player_.*?href="(.*?)"'
                match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                url = match2[0]
                content3 = Utils.getUrl(url)
                if PY3:
                    content3 = six.ensure_str(content3)
                print("getVideos4 content2 =", content3)
                if '.m3u8' in content3:
                    print('content4 .m3u8')
                    n1 = content3.find(".m3u8")
                    n2 = content3.rfind("http", 0, n1)
                    url = content3[n2:(n1 + 5)]
                    self.session.open(Playstream2, name, url)

            elif ("rai" in url.lower()) or ("rai" in name.lower()):
                print("In rai url 5 =", url)
                regexcat2 = 'liveVideo":{"mediaUrl":"(.*?)"'
                match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                url = match2[0]
                self.session.open(Playstream2, name, url)

            # elif "youtube" in url.lower():
                # print("In youtube url =", content2)
                # from Plugins.Extensions.tvDream.youtube_dl import YoutubeDL
                # ydl_opts = {'format': 'best'}
                # '''
                # ydl_opts = {'format': 'bestaudio/best'}
                # '''
                # ydl = YoutubeDL(ydl_opts)
                # ydl.add_default_info_extractors()
                # result = ydl.extract_info(url, download=False)
                # # print ("mediaset result =", result)
                # url = result["url"]
                # # print ("mediaset final url =", url)
                # self.session.open(Playstream2, name, url)
            return

        except:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout=5)
            self['info'].setText(_('Nothing ... Retry'))


class tvCategory(Screen):
    def __init__(self, session, name, url):
        self.session = session
        skin = os.path.join(skin_dream, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self['text'] = SetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_green'].hide()
        self['key_yellow'] = Button()
        self['key_yellow'].hide()
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(500, True)
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['ButtonSetupActions',
                                     'OkCancelActions',
                                     'ColorActions'], {'ok': self.okRun,
                                                       'green': self.okRun,
                                                       'red': self.close,
                                                       'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        url = 'https://www.tvdream.net/web-tv/categorie/'
        if Utils.check(url):
            datas = Utils.getUrl(url)
            if PY3:
                datas = six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                n1 = datas.find('menu-sub">', 0)
                if n1 < 0:
                    return
                n2 = datas.find("</ul>", n1)
                data2 = datas[n1:n2]
                # print("data A2 =", data2)
                regexcat = 'href="(.*?)">(.*?)<'
                match = re.compile(regexcat, re.DOTALL).findall(data2)
                for url, name in match:
                    if 'Logo di TVdream' in name:
                        continue
                    print('name : ', name)
                    print('url:  ', url)
                    self.urls.append(url)
                    self.names.append(html_conv.html_unescape(name))
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout=5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(subCategory, name, url)


class subCategory(Screen):
    def __init__(self, session, name, url):
        self.session = session
        skin = os.path.join(skin_dream, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self.name = name
        self.url = url
        self['text'] = SetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_green'].hide()
        self['key_yellow'] = Button()
        self['key_yellow'].hide()
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(500, True)
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions'], {'green': self.okRun,
                                                           'red': self.close,
                                                           'ok': self.okRun,
                                                           'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        name = self.name
        url = self.url
        if Utils.check(url):
            datas = Utils.getUrl(url)
            if PY3:
                datas = six.ensure_str(datas)
            print('datas :  ', datas)
            try:
                pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
                for page in pages:
                    url1 = url + "page/" + str(page) + "/"
                    name = "Page " + str(page)
                    print('name it : ', name)
                    print('url it:  ', url1)
                    self.urls.append(url1)
                    self.names.append(html_conv.html_unescape(name))
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout=5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(tvCanal, name, url)


class tvNew(Screen):
    def __init__(self, session, name, url):
        self.session = session
        skin = os.path.join(skin_dream, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self.name = name
        self.url = url
        self['text'] = SetList([])
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Play'))
        self['key_red'] = Button(_('Back'))
        self['key_green'].hide()
        self['key_yellow'] = Button()
        self['key_yellow'].hide()
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(500, True)
        self['title'] = Label(desc_plugin)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions'], {'green': self.okRun,
                                                           'red': self.close,
                                                           'ok': self.okRun,
                                                           'cancel': self.close}, -2)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        url = self.url
        name = self.name
        if Utils.check(url):
            datas = Utils.getUrl(url)
            if PY3:
                datas = six.ensure_str(datas)
            print('datas :  ', datas)
            try:
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
                    self.urls.append(url)
                    self.names.append(html_conv.html_unescape(name))
            except:
                self['info'].setText(_('Nothing ... Retry'))
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['text'])
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout=5)

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 1:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        if Utils.check(url):
            content = Utils.getUrl(url)
            if PY3:
                content = six.ensure_str(content)
            print('content :  ', content)
            try:
                regexcat = '<iframe.*?src="(.*?)"'

                match = re.compile(regexcat, re.DOTALL).findall(content)
                print("getVideos2 match =", match)
                url2 = match[0]
                print("getVideos2 url2 =", url2)
                # twitch = content.find('player.twitch')
                if 'player.twitch' not in content:
                    self.testinpl(name, url2)

                elif content.find('player.twitch'):
                    url3 = url2.replace('https://player.twitch.tv/?channel=', '').replace('&parent=www.tvdream.net', '')
                    urlx = twxtv.replace('+', '')
                    url = Utils.b64decoder(urlx) + 'https://www.twitch.tv/' + url3
                    self.session.open(Playstream2, name, url)
                else:
                    self.testinpl(name, url2)
                # return

            except:
                # self.testinpl(name,url2)
                self['info'].setText(_('Nothing ... Retry'))
            return

        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout=5)

    def testinpl(self, name, url2):
        try:
            content2 = Utils.getUrl(url2)
            if PY3:
                content2 = six.ensure_str(content2)
            print("getVideos2 content2 =", content2)

            if '.m3u8' in content2:
                print('content .m3u8')
                n1 = content2.find(".m3u8")
                n2 = content2.rfind("http", 0, n1)
                url = content2[n2:(n1 + 5)]
                self.session.open(Playstream2, name, url)

            # elif "youtube" in url.lower():
                # print("In youtube url =", content2)
                # from Plugins.Extensions.tvDream.youtube_dl import YoutubeDL
                # ydl_opts = {'format': 'best'}
                # '''
                # ydl_opts = {'format': 'bestaudio/best'}
                # '''
                # ydl = YoutubeDL(ydl_opts)
                # ydl.add_default_info_extractors()
                # result = ydl.extract_info(url, download=False)
                # # print ("mediaset result =", result)
                # url = result["url"]
                # # print ("mediaset final url =", url)
                # self.session.open(Playstream2, name, url)

            elif 'source src="' in content2:
                print('content .mp4')
                regexcat2 = 'source src="(.*?)"'
                match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                url = match2[0]
                n1 = url.find(".mp4")
                n2 = url.rfind("http", 0, n1)
                url = url[n2:(n1 + 5)]
                self.session.open(Playstream2, name, url)

            elif '<a class="player-' in content2:
                print("In player url =", url)
                regexcat2 = '<a class="player-.*?href="(.*?)"'
                match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                url = match2[0]
                content3 = Utils.getUrl(url)
                if PY3:
                    content3 = six.ensure_str(content3)
                print("getVideos2 content2 =", content3)
                if '.m3u8' in content3:
                    print('content .m3u8')
                    n1 = content3.find(".m3u8")
                    n2 = content3.rfind("http", 0, n1)
                    url = content3[n2:(n1 + 5)]
                    self.session.open(Playstream2, name, url)

            elif '<a class="player_' in content2:
                print("In player url =", url)
                regexcat2 = '<a class="player_.*?href="(.*?)"'
                match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                url = match2[0]
                content3 = Utils.getUrl(url)
                if PY3:
                    content3 = six.ensure_str(content3)
                print("getVideos2 content2 =", content3)
                if '.m3u8' in content3:
                    print('content .m3u8')
                    n1 = content3.find(".m3u8")
                    n2 = content3.rfind("http", 0, n1)
                    url = content3[n2:(n1 + 5)]
                    self.session.open(Playstream2, name, url)

            elif ("rai" in url.lower()) or ("rai" in name.lower()):
                print("In rai url =", url)
                regexcat2 = 'liveVideo":{"mediaUrl":"(.*?)"'
                match2 = re.compile(regexcat2, re.DOTALL).findall(content2)
                url = match2[0]
                self.session.open(Playstream2, name, url)

            return

        except:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout=5)
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
        self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {
            "toggleShow": self.OkPressed,
            "hide": self.hide
        }, 0)

        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={
            iPlayableService.evStart: self.serviceStarted
        })
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
            # self.hideTimer.stop()
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

    def debug(obj, text=""):
        print(text + " %s\n" % obj)


class Playstream1(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_dream, 'Playstream1.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('TiVuDream')
        self.setTitle(desc_plugin)
        self.list = []
        self['list'] = SetList([])
        self['info'] = Label('Select Player')
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Select'))
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions'], {'red': self.cancel,
                                                           'green': self.okClicked,
                                                           'back': self.cancel,
                                                           'cancel': self.cancel,
                                                           'ok': self.okClicked}, -2)
        self.name1 = name
        self.url = url
        print('In Playstream2 self.url =', url)
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
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
        showlist(self.names, self['list'])

    def okClicked(self):
        idx = self['list'].getSelectionIndex()
        if idx is not None or idx != -1:
            self.name = self.names[idx]
            self.url = self.urls[idx]
            if idx == 0:
                print('In playVideo url D=', self.url)
                self.play()
            elif idx == 1:
                print('In playVideo url B=', self.url)
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
                self.play()
            # preview
            elif idx == 3:
                print('In playVideo url D=', self.url)
                self.play2()
            else:
                print('In playVideo url D=', self.url)
                self.play()
            return

    def playfile(self, serverint):
        self.serverList[serverint].play(self.session, self.url, self.name)

    def play(self):
        url = self.url
        name = self.name
        self.session.open(Playstream2, name, url)

    def play2(self):
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
        try:
            self.session.nav.stopService()
            self.session.nav.playService(self.srefInit)
            self.close()
        except:
            pass


class Playstream2(InfoBarBase,
                  InfoBarMenu,
                  InfoBarSeek,
                  InfoBarAudioSelection,
                  InfoBarSubtitleSupport,
                  InfoBarNotifications,
                  TvInfoBarShowHide,
                  Screen):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 5000

    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.skinName = 'MoviePlayer'
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
                                     'ColorActions',
                                     'ButtonSetupActions',
                                     'OkCancelActions',
                                     'InfobarShowHideActions',
                                     'InfobarActions',
                                     'InfobarSeekActions'], {'stop': self.leavePlayer,
                                                             'epg': self.showIMDB,
                                                             'info': self.showIMDB,
                                                             # 'info': self.cicleStreamType,
                                                             'tv': self.cicleStreamType,
                                                             # 'stop': self.leavePlayer,
                                                             'cancel': self.cancel,
                                                             'leavePlayer': self.cancel,
                                                             'down': self.av,
                                                             'back': self.cancel}, -1)
        self.allowPiP = False
        self.service = None
        self.url = url
        self.pcip = 'None'
        self.name = html_conv.html_unescape(name)
        self.state = self.STATE_PLAYING
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
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
        return {0: '4:3 Letterbox',
                1: '4:3 PanScan',
                2: '16:9',
                3: '16:9 always',
                4: '16:10 Letterbox',
                5: '16:10 PanScan',
                6: '16:9 Letterbox'}[aspectnum]

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
        temp += 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)

    def showIMDB(self):
        text_clear = self.name
        if returnIMDB(text_clear):
            print('show imdb/tmdb')

    def slinkPlay(self, url):
        name = self.name
        ref = "{0}:{1}".format(url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(str(name))
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openTest(self, servicetype, url):
        name = self.name
        ref = "{0}:0:0:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(str(name))
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        from itertools import cycle, islice
        self.servicetype = '4097'
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        if str(os.path.splitext(url)[-1]) == ".m3u8":
            if self.servicetype == "1":
                self.servicetype = "4097"
        currentindex = 0
        streamtypelist = ["4097"]

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

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback is not None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def cancel(self):
        if os.path.exists('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(self.srefInit)
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except:
                pass
        self.close()

    def leavePlayer(self):
        self.session.nav.stopService()
        self.session.nav.playService(self.srefInit)
        self.close()


def main(session, **kwargs):
    try:
        from . import Update
        Update.upd_done()
    except:
        import traceback
        traceback.print_exc()
    session.open(MainSetting)


def Plugins(**kwargs):
    ico_path = 'logo.png'
    if not os.path.exists('/var/lib/dpkg/status'):
        ico_path = plugin_path + '/res/pics/logo.png'
    extensions_menu = PluginDescriptor(name=name_plugin, description=desc_plugin, where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main, needsRestart=True)
    result = [PluginDescriptor(name=name_plugin, description=desc_plugin, where=PluginDescriptor.WHERE_PLUGINMENU, icon=ico_path, fnc=main)]
    result.append(extensions_menu)
    return result
