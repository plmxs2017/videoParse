from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


def calc_divisional_range(filesize, chuck=10):
    step = filesize//chuck
    arr = list(range(0, filesize, step))
    result = []
    for i in range(len(arr)-1):
        s_pos, e_pos = arr[i], arr[i+1]-1
        result.append([s_pos, e_pos])
    result[-1][-1] = filesize-1
    return result

# 下载方法
def range_download(url,save_name, s_pos, e_pos):
    headers = {"Range": f"bytes={s_pos}-{e_pos}"}
    res = requests.get(url, headers=headers, stream=True)
    with open(save_name, "rb+") as f:
        f.seek(s_pos)
        for chunk in res.iter_content(chunk_size=64*1024):
            if chunk:
                f.write(chunk)


def download(url,save_name=None):
    # url = 'http://yue.cmvideo.cn:8080/depository_yqv/asset/zhengshi/5102/598/709/5102598709/media/5102598709_5010999563_56.mp4'
    if save_name is None:
        save_name = url.split('/')[-1]
    print(save_name,'下载中……')
    res = requests.head(url)
    filesize = int(res.headers['Content-Length'])
    divisional_ranges = calc_divisional_range(filesize)

    # 先创建空文件
    with open(save_name, "wb") as f:
        pass
    with ThreadPoolExecutor() as p:
        futures = []
        for s_pos, e_pos in divisional_ranges:
            # print(s_pos, e_pos)
            futures.append(p.submit(range_download,url,save_name, s_pos, e_pos))
        # 等待所有任务执行完毕
        as_completed(futures)
    print(save_name,'下载完成！')

if __name__ == '__main__':
    url = input('输入下载链接：')
    download(url)