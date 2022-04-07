import m3u8
import os, re, json, sys
from time import strftime, gmtime
from m3u8download_hecoter import decrypt


class Parser:
    def __init__(
            self, m3u8url, title='', method=None, key=None, iv=None, work_dir='./Downloads', headers=None):

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

    def run(self):

        m3u8obj = m3u8.load(uri=self.m3u8url, headers=self.headers, verify_ssl=False)

        segments = m3u8obj.data['segments']

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

        data = json.dumps(m3u8obj.data, indent=4)

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
