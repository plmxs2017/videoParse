import os


class Merge:
    def __init__(self,temp_dir:str,mode=3):
        self.temp_dir = temp_dir

        self.file_list = []
        for root, dirs, files in os.walk(temp_dir+r'\video'):
            for f in files:
                file = os.path.join(root, f)
                if os.path.isfile(file):
                    self.file_list.append(file)

        if mode == 1:
            self.mode1()
        elif mode == 2:
            self.mode2()
        elif mode == 3:
            self.mode3()
        else:
            print('合并方式输入错误！进行二进制合并中……')

    # 直接二进制合并
    def mode1(self):
        with open(self.temp_dir+'.mp4','ab') as f1:
            for i in self.file_list:
                with open(i,'rb') as f2:
                    f1.write(f2.read())
                    f2.close()
            f1.close()


    # 先二进制合并再 ffmpeg 转码
    def mode2(self):
        if not os.path.exists(self.temp_dir + "_ffmpeg.mp4"):
            self.mode1()
            try:
                cmd = 'ffmpeg -loglevel panic'
                os.system(cmd)

                cmd = f'ffmpeg -i "{self.temp_dir + ".mp4"}" -c copy "{self.temp_dir + "_ffmpeg.mp4"}" -loglevel panic'
                os.system(cmd)

            except:
                print('未找到 ffmpeg ')

    # 直接 ffmpeg 合并
    def mode3(self):
        if not os.path.exists(self.temp_dir + ".mp4"):
            try:
                cmd = 'ffmpeg -loglevel panic'
                os.system(cmd)
                filelist = [f"file './video/{str(i).zfill(6)}.ts'" for i in range(len(self.file_list))]
                with open(self.temp_dir + '/filelist.txt','w') as f:
                    for i in filelist:
                        f.write(i)
                        f.write('\n')
                    f.close()
                cmd = f'ffmpeg -f concat -safe 0 -i "{self.temp_dir + "/filelist.txt"}" -c copy "{self.temp_dir + ".mp4"}" -loglevel panic'
                os.system(cmd)

            except:
                print('未找到 ffmpeg ')



