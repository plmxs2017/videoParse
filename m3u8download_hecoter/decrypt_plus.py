import re
import requests
import base64,json
from Crypto.Cipher import AES

class Decrypt_plus:
    def __init__(self):
        pass

    def xiaoetong(self,m3u8url):
        replace_header = ['encrypt-k-vod.xet.tech']
        true_header = '1252524126.vod2.myqcloud.com'
        for i in replace_header:
            if i in m3u8url:
                m3u8url = m3u8url.replace(i, true_header).split('?')[0]
                if m3u8url[-3:] == '.ts':
                    m3u8url = re.sub('_\d+', '', m3u8url).replace('.ts', '.m3u8')
        return m3u8url

    def DecodeHuke88Key(self,m3u8url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71'
        }
        # m3u8url = 'https://video-tx.huke88.com/cb3d3408vodtransgzp1256517420/363a46cd5285890808736808030/voddrm.token.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9~eyJ0eXBlIjoiRHJtVG9rZW4iLCJhcHBJZCI6MTI1NjUxNzQyMCwiZmlsZUlkIjoiNTI4NTg5MDgwODczNjgwODAzMCIsImN1cnJlbnRUaW1lU3RhbXAiOjE2MjcwNTEwOTksImV4cGlyZVRpbWVTdGFtcCI6MjE0NzQ4MzY0NywicmFuZG9tIjoyNzU2NzE4MjQzLCJvdmVybGF5S2V5IjoiNzVkNmVlYWUzZGUxNDgwNWQ5NDdhODU4NmU3ZjE0YzQiLCJvdmVybGF5SXYiOiI0NjcxZGIwYWE3ZWI0YTIzNWJlN2EzMmJmNzE3ZmZkOSIsImNpcGhlcmVkT3ZlcmxheUtleSI6IiIsImNpcGhlcmVkT3ZlcmxheUl2IjoiIiwia2V5SWQiOjAsInN0cmljdE1vZGUiOjB9~g698PBwoPK5mSkIaN9XgeqVzVMtbnwnwTKzcV5rJtSg.video_12_2.m3u8?rlimit=3&sign=b22838015362871788c40f616acef1b3&t=60fafe87&us=1627051095'
        text = m3u8url.split('~')[1]
        if text[-2:] != '==':
            text += '=='
        enc = base64.b64decode(text).decode()

        jObject = json.loads(enc)

        overlayKey = jObject['overlayKey']
        overlayIv = jObject['overlayIv']

        # 得到 key
        m3u8text = requests.get(m3u8url, headers=headers).text
        keyurl = re.findall('URI="(.+?)"', m3u8text)[0]
        encryptkey = requests.get(keyurl).content
        cryptor = AES.new(key=bytes.fromhex(overlayKey), mode=AES.MODE_CBC, iv=bytes.fromhex(overlayIv))

        decryptkey = cryptor.decrypt(encryptkey)
        # base64编码的解密key
        decryptkey = base64.b64encode(decryptkey).decode()
        return (m3u8url, decryptkey)
