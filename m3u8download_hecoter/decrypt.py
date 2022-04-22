import sys
import base64,json,re
import requests


class Decrypt:
    def __init__(self, m3u8obj, temp_dir, method=None, key=None, iv=None, headers=None):
        if headers is None:
            self.headers = {'user-agent',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030532) Edg/100.0.4896.60'}
        self.m3u8obj = m3u8obj
        self.segments = m3u8obj.data['segments']
        if method is None:
            self.method = self.segments[0]['key']['method']

        self.temp_dir = temp_dir
        self.key = key
        self.iv = iv


    def judge_method(self):
        if self.method == 'AES-128':
            self.mode_AES_128()
        elif self.method == 'SAMPLE-AES-CTR':
            self.mode_SAMPLE_AES_CTR()
        elif self.method == 'KOOLEARN-ET':
            self.mode_KOOLEARN_ET()
        elif self.method == 'Widevine':
            self.mode_Widevine()
        else:
            self.mode_AES_128()

    def mode_AES_128(self):
        self.key = self.dec_key()
        self.iv = self.dec_iv()
        for i, segment in enumerate(self.segments):
            self.segments[i]['key']['uri'] = self.key
            self.segments[i]['key']['iv'] = self.iv

    def mode_SAMPLE_AES_CTR(self):
        init = self.segments[0]['key']['uri']
        with open(self.temp_dir+'.mp4', 'wb') as f:
            f.write(base64.b64decode(init.split(',')[-1]))

    def mode_KOOLEARN_ET(self):
        self.mode_AES_128() # 整合

    def mode_Widevine(self):
        pass

    def dec_key(self):
        # 自定义key
        deckey = ''
        if self.key != None:
            if 'http' in self.key:
                key_temp = requests.get(url=self.segments[0]['key']['uri'], headers=self.headers).content
                deckey = base64.b64encode(key_temp).decode()

            elif '{' in self.key:
                deckeys = re.findall('{.+?}', self.segments[0]['key']['uri'])
                for dk in deckeys:
                    dk = json.loads(dk)
                    index_begin = dk['index'][0]
                    index_end = dk['index'][1]
                    if 1 >= index_begin and 1 <= index_end:
                        return dk['key']
            else:
                # hexkey 转 base64
                deckey = self.key if '=' in self.key else base64.b64encode(bytes.fromhex(self.key)).decode()

        # 文件中含key
        elif 'base64:' in self.segments[0]['key']['uri']:
            deckey = re.findall('base64:(.+)', self.segments[0]['key']['uri'])[0]

        elif 'hex:' in self.segments[0]['key']['uri']:
            deckey = base64.b64encode(bytes.fromhex(re.findall('hex:(.+)', self.segments[0]['key']['uri'])[0])).decode()
        # 网络链接
        elif 'http' in self.segments[0]['key']['uri']:
            keyurl = self.segments[0]['key']['uri']
            key_temp = requests.get(url=keyurl).content
            deckey = base64.b64encode(key_temp).decode()


        elif self.segments[0]['key']['uri'][0] == '/':
            self.segments[0]['key']['uri'] = self.m3u8obj.base_uri[:-1] + self.segments[0]['key']['uri']
            key_temp = requests.get(url=self.segments[0]['key']['uri'], headers=self.headers).content
            deckey = base64.b64encode(key_temp).decode()

        elif '{' in self.segments[0]['key']['uri']:

            deckeys = re.findall('{.+?}',self.segments[0]['key']['uri'])

            for dk in deckeys:
                dk = json.loads(dk)
                index_begin = dk['index'][0]
                index_end = dk['index'][1]
                if 1 >= index_begin and 1 <= index_end:
                    return dk['key']

        else:
            print('The key parsed failed.', 'Exit after 5s.')

            sys.exit(0)

        return deckey
    def dec_iv(self):
        if 'iv' not in self.segments[0]['key']:
            return '00000000000000000000000000000000'
        else:
            iv = self.segments[0]['key']['iv'].split('x')[-1]
            if len(iv) != 32:
                return '00000000000000000000000000000000'
            return iv

    def run(self):
        self.judge_method()
        return self.method,self.segments