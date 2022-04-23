
import random
import re
import time
import execjs
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from m3u8download_hecoter import m3u8download

def get_cKey_python(vid,tm,appVer,guid,platform):
    Kn = bytes.fromhex("4E2918885FD98109869D14E0231A0BF4") # 固定
    Wn = bytes.fromhex("16B17E519DDD0CE5B79D7A63A4DD801C") # 固定

    sr = "mg3c3b04ba" #固定
    Nn = "https://w.yangshipin.cn/"
    Fn = f"|{vid}|{tm}|{sr}|{appVer}|{guid}|{platform}|{Nn}|mozilla/5.0 (windows nt ||Mozilla|Netscape|Win32|"
    jscode = """function get_qn(Vn){Jn=0;for(Mr=0;Mr<Vn.length;Mr++)Xn=Vn.charCodeAt(Mr),Jn=(Jn<<5)-Jn+Xn,Jn&=Jn;return Jn;}"""
    ctx = execjs.compile(jscode)
    qn = ctx.call('get_qn',Fn)
    Yn = f"|{qn}" + Fn
    # print(Yn)
    cryptor = AES.new(key=Kn,mode=AES.MODE_CBC,iv=Wn)
    cKey = '--01' + cryptor.encrypt(pad(Yn.encode(),16)).hex().upper()

    return cKey

def get_flowid():
    """flowid = `${(new Date).getTime().toString(36)}_${Math.random().toString(36).replace(/^0./, "")}`"""
    def baseN(num, b):
        return ((num == 0) and "0") or \
               (baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])
    flowid = baseN(int(time.time()*1000),36) + '_' + baseN(int(str(random.random()).replace('0.','')), 36)
    return flowid

def get_signs(url):
    headers = {
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44",
        'referer':'https://w.yangshipin.cn/'
    }

    guid = 'l29u6mj9_e5kopm32to5'
    platform = '4330701' # 视频平台 web: 4330701 app:4330303
    vid = re.findall('vid=(.+)',url)[0].split('&')[0]
    defn = 'fhd' # 清晰度
    charge = '0'
    defaultfmt = 'auto'
    otype = 'json'
    defnpayver = '1'  # app:defnpayver=5
    appVer = '0.2.0' # app:V8.7.1034.4247
    sphttps = '1' # app:0
    sphls = '1'# app:2
    spwm = '4' # app:2
    dtype = '3'
    defsrc = '2' # app:3
    encryptVer = '8.1' # app:4.2
    sdtfrom = '4330701' # app:v5028
    tm = str(int(time.time()))# 1650635739
    cKey = get_cKey_python(vid=vid,tm=tm,appVer=appVer,guid=guid,platform=platform)
    flowid = get_flowid()

    infourl = f"https://playvv.yangshipin.cn/playvinfo?&guid={guid}&platform={platform}&vid={vid}&defn={defn}&charge={charge}&defaultfmt={defaultfmt}&otype={otype}&defnpayver={defnpayver}&appVer={appVer}&sphttps={sphttps}&sphls={sphls}&spwm={spwm}&dtype={dtype}&defsrc={defsrc}&encryptVer={encryptVer}&sdtfrom={sdtfrom}&cKey={cKey}&flowid={flowid}"
    # print(infourl)
    response = eval(requests.get(url=infourl,headers=headers).text)
    ############################################
    vi = response['vl']['vi'][0]

    fn = vi['fn']

    fvkey = vi['fvkey']
    title = vi['ti']

    baseurl = vi['ul']['ui'][0]['url']
    # playurl = f"{baseurl}{fn}?sdtfrom={sdtfrom}&guid={guid}&vkey={fvkey}&platform=2"
    playurl_app = f"{baseurl}{fn}?vkey={fvkey}" # 这里其实有这个就够了，其他没用
    # print(title,playurl_app)
    m3u8download(title=title,m3u8url=playurl_app)


if __name__ == '__main__':
    print('央视频下载器 https://w.yangshipin.cn/video?type=0&vid=m000091l2hd')
    while True:
        url = input('输入下载网址：')
        try:
            get_signs(url)
        except:
            pass


