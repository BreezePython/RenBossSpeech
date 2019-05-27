# -*- coding: utf-8 -*-
# @Author   : 王翔
# @JianShu  : 清风Python
# @Date     : 2019/5/27 21:10
# @Software : PyCharm
# @version  ：Python 3.6.8
# @File     : speech.py

import os
import re
from aip import AipSpeech
import threading
import time


class FileToVoice:
    """
    将用户指定的文件(夹)中的文本内容，转化为语音
    """
    SIZE = 1024  # 百度aip单次转化长度限制

    def __init__(self):
        # AipSpeech秘钥，个人需单独修改...
        app_id = ''
        api_key = ''
        secret_key = ''
        self.client = AipSpeech(app_id, api_key, secret_key)
        func = self.read_dir()
        if func:
            func()

    def read_dir(self):
        """
        判断路径类型
        """
        if os.path.isdir(StartPath):
            # 返回文件夹遍历方法
            return self.ergodic_dir
        elif os.path.isfile(StartPath):
            self.change_file(StartPath)
        else:
            raise TypeError("未找到需要转化的文件(夹)...")

    def ergodic_dir(self):
        """
        百度API的转换速度基本为1000字12秒
        启用多线程并发，加快转换速度。
        """
        for root, dirs, files in os.walk(StartPath):
            base_dir = os.path.join(SavePath, os.path.split(root)[1])
            try:
                os.mkdir(base_dir)
            except FileExistsError:
                pass
            for file in files:
                filepath = os.path.join(root, file)
                t = threading.Thread(target=self.change_file, args=(filepath, base_dir))
                t.start()
                time.sleep(0.2)

    def change_file(self, file, base_dir='', per=3):
        try:
            sem.acquire()
            with open(file, 'r', encoding='utf-8') as f:
                mp3 = bytes()
                while True:
                    index = f.read(self.SIZE)
                    if not index:
                        break
                    _index = re.sub(r'!?\[[^\]]+\]\([^\)]+\)|[\#\-\>\*]*', '', index)
                    reult = self.client.synthesis(_index, 'zh', 1, {'vol': 5, 'per': per})
                    mp3 += reult
                # 获取文件名称并拼接MP3文件名
                file_name = '%s.mp3' % os.path.splitext(os.path.split(file)[1])[0]
                # 合并最终文件归档地址
                mp3_file = os.path.join(base_dir, file_name)
                with open(mp3_file, 'wb+') as t:
                    t.write(mp3)
                print('系统已转换完成 %s ' % mp3_file)
        except Exception as ErrorInfo:
            print(ErrorInfo)

        finally:
            sem.release()


if __name__ == '__main__':
    StartPath = r'D:\Codes_Repository\Python\RenBossSpeech\RenBoss'
    SavePath = r"F:\Speech\度逍遥"
    try:
        os.mkdir(SavePath)
    except FileExistsError:
        pass
    sem = threading.Semaphore(5)
    main = FileToVoice()
    while threading.active_count() != 1:
        pass
    else:
        print('### FileToVoice Jobs is over!!!###')
