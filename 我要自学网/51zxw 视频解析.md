# 51zxw 视频解析

只有视频解析思路，无成品

测试网址：https://www.51zxw.net/Show.aspx?cid=1049&id=120012

## 1.打开浏览器开发者工具，刷新，观察数据

![iEhTT.jpg](https://s1.328888.xyz/2022/04/17/iEhTT.jpg)

发现视频数据是以图片形式加密

使用winhex查看图片数据，文件不以 `b'\x89PNG'`或 `b'BM\xee\x0c'`  开头，所以并不是简单的对ts文件进行图片伪装

![iE4N2.jpg](https://s1.328888.xyz/2022/04/17/iE4N2.jpg)

并且搜不到图片来源，说明图片文件加密，来源也加密

## 2.向上找可疑数据

发现两个链接：

1. ```
   https://www.51zxw.net/VLine.asp?ck=08af445d09f7e1b8e757585ed5f98c19&xl=727670336381316138020_1-3
   
   aUtwVnlFdjlVVXNITFVRSWFBVnVScDZqSk1ETHA4UkZ3ekU4WVBIRmloS2RKelkyozCiNFWFQtWC1UQVJHRVREVVJBVElPTjoyMAojRVhULVgtTUVESUEtU0VRVUVOQ0U6MAojRVhULVgtS0VZOk1FVEhPRD1BRVMtMTI4LFVSST0ic2hpcG1pbmdrby5hc3A/dj02QkVGOThFQiZ4PTI0MjU1Njc4MjAxNDA1OTEwNDkmY2s9Zjg5YmEyY2FjZjliZGIzMmVjNzA3ZjA0M2M2ZGExZDIiCiNFWFRJTkY6MjAuMDAwMDAwLApodHRwczovL3Y5OS41MXp4dy5uZXQvaDUvMTA0OS82QkVGOThFQi9hc2YveE4xaFhUT3ZEZGNPLnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL203bEZIY1lSUFZMcS5wbmcKI0VYVElORjoyMC4wMDAwMDAsCmh0dHBzOi8vdjk5LjUxenh3Lm5ldC9oNS8xMDQ5LzZCRUY5OEVCL2FzZi9ieEI1Sm4zVzJpODMucG5nCiNFWFRJTkY6MjAuMDAwMDAwLApodHRwczovL3Y5OS41MXp4dy5uZXQvaDUvMTA0OS82QkVGOThFQi9hc2YvZ0ZTVUFqT3NqOTU2LnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL3NzbmZ1WGdhYU5xSi5wbmcKI0VYVElORjoyMC4wMDAwMDAsCmh0dHBzOi8vdjk5LjUxenh3Lm5ldC9oNS8xMDQ5LzZCRUY5OEVCL2FzZi9SOGxIRWlVdjY0LnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL0d5QTZGdGtDc0QucG5nCiNFWFRJTkY6MjAuMDAwMDAwLApodHRwczovL3Y5OS41MXp4dy5uZXQvaDUvMTA0OS82QkVGOThFQi9hc2YvTEdSVzZxS0xRZW9HLnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL25IeFFOM25zcGVXLnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL01kVkZibm1hVGxJdi5wbmcKI0VYVElORjoyMC4wMDAwMDAsCmh0dHBzOi8vdjk5LjUxenh3Lm5ldC9oNS8xMDQ5LzZCRUY5OEVCL2FzZi9CU3c0Y3lIZjZ4NTgucG5nCiNFWFRJTkY6MjAuMDAwMDAwLApodHRwczovL3Y5OS41MXp4dy5uZXQvaDUvMTA0OS82QkVGOThFQi9hc2YvR2xDVVV1YzFuUDFCLnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL2luaXluUkxURVpzUi5wbmcKI0VYVElORjoyMC4wMDAwMDAsCmh0dHBzOi8vdjk5LjUxenh3Lm5ldC9oNS8xMDQ5LzZCRUY5OEVCL2FzZi9JMmhXTHVJT3pXNjgucG5nCiNFWFRJTkY6MjAuMDAwMDAwLApodHRwczovL3Y5OS41MXp4dy5uZXQvaDUvMTA0OS82QkVGOThFQi9hc2YvclN4MW5MTWsxbm9KLnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL051aHlDVTR5N1kucG5nCiNFWFRJTkY6MjAuMDAwMDAwLApodHRwczovL3Y5OS41MXp4dy5uZXQvaDUvMTA0OS82QkVGOThFQi9hc2YvNk5ZYk81em9ZVFZaLnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL0RYU1VpeWEzTEdLMy5wbmcKI0VYVElORjoyMC4wMDAwMDAsCmh0dHBzOi8vdjk5LjUxenh3Lm5ldC9oNS8xMDQ5LzZCRUY5OEVCL2FzZi8xTXNKazg1OHpUN0gucG5nCiNFWFRJTkY6MjAuMDAwMDAwLApodHRwczovL3Y5OS41MXp4dy5uZXQvaDUvMTA0OS82QkVGOThFQi9hc2YvNmY4aWI0UVZmdjNMLnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL1pnZUN2Y0F3NjR1YS5wbmcKI0VYVElORjoyMC4wMDAwMDAsCmh0dHBzOi8vdjk5LjUxenh3Lm5ldC9oNS8xMDQ5LzZCRUY5OEVCL2FzZi90WFRSdE1lOEc2MkUucG5nCiNFWFRJTkY6MjAuMDAwMDAwLApodHRwczovL3Y5OS41MXp4dy5uZXQvaDUvMTA0OS82QkVGOThFQi9hc2YvaE10R3ZYQUN1SXFTLnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL21mOWZtVFVaYWxuVy5wbmcKI0VYVElORjoyMC4wMDAwMDAsCmh0dHBzOi8vdjk5LjUxenh3Lm5ldC9oNS8xMDQ5LzZCRUY5OEVCL2FzZi9FZ2Y5NUUxdmRsLnBuZwojRVhUSU5GOjIwLjAwMDAwMCwKaHR0cHM6Ly92OTkuNTF6eHcubmV0L2g1LzEwNDkvNkJFRjk4RUIvYXNmL24xRFBHUXhvZHJHOS5wbmcKI0VYVElORjoyMC4wMDAwMDAsCmh0dHBzOi8vdjk5LjUxenh3Lm5ldC9oNS8xMDQ5LzZCRUY5OEVCL2FzZi90R29Zckt2Y3J6OVIucG5nCiNFWFRJTkY6MTcuMjAwMDAwLApodHRwczovL3Y5OS41MXp4dy5uZXQvaDUvMTA0OS82QkVGOThFQi9hc2YveVo1eGpHRXlYUjZVLnBuZwojRVhULVgtRU5ETElTVAoI0VYVE0zVQojRVhULVgtVkVSU0lPTjjZVLnBuZwojRVhULVgtRU5ETElTVAo
   ```

2. ```
   https://www.51zxw.net/shipmingko.asp?v=6BEF98EB&x=2425567820140591049&ck=f89ba2cacf9bdb32ec707f043c6da1d2
   
   {"type":"NK5o","value":"bzhqT1lLRWJvRTByUFczR3RCMWVjOGJiOWU1NTIxNWRmZUNpM01n"}
   ```

   毫无疑问，图片的链接是从这些加密数据中解密来的，另外经测试发现请求中必须含有 referer 才能请求成功

   ```
   headers = {
       'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39',
       'Cookie':Cookie,
       'Referer':'https://www.51zxw.net/Show.aspx?cid=1049&id=120013',
   }
   ```

   ### 2.1 VLine数据解密

   VLine 链接的获得可以先从网页源代码中获取 getvutf 的链接，通过此链接获取内容

   ```
   {'video': [['https://www.51zxw.net/VLine.asp?ck=19286429fd255549372084e1f26def6c&xl=727670336540832138020_1-3', 'xxx', '电信线路1', '10'], ['https://www.51zxw.net/VLine.asp?ck=19286429fd255549372084e1f26def6c&xl=727670336540832178020_1-3', 'xxx', '电信线路2', '0'], ['https://www.51zxw.net/VLine.asp?ck=19286429fd255549372084e1f26def6c&xl=727670336540832218020_1-3', 'xxx', '联通线路1', '0'], ['https://www.51zxw.net/VLine.asp?ck=19286429fd255549372084e1f26def6c&xl=727670336540832258020_1-3', 'xxx', '联通线路2', '0'], ['https://www.51zxw.net/VLine.asp?ck=19286429fd255549372084e1f26def6c&xl=727670336540832298020_1-3', 'xxx', '移动线路', '0']]}
   
   ```

   根据之前的经验直接去找加载成功的函数，下断点的这个地方就是解密部分

   ![iPe5Z.jpg](https://s1.328888.xyz/2022/04/17/iPe5Z.jpg)

   

可以把这里代码全都复制去运行：

```
var video_c = {
    _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    encode: function(e) {
        var t = "";
        var n, r, i, s, o, u, a;
        var f = 0;
        e = video_c._utf8_encode(e);
        while (f < e.length) {
            n = e.charCodeAt(f++);
            r = e.charCodeAt(f++);
            i = e.charCodeAt(f++);
            s = n >> 2;
            o = (n & 3) << 4 | r >> 4;
            u = (r & 15) << 2 | i >> 6;
            a = i & 63;
            if (isNaN(r)) {
                u = a = 64
            } else if (isNaN(i)) {
                a = 64
            }
            t = t + this._keyStr.charAt(s) + this._keyStr.charAt(o) + this._keyStr.charAt(u) + this._keyStr.charAt(a)
        }
        return t
    },
    decode: function(e) {
        var t = "";
        var n, r, i;
        var s, o, u, a;
        var f = 0;
        e = e.replace(/[^A-Za-z0-9+/=]/g, "");
        while (f < e.length) {
            s = this._keyStr.indexOf(e.charAt(f++));
            o = this._keyStr.indexOf(e.charAt(f++));
            u = this._keyStr.indexOf(e.charAt(f++));
            a = this._keyStr.indexOf(e.charAt(f++));
            n = s << 2 | o >> 4;
            r = (o & 15) << 4 | u >> 2;
            i = (u & 3) << 6 | a;
            t = t + String.fromCharCode(n);
            if (u != 64) {
                t = t + String.fromCharCode(r)
            }
            if (a != 64) {
                t = t + String.fromCharCode(i)
            }
        }
        t = video_c._utf8_decode(t);
        return t
    },
    _utf8_encode: function(e) {
        e = e.replace(/rn/g, "n");
        var t = "";
        for (var n = 0; n < e.length; n++) {
            var r = e.charCodeAt(n);
            if (r < 128) {
                t += String.fromCharCode(r)
            } else if (r > 127 && r < 2048) {
                t += String.fromCharCode(r >> 6 | 192);
                t += String.fromCharCode(r & 63 | 128)
            } else {
                t += String.fromCharCode(r >> 12 | 224);
                t += String.fromCharCode(r >> 6 & 63 | 128);
                t += String.fromCharCode(r & 63 | 128)
            }
        }
        return t
    },
    _utf8_decode: function(e) {
        var t = "";
        var n = 0;
        var r = c1 = c2 = 0;
        while (n < e.length) {
            r = e.charCodeAt(n);
            if (r < 128) {
                t += String.fromCharCode(r);
                n++
            } else if (r > 191 && r < 224) {
                c2 = e.charCodeAt(n + 1);
                t += String.fromCharCode((r & 31) << 6 | c2 & 63);
                n += 2
            } else {
                c2 = e.charCodeAt(n + 1);
                c3 = e.charCodeAt(n + 2);
                t += String.fromCharCode((r & 15) << 12 | (c2 & 63) << 6 | c3 & 63);
                n += 3
            }
        }
        return t
    }
};
```

简单转换下就是：

```
def decodeData(data):

    data = data[64:][-60:][0:30] + data[64:][0:len(data[64:])-60] + data[64:][-30:]

    dedata = safe_base64_decode(data)

def safe_base64_decode(data):
    try:
        num = len(data) % 4
        if num != 0:
            data = data + '=' * (4 - num)
        dedata = base64.b64decode(data).decode()
    except:
        data = data[:-34]
        dedata = safe_base64_decode(data)
    return dedata
```

得出解密后的数据：

```
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:20
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-KEY:METHOD=AES-128,URI="shipmingko.asp?v=6BEF98EB&x=2425567820140591049&ck=f89ba2cacf9bdb32ec707f043c6da1d2"
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/xN1hXTOvDdcO.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/m7lFHcYRPVLq.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/bxB5Jn3W2i83.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/gFSUAjOsj956.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/ssnfuXgaaNqJ.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/R8lHEiUv64.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/GyA6FtkCsD.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/LGRW6qKLQeoG.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/nHxQN3nspeW.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/MdVFbnmaTlIv.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/BSw4cyHf6x58.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/GlCUUuc1nP1B.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/iniynRLTEZsR.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/I2hWLuIOzW68.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/rSx1nLMk1noJ.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/NuhyCU4y7Y.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/6NYbO5zoYTVZ.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/DXSUiya3LGK3.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/1MsJk858zT7H.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/6f8ib4QVfv3L.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/ZgeCvcAw64ua.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/tXTRtMe8G62E.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/hMtGvXACuIqS.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/mf9fmTUZalnW.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/Egf95E1vdl.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/n1DPGQxodrG9.png
#EXTINF:20.000000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/tGoYrKvcrz9R.png
#EXTINF:17.200000,
https://v99.51zxw.net/h5/1049/6BEF98EB/asf/yZ5xjGEyXR6U.png
#EXT-X-ENDLIST

```

m3u8链接有了，方法是aes-cbc，接下来就是key，

### 2.2 shipmingko value解密

知道了上面怎么解密，让代码继续运行发现 value 采用大致相同的加密方法

![rQsNB.jpg](https://s1.328888.xyz/2022/04/17/rQsNB.jpg)



```
a.data = stringToBytes(video_c.decode(e.substr(24)).substr(18));
```

转python:

```
value = response['value']
dykey =  safe_base64_decode(value)[18:]
```

但是这里 key 是21位，通常aes-cbc解密key是16位，所以还得继续向下解密

二次解密：

```
u = list(bytes(dykey.encode()))
newkey = [u[15], u[0], u[8], u[9], u[10], u[11], u[12], u[13], u[14], u[1], u[2], u[3], u[4], u[5], u[6], u[7]]
```

## 3.下载部分

目前已有了m3u8内容,传入m3u8下载即可

这里我自写了一款： https://github.com/hecoter/m3u8download_hecoter

## 完整代码

```
import json
import re,base64
import requests
from m3u8download_hecoter import m3u8download

class _51ZXW:
    def __init__(self,cookie=''):
        if cookie != '':
            print('cookie 初始化成功！')
        self.baseurl = 'https://www.51zxw.net'

        self.Cookie = cookie
        self.title = ''

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39',
            'Cookie': self.Cookie,
            'Referer': 'https://www.51zxw.net',
        }

    def spider(self,url):
        if 'Show.aspx' in url:
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
    while True:
        cookie = input('输入Cookie:')
        zxw = _51ZXW(cookie=cookie)
        url = input('输入解析链接：')
        try:
            zxw.spider(url=url)
        except:
            print('无权限观看，或未知错误')



```

https://github.com/hecoter/videoParse/

