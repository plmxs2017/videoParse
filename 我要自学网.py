import json
import re,base64
import requests
from m3u8download_hecoter import m3u8download

class _51ZXW:
    def __init__(self,url,cookie=''):
        print('init 运行')
        self.baseurl = 'https://www.51zxw.net'

        self.Cookie = cookie
        self.title = ''
        self.url = url
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39',
            'Cookie': self.Cookie,
            'Referer': 'https://www.51zxw.net',
        }

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

    def run(self):
        response = requests.get(url=self.url, headers=self.headers).text
        self.title = re.findall('<meta name="keywords" content="(.+?)" />', response)[0]
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
    zxw = _51ZXW(url='https://www.51zxw.net/Show.aspx?cid=1049&id=120012',cookie='').run()



