import re
import requests
from lxml import etree
from time import sleep
import ddddocr
from m3u8download_hecoter import m3u8download

ocr = ddddocr.DdddOcr()

def run(playurl):
    # url = 'https://cokemv.me/vodplay/39727-1-2.html'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }
    response = requests.get(url=playurl, headers=headers).text

    title = re.findall('<title>在线播放(.+?) - 高清资源 - COKEMV影视 在线1080P电影</title>', response)[0]
    player_aaaa = eval(re.findall('player_aaaa=(\{.+?\})', response)[0].replace('\\', ''))
    m3u8url = player_aaaa['url']
    m3u8download(m3u8url, title=title, base_uri='https://cokemv.org')

def resume(List1):
    List2 = []
    if List1 == []:
        print('列表获取错误')
        return
    i = 0
    for List in List1:
        print("{:>3}  {:<25} {:<50}".format(i,List['title'],List['playurl']))
        # print('{:^8}'.format(i), List['Title'],List['play_url'])
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

def spider(url):
    # url = 'https://cokemv.me/voddetail/39421.html'
    infos = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }
    response = requests.get(url=url,headers=headers).text

    HTML = etree.HTML(response)
    links = HTML.xpath("//a[@class='module-play-list-link']/@href")

    titles = HTML.xpath("//a[@class='module-play-list-link']/@title")
    for i in range(len(links)):
        info = {
            'title':titles[i],
            'playurl':'https://cokemv.me' + links[i]
        }
        infos.append(info)
    infos = resume(infos)
    for info in infos:
        run(info['playurl'])

def search(keyword):
    search_url = f'https://cokemv.me/vodsearch/{keyword}-------------.html'
    session = requests.Session()
    response = session.get(url=search_url).text
    code_url = 'https://cokemv.me/index.php/verify/index.html?'
    code_content = session.get(code_url).content
    code = ocr.classification(code_content)
    verify_url = f'https://cokemv.me/index.php/ajax/verify_check?type=search&verify={code}'
    response2 = session.post(verify_url)

    try:
        if response2.json()['msg'] != "ok":
            search(keyword)
    except:
        search(keyword)
    sleep(3)
    response = session.get(search_url).text
    html = etree.HTML(response)
    urls = html.xpath("//div[@class='module-card-item-title']//@href")[0]
    urls = 'https://cokemv.me' + urls
    titles = html.xpath("//div[@class='module-card-item-title']//text()")[1]
    print(titles,urls)

if __name__ == '__main__':
    print('https://cokemv.me 视频解析')
    while True:
        url = input('输入下载链接或关键字：')
        if 'voddetail' in url:
            spider(url)
        elif 'vodplay' in url:
            run(playurl=url)
        elif 'http' not in url:
            search(url)


