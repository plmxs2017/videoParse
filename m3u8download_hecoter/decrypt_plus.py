import re

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
