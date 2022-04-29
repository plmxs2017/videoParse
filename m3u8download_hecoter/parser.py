import m3u8
import os, re, json, sys
from rich.table import Table
from rich.console import Console
import m3u8download_hecoter
from m3u8download_hecoter import decrypt
from m3u8download_hecoter.decrypt_plus import Decrypt_plus


class Parser:
    def __init__(
            self, m3u8url, title='',base_uri_parse='',method=None, key=None, iv=None, work_dir='./Downloads', headers=None):

        if not os.path.exists(work_dir):
            os.makedirs(work_dir)

        if title == '':
            title = m3u8url.split('?')[0].split('/')[-1].replace('.m3u8', '')

        self.title = self.check_title(title)
        self.temp_dir = work_dir + '/' + title

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        if not os.path.exists(self.temp_dir + '/video'):
            os.makedirs(self.temp_dir + '/video')
        if not os.path.exists(self.temp_dir + '/audio'):
            os.makedirs(self.temp_dir + '/audio')

        self.m3u8url = m3u8url
        self.headers = headers
        self.method = method
        self.key = key
        self.iv = iv
        self.work_dir = work_dir
        self.durations = 0
        self.count = 0
        self.base_uri_parse = base_uri_parse

    def resume(self, List1):
        table = Table()
        console = Console(color_system='256', style=None)
        List2 = []
        if List1 == []:
            print('列表获取错误')
            return
        i = 0
        table.add_column(f'[red]序号')
        table.add_column(f'[red]名称')
        table.add_column(f'[red]清晰度')
        table.add_column(f'[red]链接')
        for List in List1:
            # print("{:>3}  {:<30} {:<10}{:<50}".format(i,List['title'],List['resolution'],List['m3u8url']))
            table.add_row(str(i),List['title'],List['resolution'],List['m3u8url'])
            # print('{:^8}'.format(i), List['Title'],List['play_url'])
            i = i + 1
        console.print(table)
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


    def run(self):

        # preload

        if 'xet.tech' in self.m3u8url:
            self.m3u8url = Decrypt_plus().xiaoetong(m3u8url=self.m3u8url)
        elif 'huke88.com' in self.m3u8url:
            (self.m3u8url,self.key) = Decrypt_plus().DecodeHuke88Key(m3u8url=self.m3u8url)
        m3u8obj = m3u8.load(uri=self.m3u8url, headers=self.headers, verify_ssl=False)
        segments = m3u8obj.data['segments']



        if m3u8obj.data['playlists'] != []:
            infos = []

            print('检测到大师列表，构造链接……')
            playlists = m3u8obj.data['playlists']
            # 央视视频高画质特殊处理
            if self.base_uri_parse == 'https://hls.cntv.myhwcdn.cn':
                _720_playlist = playlists[-1]
                _1080_playlist = {'uri': '', 'stream_info': {'program_id': '', 'bandwidth': '', 'resolution': ''}}
                _1080_playlist['uri'] = _720_playlist['uri'].replace('/1200','/2000')
                _1080_playlist['stream_info']['resolution'] = '1920x1080'
                playlists.append(_1080_playlist)

            for playlist in playlists:
                info = {
                    'm3u8url':self.base_uri_parse + playlist['uri'] if playlist['uri'][:4] != 'http' else playlist['uri'],
                    'title':self.title +'_' + playlist['uri'].split('/')[-1].replace('.m3u8',''),
                    'base_uri_parse':self.base_uri_parse,
                    'resolution':playlist['stream_info']['resolution']
                }

                infos.append(info)


            # 视频之后的其他文件
            if m3u8obj.data['media'] != []:
                medias = m3u8obj.data['media']
                print('media["url"] : ',medias['uri'])

                for media in medias:
                    info = {
                        'm3u8url':self.base_uri_parse + media['uri'] if media['uri'][:4] != 'http' else media['uri'],
                        'title':self.title +'_' + media['uri'].split('/')[-1].replace('.m3u8',''),
                        'base_uri_parse': self.base_uri_parse
                    }
                    infos.append(info)
            infos = self.resume(infos)
            m3u8download_hecoter.m3u8download(infos)

            sys.exit(0)

        if 'key' in segments[0]:
            self.method, segments = decrypt.Decrypt(m3u8obj, self.temp_dir, method=self.method, key=self.key,
                                                    iv=self.iv).run()
        self.count = len(segments)



        for i, segment in enumerate(segments):
            # 计算时长
            if 'duration' in segment:
                self.durations += segment['duration']

            if 'http' != segment['uri'][:4]:
                if segment['uri'][:2] == '//':
                    segment['uri'] = 'https:' + segment['uri']
                else:

                    segment['uri'] = m3u8obj.base_uri + segment['uri']

                segments[i]['uri'] = segment['uri']
            segment['title'] = str(i).zfill(6)
            segments[i]['title'] = segment['title']


        data = json.dumps(m3u8obj.data, indent=4,default=str)

        with open(f'{self.work_dir}/{self.title}/meta.json', 'w', encoding='utf-8') as f:
            f.write(data)
        # 写入raw.m3u8
        raw = m3u8obj.dumps()
        with open(self.work_dir + '/' + self.title + '/' + 'raw.m3u8', 'w', encoding='utf-8') as f:
            f.write(raw)

        return self.title, self.durations, self.count, self.temp_dir, data, self.method

    def check_title(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title
