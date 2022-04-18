from __future__ import annotations
# 用于显示进度条
from tqdm import tqdm
# 用于发起网络请求
import requests
# 用于多线程操作
import multitasking
import signal
# 导入 retry 库以方便进行下载出错重试
from retry import retry
signal.signal(signal.SIGINT, multitasking.killall)

requests.packages.urllib3.disable_warnings()
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
# 定义 1 MB 多少为 B
MB = 1024**2


def split(start: int, end: int, step: int) -> list[tuple[int, int]]:
    # 分多块
    parts = [(start, min(start+step, end))
             for start in range(0, end, step)]
    return parts


def get_file_size(url: str, raise_error: bool = False) -> int:
    '''
    获取文件大小

    Parameters
    ----------
    url : 文件直链
    raise_error : 如果无法获取文件大小，是否引发错误

    Return
    ------
    文件大小（B为单位）
    如果不支持则会报错

    '''
    response = requests.head(url,verify=False)
    file_size = response.headers.get('Content-Length')
    if file_size is None:
        if raise_error is True:
            raise ValueError('该文件不支持多线程分段下载！')
        return file_size
    return int(file_size)


def download(url: str, file_name: str = '', retry_times: int = 16, each_size=16*MB) -> None:
    '''
    根据文件直链和文件名下载文件

    Parameters
    ----------
    url : 文件直链
    file_name : 文件名
    retry_times: 可选的，每次连接失败重试次数
    Return
    ------
    None

    '''
    if file_name == '':
        file_name = url.split('/')[-1].split('?')[-2]
    f = open(file_name, 'wb')
    file_size = get_file_size(url)

    @retry(tries=retry_times)
    @multitasking.task
    def start_download(start: int, end: int) -> None:
        '''
        根据文件起止位置下载文件

        Parameters
        ----------
        start : 开始位置
        end : 结束位置
        '''
        _headers = headers.copy()
        # 分段下载的核心
        _headers['Range'] = f'bytes={start}-{end}'
        # 发起请求并获取响应（流式）
        response = session.get(url, headers=_headers, stream=True,verify=False)
        # 每次读取的流式响应大小
        chunk_size = 128
        # 暂存已获取的响应，后续循环写入
        chunks = []
        for chunk in response.iter_content(chunk_size=chunk_size):
            # 暂存获取的响应
            chunks.append(chunk)
            # 更新进度条
            bar.update(chunk_size)
        f.seek(start)
        for chunk in chunks:
            f.write(chunk)
        # 释放已写入的资源
        del chunks

    session = requests.Session()
    # 分块文件如果比文件大，就取文件大小为分块大小
    each_size = min(each_size, file_size)

    # 分块
    parts = split(0, file_size, each_size)
    # 创建进度条
    # bar_format = '{desc}{percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt}[{elapsed}<{remaining}{postfix}]'

    bar_format = '{l_bar}{bar}{r_bar}'
    # 下载文件：amd64.iso:   1%|          | 17655936/3277746176 [00:07<27:48, 1954160.90it/s]

    bar = tqdm(total=file_size, desc=f'下载文件：{file_name}',bar_format=bar_format)
    for part in parts:
        start, end = part
        start_download(start, end)
    # 等待全部线程结束
    multitasking.wait_for_tasks()
    f.close()
    bar.close()


if "__main__" == __name__:
    url = 'https://om.tc.qq.com/gzc_1000102_0b53juaa4aaabyagna233nrmatodbzaqacsa.f10217.mp4?vkey=ECDFE1180F0A3A4C557680CAB24706A3966392F1DE944FA1F892A178BE75447A2BB5B9A98B0470AFB1C0F953E4A6E146901DCA7FC937C84B0B26ABB3F7E8674D460D12B6D032CFBDA9A9119079EBC2CD17157810E278C695CE7CDC70E447119D58D4DE5E8D40583FFCCC8B9814E7DB91D57AC66382AC9075D1B1BE19C0AD294773FFDD3686DF9D0D'
    # 开始下载文件
    download(url)