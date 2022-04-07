import json,sys,os
import time,base64

from m3u8download_hecoter import parser,download,merge,delFile

def m3u8download(m3u8url, title='', threads=20, key=None, iv=None, method=None, work_dir='./Downloads', headers=None,enable_del=True,merge_mode=3):
    # 构造m3u8下载信息
    # list: m3u8url = [{'m3u8url':m3u8url,'title':title},{'m3u8url':m3u8url,'title':title}]
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030532) Edg/100.0.4896.60',
            'Cookie': '',
        }
    if type(m3u8url) == list:
        for info in m3u8url:
            print(info)
            m3u8download(m3u8url=info['m3u8url'],title=info['title'])
        sys.exit(0)
    # dir: m3u8url = r'c:\windows\'
    if os.path.isdir(m3u8url):
        for root, dirs, files in os.walk(m3u8url):
            for f in files:
                file = os.path.join(root, f)
                if os.path.isfile(file):
                    if file.split('.')[-1] == 'm3u8':
                        m3u8download(m3u8url=file)
        sys.exit(0)
    if os.path.isfile(m3u8url):
        title = m3u8url.split('/')[-1].split('.')[-2]
        m3u8download(m3u8url=m3u8url,title=title)
        sys.exit(0)
    title,durations,count,temp_dir,data,method = parser.Parser(m3u8url,title,method=method,key=key,iv=iv,work_dir=work_dir,headers=headers).run()
    tm = time.strftime("%H:%M:%S", time.gmtime(durations))
    print(title,tm)
    segments = json.loads(data)['segments']

    infos = []
    for segment in segments:
        name = segment['title'] + '.ts'
        uri = segment['uri']
        info1 = {
            'title': temp_dir +'/video/'+name,
            'link': uri
        }
        if 'key' in segment:
            info1['method'] = method
            info1['key'] = base64.b64decode(segment['key']['uri'])
            info1['iv'] = bytes.fromhex(segment['key']['iv'])

        infos.append(info1)

    download.FastRequests(infos,threads=threads,headers=headers).run() # 下载

    # 下载完成，开始合并
    merge.Merge(temp_dir,mode=merge_mode)
    # 删除多余文件
    if enable_del:
        delFile.del_file(temp_dir)
    print()


if __name__ == '__main__':
    # pass
    m3u8url = 'https://hls.videocc.net/5cea6c5252/8/5cea6c52523dfd35f3b63b22f0aa3c78_3.m3u8'
    m3u8download(m3u8url,key='j/ZwmOskMzcHIUTbr2IHUw==',title='2021-05-16-西瓜')
