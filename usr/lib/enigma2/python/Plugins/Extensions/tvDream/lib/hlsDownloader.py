"""
Simple HTTP Live Streaming client.

References:
    http://tools.ietf.org/html/draft-pantos-http-live-streaming-08

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.

Last updated: July 22, 2012
MODIFIED BY shani to make it work with F4mProxy
"""
import sys
import struct  # Added missing import
from six.moves.urllib.parse import urlparse
import xbmc
import traceback
import re
import array
import random
import string
import requests  # Added missing import

PY3 = sys.version_info[0] == 3

if PY3:
    import http.cookiejar
else:
    import urllib
    import cookielib

'''
from crypto.cipher.aes      import AES
from crypto.cipher.cbc      import CBC
from crypto.cipher.base     import padWithPadLen
from crypto.cipher.rijndael import Rijndael
from crypto.cipher.aes_cbc import AES_CBC
'''
gproxy = None
gauth = None

try:
    from Crypto.Cipher import AES
    USEDec = 1  # 1==crypto 2==local, local pycrypto
except BaseException:
    print('pycrypt not available using slow decryption')
    USEDec = 3  # 1==crypto 2==local, local pycrypto

if USEDec == 1:
    print('using pycrypto')
elif USEDec == 2:
    from decrypter import AESDecrypter
    AES_decrypter = AESDecrypter()  # Fixed: renamed to avoid redefinition
else:
    from f4mUtils import python_aes

iv = None
key = None
value_unsafe = '%+&;#'
VALUE_SAFE = ''.join(chr(c) for c in range(33, 127)
                     if chr(c) not in value_unsafe)

SUPPORTED_VERSION = 3

if PY3:
    cookieJar = http.cookiejar.LWPCookieJar()
else:
    cookieJar = cookielib.LWPCookieJar()
clientHeader = None


class HLSDownloader():
    """
    A downloader for f4m manifests or AdobeHDS.
    """

    def __init__(self):
        self.init_done = False

    def init(
            self,
            out_stream,
            url,
            proxy=None,
            use_proxy_for_chunks=True,
            g_stopEvent=None,
            maxbitrate=0,
            auth=''):
        try:
            self.init_done = False
            self.init_url = url
            self.status = 'init'
            self.proxy = proxy
            self.auth = auth
            if self.auth is None or self.auth == 'None' or self.auth == '':
                self.auth = None
            if self.auth:
                pass

            if self.proxy and len(self.proxy) == 0:
                self.proxy = None
            self.use_proxy_for_chunks = use_proxy_for_chunks
            self.out_stream = out_stream
            self.g_stopEvent = g_stopEvent
            self.maxbitrate = maxbitrate
            if '|' in url:
                sp = url.split('|')
                url = sp[0]
                clientHeader = sp[1]
                print(clientHeader)
                if PY3:
                    clientHeader = urllib.parse.parse_qsl(clientHeader)
                else:
                    clientHeader = urlparse.parse_qsl(clientHeader)
                print(
                    'header recieved now url and headers are',
                    url,
                    clientHeader)
            self.status = 'init done'
            self.url = url
            return self.preDownoload()
        except BaseException:
            traceback.print_exc()
            self.status = 'finished'
        return False

    def preDownoload(self):
        print('code here')
        return True

    def keep_sending_video(
            self,
            dest_stream,
            segmentToStart=None,
            totalSegmentToSend=0):
        try:
            self.status = 'download Starting'
            downloadInternal(
                self.url,
                dest_stream,
                self.maxbitrate,
                self.g_stopEvent)
        except BaseException:
            traceback.print_exc()
        self.status = 'finished'


def getUrl(url, timeout=15, returnres=False, stream=False):
    try:
        post = None
        # Fixed: create session object instead of using undefined variable
        session_obj = requests.Session()
        session_obj.cookies = cookieJar
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:42.0) Gecko/20100101 Firefox/42.0 Iceweasel/42.0'}
        if clientHeader:
            for n, v in clientHeader:
                headers[n] = v
        proxies = {}
        if gproxy:
            proxies = {"http": "http://" + gproxy}
        if post:
            req = session_obj.post(
                url,
                headers=headers,
                data=post,
                proxies=proxies,
                verify=False,
                timeout=timeout,
                stream=stream)
        else:
            req = session_obj.get(
                url,
                headers=headers,
                proxies=proxies,
                verify=False,
                timeout=timeout,
                stream=stream)

        req.raise_for_status()
        if returnres:
            return req
        else:
            return req.text
    except BaseException:
        print('Error in getUrl')
        traceback.print_exc()
        return None


def download_chunks(URL, chunk_size=4096, enc=None):
    conn = getUrl(URL, timeout=6, returnres=True, stream=True)
    if enc:
        if USEDec == 1:
            chunk_size *= 1000
        else:
            chunk_size *= 100

    else:
        chunk_size = chunk_size * 1000

    for chunk in conn.iter_content(chunk_size=chunk_size):
        yield chunk


def download_file(URL):
    return ''.join(download_chunks(URL))


def validate_m3u(conn):
    ''' make sure file is an m3u, and returns the encoding to use. '''
    return 'utf8'
    mime = conn.headers.get('Content-Type', '').split(';')[0].lower()
    if mime == 'application/vnd.apple.mpegurl':
        enc = 'utf8'
    elif mime == 'audio/mpegurl':
        enc = 'iso-8859-1'
    elif conn.url.endswith('.m3u8'):
        enc = 'utf8'
    elif conn.url.endswith('.m3u'):
        enc = 'iso-8859-1'
    else:
        raise Exception("Stream MIME type or file extension not recognized")
    if conn.readline().rstrip('\r\n') != '#EXTM3U':
        raise Exception("Stream is not in M3U format")
    return enc


def gen_m3u(url, skip_comments=True):
    conn = getUrl(url, returnres=True)
    enc = validate_m3u(conn)
    for line in conn.iter_lines():
        line = line.rstrip('\r\n').decode(enc)
        if not line:
            continue
        elif line.startswith('#EXT'):
            yield line
        elif line.startswith('#'):
            if skip_comments:
                continue
            else:
                yield line
        else:
            yield line


def parse_m3u_tag(line):
    if ':' not in line:
        return line, []
    tag, attribstr = line.split(':', 1)
    attribs = []
    last = 0
    quote = False
    for i, c in enumerate(attribstr + ','):
        if c == '"':
            quote = not quote
        if quote:
            continue
        if c == ',':
            attribs.append(attribstr[last:i])
            last = i + 1
    return tag, attribs


def parse_kv(attribs, known_keys=None):
    d = {}
    for item in attribs:
        k, v = item.split('=', 1)
        k = k.strip()
        v = v.strip().strip('"')
        if known_keys is not None and k not in known_keys:
            raise ValueError("unknown attribute %s" % k)
        d[k] = v
    return d


def handle_basic_m3u(url):
    global iv
    seq = 1
    enc = None
    duration = 5
    targetduration = 5
    aesdone = False
    for line in gen_m3u(url):
        if line.startswith('#EXT'):
            tag, attribs = parse_m3u_tag(line)
            if tag == '#EXTINF':
                duration = float(attribs[0])
            elif tag == '#EXT-X-TARGETDURATION':
                assert len(
                    attribs) == 1, "too many attribs in EXT-X-TARGETDURATION"
                targetduration = int(attribs[0])
                pass
            elif tag == '#EXT-X-MEDIA-SEQUENCE':
                assert len(
                    attribs) == 1, "too many attribs in EXT-X-MEDIA-SEQUENCE"
                seq = int(attribs[0])
            elif tag == '#EXT-X-KEY':
                attribs = parse_kv(attribs, ('METHOD', 'URI', 'IV'))
                assert 'METHOD' in attribs, 'expected METHOD in EXT-X-KEY'
                if attribs['METHOD'] == 'NONE':
                    assert 'URI' not in attribs, 'EXT-X-KEY: METHOD=NONE, but URI found'
                    assert 'IV' not in attribs, 'EXT-X-KEY: METHOD=NONE, but IV found'
                    enc = None
                elif attribs['METHOD'] == 'AES-128':
                    if not aesdone:
                        aesdone = False
                        assert 'URI' in attribs, 'EXT-X-KEY: METHOD=AES-128, but no URI found'
                        codeurl = attribs['URI'].strip('"')
                        if gauth:
                            codeurl = gauth
                        if not codeurl.startswith('http'):
                            if PY3:
                                codeurl = urllib.parse.urljoin(url, codeurl)
                            else:
                                codeurl = urlparse.urljoin(url, codeurl)

                        assert len(
                            key) == 16, 'EXT-X-KEY: downloaded key file has bad length'
                        if 'IV' in attribs:
                            assert attribs['IV'].lower().startswith(
                                '0x'), 'EXT-X-KEY: IV attribute has bad format'
                            iv_hex = attribs['IV'][2:].zfill(32)
                            if PY3:
                                iv = bytes.fromhex(iv_hex)
                            else:
                                iv = iv_hex.decode('hex')
                            assert len(
                                iv) == 16, 'EXT-X-KEY: IV attribute has bad length'
                        else:
                            if PY3:
                                iv = b'\0' * 8 + struct.pack('>Q', seq)
                            else:
                                iv = '\0' * 8 + struct.pack('>Q', seq)
                else:
                    assert False, 'EXT-X-KEY: METHOD=%s unknown' % attribs['METHOD']
            elif tag == '#EXT-X-PROGRAM-DATE-TIME':
                assert len(
                    attribs) == 1, "too many attribs in EXT-X-PROGRAM-DATE-TIME"
                pass
            elif tag == '#EXT-X-ALLOW-CACHE':
                pass
            elif tag == '#EXT-X-ENDLIST':
                assert not attribs
                yield None
                return
            elif tag == '#EXT-X-STREAM-INF':
                raise ValueError(
                    "don't know how to handle EXT-X-STREAM-INF in basic playlist")
            elif tag == '#EXT-X-DISCONTINUITY':
                assert not attribs
                print("[warn] discontinuity in stream")
            elif tag == '#EXT-X-VERSION':
                assert len(attribs) == 1
                if int(attribs[0]) > SUPPORTED_VERSION:
                    print(
                        "[warn] file version %s exceeds supported version %d; some things might be broken" %
                        (attribs[0], SUPPORTED_VERSION))
        else:
            yield (seq, enc, duration, targetduration, line)
            seq += 1


def send_back(data, file):
    file.write(data)
    file.flush()


def downloadInternal(url, file, maxbitrate=0, stopEvent=None):
    if stopEvent and stopEvent.isSet():
        return
    dumpfile = None
    variants = []
    variant = None
    redirurl = url
    try:
        print('going gor  ', url)
        res = getUrl(url, returnres=True)
        print('here ', res)
        if res.history:
            print('history')
            redirurl = res.url
        res.close()

    except BaseException:
        traceback.print_exc()
    print('redirurl', redirurl)
    for line in gen_m3u(url):
        if line.startswith('#EXT'):
            tag, attribs = parse_m3u_tag(line)
            if tag == '#EXT-X-STREAM-INF':
                variant = attribs
        elif variant:
            variants.append((line, variant))
            variant = None
    print('variants', variants)
    if len(variants) == 0:
        url = redirurl
    if len(variants) == 1:
        if PY3:
            url = urllib.parse.urljoin(redirurl, variants[0][0])
        else:
            url = urlparse.urljoin(redirurl, variants[0][0])
    elif len(variants) >= 2:
        print("More than one variant of the stream was provided.")
        choice = - 1
        lastbitrate = 0
        print('maxbitrate', maxbitrate)
        for i, (vurl, vattrs) in enumerate(variants):
            for attr in vattrs:
                # Fixed: use different variable name to avoid redefining 'key'
                attr_key, value = attr.split('=')
                attr_key = attr_key.strip()
                value = value.strip().strip('"')
                if attr_key == 'BANDWIDTH':
                    print('bitrate %.2f kbps' % (int(value) / 1024.0))
                    if int(value) <= int(maxbitrate) and int(
                            value) > lastbitrate:
                        choice = i
                        lastbitrate = int(value)
                elif attr_key == 'PROGRAM-ID':
                    print('program %s' % value)
                elif attr_key == 'CODECS':
                    print('codec %s' % value)
                elif attr_key == 'RESOLUTION':
                    print('resolution %s' % value)
                else:
                    print("unknown STREAM-INF attribute %s" % attr_key)
            print()
        if choice == - 1:
            choice = 0

        print('choose %d' % choice)
        if PY3:
            url = urllib.parse.urljoin(redirurl, variants[choice][0])
        else:
            url = urlparse.urljoin(redirurl, variants[choice][0])
    control = ['go']
    last_seq = -1
    targetduration = 5
    glsession = None
    if ':7777' in url:
        try:
            # Fixed: escape sequence in regex
            glsession = re.compile(
                r':7777/.*?m3u8.*?session=(.*?)&').findall(url)[0]
        except BaseException:
            pass
    try:
        while True:
            if stopEvent and stopEvent.isSet():
                return
            medialist = list(handle_basic_m3u(url))
            playedSomething = False
            if medialist is None:
                return
            if None in medialist:
                pass
            else:
                medialist = medialist[-6:]

            addsomewait = False
            for media in medialist:
                if stopEvent and stopEvent.isSet():
                    return
                if media is None:
                    return
                seq, encobj, duration, targetduration, media_url = media
                addsomewait = True
                if seq > last_seq:
                    enc = None
                    if encobj:
                        codeurl, iv = encobj
                        key = download_file(codeurl)
                        if not USEDec == 3:
                            enc = AES.new(key, AES.MODE_CBC, iv)
                        else:
                            ivb = array.array('B', iv)
                            keyb = array.array('B', key)
                            enc = python_aes.new(keyb, 2, ivb)

                    if glsession:
                        media_url = media_url.replace(glsession, glsession[:-10] + ''.join(
                            random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))
                    try:
                        for chunk in download_chunks(
                                urlparse.urljoin(url, media_url), enc=encobj):
                            if stopEvent and stopEvent.isSet():
                                return

                            if enc:
                                if not USEDec == 3:
                                    chunk = enc.decrypt(chunk)
                                else:
                                    chunkb = array.array('B', chunk)
                                    chunk = enc.decrypt(chunkb)
                                    chunk = "".join(map(chr, chunk))

                            if dumpfile:
                                dumpfile.write(chunk)
                            send_back(chunk, file)

                        last_seq = seq
                        playedSomething = True
                    except BaseException:
                        pass

            if not playedSomething:
                xbmc.sleep(2000 + (3000 if addsomewait else 0))
    except BaseException:
        control[0] = 'stop'
        raise
