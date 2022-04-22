# python 多线程实例—简易的m3u8下载器

## 介绍

这个是上篇帖子的实际应用 [简易封装的python多线程类 - 『编程语言讨论求助区』 - 吾爱破解 - LCG - LSG |安卓破解|病毒分析|www.52pojie.cn](https://www.52pojie.cn/thread-1615108-1-1.html)

主要用来多线程下载文件，对m3u8链接进行了 解析、下载、解密、合并、删除等操作

## 文件内容：

m3u8download_hecoter

​		__init__.py

​		decrypt.py

​		delFile.py

​		download.py

​		merge.py

​		parser.py

## __init__.py

识别为 python 程序，向里面插入代码也可以在外部直接引用



## decrypt.py

支持 AES_128、SAMPLE-AES-CTR、KOOLEARN-ET、Widevine



## parser.py

解析 m3u8 链接，方便后面传入下载模块



## download.py

实际多线程下载部分，另配有简易进度条

## 	merge.py

下载完成合并部分，有3种合并方式，

1.二进制合并

2.先二进制合并再 ffmpeg 转码

3.直接 ffmpeg 合并

​	默认第三种，其他可自行选择



## delFile.py

删除多余文件

## 使用方法

下载完整代码：https://github.com/hecoter/m3u8download_hecoter 直接调用

```
from m3u8download_hecoter import m3u8download
m3u8download(m3u8url='https://hls.videocc.net/4adf37ccc0/a/4adf37ccc0342e919fef2de4d02b473a_3.m3u8',title='9-第四节  民法典合同编及价格法（二）',work_dir='000',key='kQ2aSmyG1FDSmzpqTso/0w==',enable_del=False)

```

