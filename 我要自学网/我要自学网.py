import json
import re,base64
import requests
from m3u8download_hecoter import m3u8download

class _51ZXW:
    def __init__(self,cookie=''):
        self.baseurl = 'https://www.51zxw.net'

        self.Cookie = cookie
        self.title = ''

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39',
            'Cookie': self.Cookie,
            'Referer': 'https://www.51zxw.net',
        }

    def login(self,username,password):
        login_url = 'https://www.51zxw.net/login/NewLogin/AjaxForlogin'
        url = 'https://www.51zxw.net/login'
        session = requests.session()
        response = session.get(url).text
        __RequestVerificationToken = re.findall('"__RequestVerificationToken" type="hidden" value="(.+?)"', response)[0]
        data = {
            'loginStr':username,
            'pwd':password,
            '__RequestVerificationToken':__RequestVerificationToken,
            'isRememberlogin':'false'
        }
        response2 = session.post(url=login_url,data=data)
        login_info = response2.json()
        msg = login_info['msg']
        print(msg)

        if login_info['success'] == True:
            self.headers['Cookie'] = 'newsMember=' + response2.cookies.values()[0]
            return True
        else:
            return False



    def spider(self,url):
        if 'Show.aspx' in url or 'show.aspx' in url:
            self.run(url)
        elif 'List.aspx' in url or 'list.aspx' in url:
            infos = []
            response = requests.get(url, headers=self.headers).text
            cid = str(re.findall('cid: parseInt\("(\d+)"\)',response)[0])

            getChaptersUrl = 'https://www.51zxw.net/MainExtend/AjaxGetChapters.ashx'
            data = {
                'cid':cid,
                'pageIndex':'1'
            }
            chapters_response_data = requests.post(url=getChaptersUrl,data=data,headers=self.headers).json()['data']

            Pages = int(chapters_response_data[0]['Pages'])
            for fenye in range(1,Pages+1):
                data = {
                'cid':cid,
                'pageIndex':str(fenye)
            }
                data_response = requests.post(url=getChaptersUrl,headers=self.headers,data=data).json()
                datas = data_response['data']
                for data_info in datas:
                    if data_info['Source'] != None:
                        info = {

                            'Title':data_info['Title'],
                            'play_url':f'https://www.51zxw.net/Show.aspx?cid={cid}&id={data_info["Articleid"]}'
                        }
                        infos.append(info)
            infos = self.resume(infos)
            for info in infos:
                self.run(url=info['play_url'],title=info['Title'])
    def resume(self, List1):
        List2 = []
        if List1 == []:
            print('列表获取错误')
            return
        i = 0
        for List in List1:
            print("{:>3}  {:<25} {:<50}".format(i,List['Title'],List['play_url']))
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

    def safe_base64_decode(self,data):
        try:
            num = len(data) % 4
            if num != 0:
                data = data + '=' * (4 - num)
            dedata = base64.b64decode(data).decode()
        except:
            data = data[:-34]
            dedata = self.safe_base64_decode(data)
        return dedata

    def run(self,url,title=None):
        # url = 'https://www.51zxw.net/Show.aspx?cid=1037&id=120698'
        response = requests.get(url=url, headers=self.headers).text
        self.title = title
        if self.title is None:
            self.title = re.findall('<meta name="keywords" content="(.+?)" />', response)[0].replace(',我要自学网,视频教程', '')


        videourl1 = self.baseurl + re.findall("website:(.+?)'", response)[0]
        response2 = json.loads(requests.get(videourl1, headers=self.headers).content.decode())

        videourl2 = response2['video'][0][0]

        data = requests.get(videourl2, headers=self.headers).text

        dedata = self.decodeData(data)

        keyurl = self.baseurl + '/' + re.findall('URI="(.+?)"', dedata)[0]

        key = self.getKey(keyurl)
        m3u8download(m3u8url=f'{self.title}.m3u8',title=self.title,key=base64.b64encode(key.encode()).decode())

    def decodeData(self, data):
        data = data[64:][-60:][0:30] + data[64:][0:len(data[64:]) - 60] + data[64:][-30:]
        dedata = self.safe_base64_decode(data)

        with open(f'{self.title}.m3u8', 'w') as f:
            f.write(dedata)
        return dedata

    def getKey(self,keyurl):
        response = requests.get(keyurl, headers=self.headers).json()
        value = response['value']
        dykey = self.safe_base64_decode(value)[18:]
        u = list(bytes(dykey.encode()))
        newkey = [u[15], u[0], u[8], u[9], u[10], u[11], u[12], u[13], u[14], u[1], u[2], u[3], u[4], u[5], u[6], u[7]]
        newkey = bytes(newkey).decode()
        return newkey

if __name__ == '__main__':
    print('我要自学网视频下载器')
    print('支持链接格式：https://www.51zxw.net/show.aspx?id=113755&cid=988 https://www.51zxw.net/List.aspx?cid=988')
    cookie = input('输入Cookie（或回车跳过输入账号密码）:')
    zxw = _51ZXW(cookie=cookie)
    if cookie == '':
        username = input('输入账号：')
        password = input('输入密码：')
        zxw.login(username=username,password=password)

    while True:
        url = input('输入解析链接：')
        try:
            zxw.spider(url=url)
        except:
            print('无权限观看，或未知错误')

