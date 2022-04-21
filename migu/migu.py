import requests
import re

def resume(List1):
    List2 = []
    if List1 == []:
        print('列表获取错误')
        return
    i = 0
    for List in List1:
        print("{:>3}  {:<15} {:<50}".format(i,List['name'],List['subSetId']))
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

def run(url):
    # url = 'https://www.miguvideo.com/mgs/website/prd/detail.html?cid=717417210'
    cid = re.findall('cid=(\d+)', url)[0]
    webapi_url = f'https://webapi.miguvideo.com/gateway/playurl/v3/play/playurl?contId={cid}&startPlay=true'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }

    response = requests.get(url=webapi_url, headers=headers).json()

    content = response['body']['content']
    contName = content['contName']
    if '《' in contName:
        contName = re.findall('《(.+?)》', contName)[0]
    subcollectionList = response['body']['content']['subcollectionList']
    if subcollectionList == []:

        single_parse(countid=cid)
    else:
        infos = []
        for i in range(len(subcollectionList)):
            subSetId = str(subcollectionList[i]['subSetId'])
            info = {
                'name':contName +'_'+str(subcollectionList[i]['index']),
                'subSetId':'https://www.miguvideo.com/mgs/website/prd/detail.html?cid=' + subSetId,
                'cid':subSetId
            }
            infos.append(info)
        infos = resume(infos)
        for info in infos:
            single_parse(countid=info['cid'])

def magic(video_url):
    video_url = video_url.split('.m3u8')[0].replace('http://h5vod.gslb.cmvideo.cn/depository_yqv/asset/zhengshi','http://yue.cmvideo.cn:8080/depository_yqv/asset/zhengshi')
    return video_url

def single_parse(countid):
    webapi_url = f'https://webapi.miguvideo.com/gateway/playurl/v3/play/playurl?contId={countid}&startPlay=true'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }
    response = requests.get(url=webapi_url, headers=headers).json()
    content = response['body']['content']
    contName = content['contName']
    urlInfo = response['body']['urlInfo']

    video_url = magic(urlInfo['url'])
    rateDesc = urlInfo['rateDesc']
    contName += '_'+rateDesc
    print(contName,video_url)

if __name__ == '__main__':
    print('migu视频解析')
    while True:
        url = input('输入咪咕视频网址：')
        run(url)
