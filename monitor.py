import cv2
import os
import yaml
from datetime import datetime
import pygame
import sys
from organize_email import send_mail
from multiprocessing import Process
from tqdm import trange


def process_mail(video_path):
    """单独开启一个线程来进行邮件的发送"""
    import time

    if not os.path.exists(video_path):
        # 如果视频不存在
        print("捕获视频不存在")
        video_path = None
    # 读取配置文件
    yaml_file = open(
        sys.path[0] + "/configuration/configuration.yaml", "r", encoding="utf-8"
    )  # 打开
    yaml_dict = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)  # 用load转字典
    # 开始发送邮件
    print(datetime.now(), "开始发送邮件")
    send_mail(
        yaml_dict["sender"],
        yaml_dict["password"],
        yaml_dict["recipient"],
        "MovingEye",
        time.strftime("%Y-%m-%d %H:%M:%S") + "有物体移动。",
        mail_host=yaml_dict["mail_host"],
        file=video_path,
    )
    print(datetime.now(), "邮件发送成功")


def monitor():
    """开启移动物体的监测"""
    import time

    # 定义摄像头对象，其参数0表示第一个摄像头
    camera = cv2.VideoCapture(0)
    # 设置一下帧数和前背景
    fps = 5
    pre_frame = None
    while 1:
        print(f"监测中：{datetime.now()}")
        start = time.time()
        # 读取视频流
        ret, frame = camera.read()
        # 转灰度图
        gray_pic = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if not ret:
            print("打开摄像头失败")
            break
        end = time.time()
        # 运动检测部分,看看是不是5FPS
        seconds = end - start
        if seconds < 1.0 / fps:
            time.sleep(1.0 / fps - seconds)
        gray_pic = cv2.resize(gray_pic, (480, 480))
        # 用高斯滤波进行模糊处理
        gray_pic = cv2.GaussianBlur(gray_pic, (21, 21), 0)
        # 如果没有背景图像就将当前帧当作背景图片
        if pre_frame is None:
            pre_frame = gray_pic
        else:
            # absdiff把两幅图的差的绝对值输出到另一幅图上面来
            img_delta = cv2.absdiff(pre_frame, gray_pic)
            # threshold阈值函数(原图像应该是灰度图,对像素值进行分类的阈值,当像素值高于（有时是小于）阈值时应该被赋予的新的像素值,阈值方法)
            thresh = cv2.threshold(img_delta, 30, 255, cv2.THRESH_BINARY)[1]
            # 用一下腐蚀与膨胀
            thresh = cv2.dilate(thresh, None, iterations=2)
            # findContours检测物体轮廓(寻找轮廓的图像,轮廓的检索模式,轮廓的近似办法)
            contours, hierarchy = cv2.findContours(
                thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            is_moving_object = False
            for c in contours:
                # 设置敏感度
                # contourArea计算轮廓面积
                if cv2.contourArea(c) > 1000:
                    is_moving_object = True
            if is_moving_object:
                # 发现移动的物体
                print(f"{datetime.now()}--->有物体移动！！！")
                # 播放报警声
                # 音频初始化
                pygame.mixer.init()
                # 载入音频
                pygame.mixer.music.load(sys.path[0] + "/music/alarm.mp3")
                # 播放音频
                pygame.mixer.music.play()
                # 目录不存在则创建目录
                if not os.path.isdir(sys.path[0] + "/capture"):
                    os.mkdir(sys.path[0] + "/capture")

                fps_viedo = 20

                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                # 视频size
                size = (
                    int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                )
                # 打开和设置道具
                vout = cv2.VideoWriter()
                vout.open("capture/capture.mp4", fourcc, fps_viedo, size, True)
                print(datetime.now(), "开始录像")
                # 录制400张帧图片
                for i in trange(400):
                    _, frame = camera.read()
                    cv2.putText(
                        frame,
                        str(i),
                        (10, 20),
                        cv2.FONT_HERSHEY_PLAIN,
                        1,
                        (0, 255, 0),
                        1,
                        cv2.LINE_AA,
                    )
                    vout.write(frame)
                vout.release()
                print(datetime.now(), "录像结束")
                p = Process(
                    target=process_mail, args=(sys.path[0] + "/capture/capture.mp4",)
                )
                p.start()
                pre_frame = None
            else:
                # 未发现移动的物体
                pre_frame = gray_pic


if __name__ == "__main__":
    print(
        """
       _____              .__              ___________             
  /     \   _______  _|__| ____    ____\_   _____/__.__. ____  
 /  \ /  \ /  _ \  \/ /  |/    \  / ___\|    __)<   |  |/ __ \ 
/    Y    (  <_> )   /|  |   |  \/ /_/  >        \___  \  ___/ 
\____|__  /\____/ \_/ |__|___|  /\___  /_______  / ____|\___  >
        \/                    \//_____/        \/\/         \/ 
MovingEye
Author : red-fox-yj
Github address : https://github.com/red-fox-yj/MovingEye_OpenSource.git
    """
    )
    monitor()
