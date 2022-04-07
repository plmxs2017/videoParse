
import sys,re
import html
import requests,urllib.parse
from lxml import etree
from m3u8download_hecoter import m3u8download
from Crypto.Cipher import AES
import base64

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29'
}

def unescape(string):
    string = urllib.parse.unquote(string)
    quoted = html.unescape(string).encode(sys.getfilesystemencoding()).decode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: chr(int(m.group(1), 16)), quoted)

def player_a(player_aaaa_url):
    # url = "JTY4JTc0JTc0JTcwJTczJTNBJTJGJTJGJTZEJTMzJTc1JTM4JTJFJTYzJTYxJTYzJTY4JTY1JTJFJTczJTc1JTZGJTc5JTZGJTJFJTYzJTYzJTJGJTZEJTMzJTc1JTM4JTJGJTYxJTYyJTYzJTcxJTJGJTY0JTZEJTJGJTY0JTZGJTc1JTZDJTc1JTZGJTY0JTYxJTZDJTc1JTJGJTY0JTZGJTc1JTZDJTc1JTZGJTY0JTYxJTZDJTc1JTVGJTMwJTMzJTMwJTVGJTY5JTZFJTY0JTY1JTc4JTJFJTZEJTMzJTc1JTM4"
    deurl = unescape(base64.b64decode(player_aaaa_url).decode())
    return deurl

def get_player_aaaa(url):
    # url = 'https://555dy.fun/vodplay/319169-1-30.html'
    response = requests.get(url=url,headers=HEADERS).text

    responses = response.split('\n')
    for response in responses:
        if 'player_aaaa' in response:
            player_aaaa_url= re.findall('"url":"(.+?)"',response)[0]
            return player_a(player_aaaa_url)


def api_php(data_url):
    url = 'https://jhpc.manduhu.com/duoduo/api.php'
    data = {
        'url':data_url
    }
    response = requests.post(url=url,data=data).json()
    return getVideoInfo(response['url'])

def getVideoInfo(data):
    key = '6461633263303839303464333031316666393035363463396637373836356366'
    # key1 = 'dac2c08904d3011ff90564c9f77865cf'
    iv = '4e5862486f574a627073454f696e3862'
    cryptor = AES.new(key=bytes.fromhex(key),mode=AES.MODE_CBC,IV=bytes.fromhex(iv))
    m3u8url = cryptor.decrypt(base64.b64decode(data)).decode('UTF-8', 'ignore').strip().strip(b'\x00'.decode())
    return m3u8url

def get_list(detail_url):
    # url = 'http://555dy.fun/voddetail/318860.html'
    infos = []
    response = requests.get(detail_url,headers=HEADERS).text
    html = etree.HTML(response)
    Title = html.xpath('//h1[@class="title"]/text()')[0]
    srcs = html.xpath("//div[@id='playlist1']//@href")
    titles = html.xpath("//div[@id='playlist1']//a/text()")
    for i in range(len(srcs)):
        info = {
            'title':Title + '_' + titles[i],
            'url':'http://555dy.fun' + srcs[i]
        }
        infos.append(info)
    List = resume(infos)
    for l in List:
        one_video_parse(l['title'],l['url'])

def one_video_parse(title,url):
    m3u8download(video_parser(url),title=title)

def resume(List1):
    List2 = []
    if List1 == []:
        print('列表获取错误')
        return
    i = 0
    for List in List1:
        print(i, List['title'],List['url'])
        i = i + 1
    numbers = input('输入下载序列（① 5 ② 4-10 ③ 4 10）:')
    if ' ' in numbers:
        for number in numbers.split(' '):
            number = int(number)
            List2.append(List1[number])
    elif '-' in numbers:
        number = re.findall('\d+', numbers)
        return List1[int(number[0]):int(number[1]) + 1]
    else:
        number = re.findall('\d+', numbers)
        List2.append(List1[int(number[0])])
        return List2
    return List2

def video_parser(url):
    # url = 'https://555dy.fun/vodplay/319169-1-30.html'
    player_aaaa_url = get_player_aaaa(url)
    videoInfo = api_php(player_aaaa_url)
    return videoInfo


if __name__ == '__main__':

    # url = 'https://555dy.fun/vodplay/319169-1-30.html'
    print('示例：https://555dy.fun/vodplay/319169-1-30.html \n     http://555dy.fun/voddetail/318860.html')
    while True:
        url = input('输入视频网址：')
        # video_parser(url)
        if 'voddetail' in url:
            get_list(detail_url=url)
        elif 'vodplay' in url:
            one_video_parse(title='', url=url)
        else:
            print('未知类型')


