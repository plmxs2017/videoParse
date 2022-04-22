import os
import re

import requests
from threading import Thread
from queue import Queue
import time
from Crypto.Cipher import AES
import warnings

warnings.filterwarnings("ignore")
requests.adapters.DEFAULT_RETRIES = 10 # 增加重连次数

q = Queue(100000)
time_start = time.time()
ALL_COUNT = 0
DONE_COUNT = 0

DONE_SIZE = 0


class FastRequests:
    def __init__(
            self,infos,threads=20,headers=None):
        self.threads = threads # 线程数 20
        global ALL_COUNT
        ALL_COUNT = len(infos)
        self.all_count = len(infos)
        for info in infos:
            q.put(info)
        self.headres = headers

    def run(self):
        global ALL_COUNT,DONE_COUNT,DONE_SIZE,time_start
        for i in range(self.threads):
            t = Consumer(self.headres)
            t.start()

        while DONE_COUNT < ALL_COUNT:
            time.sleep(0.01)
        # 下载完后初始化缓存信息
        ALL_COUNT = 0
        DONE_COUNT = 0
        DONE_SIZE = 0
        time_start = time.time()

class Decrypt:
    def __init__(self,method,ts,key,iv=None):
        self.method = method
        self.ts = ts
        self.key = key
        self.iv = iv

    def AES_128_CBC(self):
        cryptor = AES.new(key=self.key, mode=AES.MODE_CBC, iv=self.iv)
        decrypt_ts = cryptor.decrypt(self.ts)
        return decrypt_ts

    def run(self):
        if self.method == 'AES-128':
            ts = self.AES_128_CBC()
        elif self.method == 'SAMPLE-AES-CTR':
            ts = self.ts
        elif self.method == 'KOOLEARN-ET':
            ts = self.AES_128_CBC()
        elif self.method == 'Widevine':
            ts = self.ts
        else:
            ts = self.AES_128_CBC()
        return ts

class Consumer(Thread):
    def __init__(self,headers):
        Thread.__init__(self)
        self.headers = headers
        self.retry_times = 16


    def run(self):
        while True:
            if q.qsize() == 0:
                break
            self.download(q.get())

    def sizeFormat(self, size, is_disk=False, precision=2):

        formats = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        unit = 1000.0 if is_disk else 1024.0
        if not (isinstance(size, float) or isinstance(size, int)):
            raise TypeError('a float number or an integer number is required!')
        if size < 0:
            raise ValueError('number must be non-negative')
        for i in formats:
            size /= unit
            if size < unit:
                return f'{round(size, precision)}{i}'
        return f'{round(size, precision)}{i}'


    def download(self,info):
        global DONE_SIZE
        title = info['title']
        link = info['link']

        if not os.path.exists(title):
            for i in range(self.retry_times):
                try:
                    response = requests.get(url=link, headers=self.headers, stream=True, timeout=30)
                    ts = response.content

                    if 'method' in info:
                        ts = Decrypt(ts=ts, method=info['method'], key=info['key'], iv=info['iv']).run()
                    if ts[:4] == b'\x89PNG' or ts[:2] == bytes.fromhex('424D'):
                        ts_start = ts.find(b'G@')
                        ts = ts[ts_start:]

                    DONE_SIZE += ts.__sizeof__()
                    with open(title, 'wb') as f:
                        # for chunk in response.iter_content(chunk_size=1024):
                        #     if chunk:
                        #         f.write(chunk)
                        f.write(ts)
                        f.close()

                    if response.status_code == 200:
                        break
                except requests.exceptions.RequestException as e:
                    continue


            # if not os.path.exists(title):
            #     self.download(info)

        global DONE_COUNT
        DONE_COUNT += 1
        end_time = time.time()
        speed = DONE_SIZE/(end_time-time_start)
        # 简化的进度条
        if speed != 0:
            eta = int((end_time - time_start) * (ALL_COUNT-DONE_COUNT) / DONE_COUNT)
        else:
            eta = 0
        print(f'\r  process:[{DONE_COUNT}/{ALL_COUNT}] [{self.sizeFormat(DONE_SIZE)}/{self.sizeFormat((DONE_SIZE/DONE_COUNT)*ALL_COUNT)}] {round((DONE_COUNT/ALL_COUNT)*100,2)}% speed:{self.sizeFormat(speed)}/s eta:{time.strftime("%H:%M:%S", time.gmtime(eta))}',end='')


