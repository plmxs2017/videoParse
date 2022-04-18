# cokemv.me 视频站解析

测试网址：`https://cokemv.me/vodplay/39727-1-2.html`

这篇比较简单，但还是有几个地方要讲下

## 分析

| 问题                         | 解决方法                                                   |
| ---------------------------- | ---------------------------------------------------------- |
| 网页不能按 F12               | 手动打开开发者工具                                         |
| 遇到无限 debugger            | 在debugger 位置,点击行号,右键 *Never* *pause* here         |
| 在网页源代码就可看到m3u8链接 | 直接正则匹配内容                                           |
| 请求m3u8链接时链接不太对     | 加上 base_uri：https://cokemv.org                          |
| ts 文件伪图片加密            | 之前遇到过，使用我的m3u8下载器解析下载即可，已自动适配解密 |
|                              |                                                            |
|                              |                                                            |
|                              |                                                            |
|                              |                                                            |

## 代码

```
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
```

https://github.com/hecoter/videoParse

这个没写批量，不过已经到这一步，批量已经很简单了，如果感兴趣就自己写一下吧。