import re
import requests
from m3u8download_hecoter import m3u8download

url = 'https://cokemv.me/vodplay/39727-1-2.html'

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
}
response = requests.get(url=url,headers=headers).text

title = re.findall('<title>在线播放(.+?) - 高清资源 - COKEMV影视 在线1080P电影</title>',response)[0]
player_aaaa = eval(re.findall('player_aaaa=(\{.+?\})',response)[0].replace('\\',''))
m3u8url = player_aaaa['url']
m3u8download(m3u8url,title=title,base_uri='https://cokemv.org')
