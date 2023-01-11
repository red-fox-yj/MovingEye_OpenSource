# MovingEye（开源版）

<img src="https://raw.githubusercontent.com/red-fox-yj/MarkDownPic/main/typora/MovingEye.jpg" alt="MovingEye" style="zoom: 18%;" />

- [MovingEye](#movingeye)
  - [简介](#简介)
  - [开发时硬件环境](#开发时硬件环境)
  - [开发时软件环境](#开发时软件环境)
  - [快速开始](#快速开始)
  - [疑难解答](#疑难解答)
    - [树莓派ubuntu无法安装pygame](#树莓派ubuntu无法安装pygame)
    - [树莓派ubuntu连接wifi](#树莓派ubuntu连接wifi)
    - [树莓派配置摄像头](#树莓派配置摄像头)
      - [1.在ubuntu server上安装raspi-config](#1在ubuntu-server上安装raspi-config)
      - [2.设置raspi-config](#2设置raspi-config)
    - [opencv-python问题](#opencv-python问题)

## 简介

部署在树莓派4B上实现移动物体的实时监控。当移动物体进入树莓派摄像头的视野时，树莓派会发出连续的报警提示音，同时会将移动物体拍照后保存为图片以邮件附件的方式发送给事先指定好的邮箱地址。当移动物体从树莓派摄像头视野中消失时则会停止报警。更多内容请参考：点我[http://mjvvv.cn/#/blogBrowse?blogId=30]

## 开发时硬件环境
- 树莓派4B，内存2GB；
- 树莓派专用摄像头一个；
- 扬声器一个。

## 开发时软件环境
Ubuntu Server 20.04.2 LTS（RPi 2/3/4/400）64位

## 快速开始

树莓派烧录好ubuntu系统，配置好网络和摄像头（配置方法可见下文**疑难解答**），连接扬声器。

克隆项目到你树莓派的工作目录，`cd`进入项目根目录。

```
# 克隆
×××@×××:~$ git clone https://github.com/red-fox-yj/MovingEye_OpenSource.git
# 切换目录
×××@×××:~$ cd MovingEye_OpenSource
```

利用`vim`编辑`configuration/configuration.yaml`，输入发送者邮箱地址、邮箱服务器密码、邮箱服务器、接收者邮箱地址（邮件服务器的配置较为简单，可以自行谷歌，这里不再赘述）。

```
# vim编辑
×××@×××:~$ vim configuration.yaml
```

运行`monitor.py`。

```
×××@×××:~$ python3 monitor.py
```

遇到缺少python依赖时可以利用`pip`工具下载安装。

```
×××@×××:~$ pip install 模块名
```

## 疑难解答
### 树莓派ubuntu无法安装pygame

正确指令应该为

```
sudo apt-get install python3-pygame
```

### 树莓派ubuntu连接wifi

修改`/etc/netplan/50-cloud-init.yaml`，修改后的文件如下：

```
# This file is generated from information provided by the datasource.  Changes
# to it will not persist across an instance reboot.  To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    ethernets:
        eth0:
            dhcp4: true
            optional: true
    version: 2

    wifis:
        wlan0:
            dhcp4: true
            access-points:
                "wifi的帐户名":
                    password: "wifi密码"
```

配置生效：

```
ubuntu@ubuntu:~$ sudo netplan try
ubuntu@ubuntu:~$ sudo netplan apply
```

### 树莓派配置摄像头

#### 1.在ubuntu server上安装raspi-config
启动摄像头需要用到官方的raspi-config配置程序，进入官网地址，下载最新的deb程序。

```
wget http://archive.raspberrypi.org/debian/pool/main/r/raspi-config/raspi-config_20200817_all.deb
```

然后安装：

```
sudo dpkg -i raspi-config_20200817_all.deb
```

发现有依赖报错，修复依赖：

```
sudo apt --fix-broken install
```

然后再重新安装。

#### 2.设置raspi-config
启动raspi-config

```
sudo raspi-config
```

选择第5项，交互设置：

![在这里插入图片描述](https://raw.githubusercontent.com/red-fox-yj/MarkDownPic/main/typora/20200902000640766.png)

选择第1项：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200902000717985.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3NpbmF0XzI1MjU5NDYx,size_16,color_FFFFFF,t_70#pic_center)

如果出现固件过时的错误时：

> Your firmwave appears to be out of date (no start_x.elf). Please update

解决方法：

1.查看boot分区所在的设备号，设备号可能是：/dev/mmcblk0p1

```
df -h
```

2将该设备号挂载在/boot上

```
mount /dev/mmcblk0p1 /boot
```

完美解决
随后会出现是否设置为enabled，选择yes。

![在这里插入图片描述](https://raw.githubusercontent.com/red-fox-yj/MarkDownPic/main/typora/2020090200125073.png)

等待树莓派重启。
重启后检查是否有摄像头设备：

```
ls -al /dev/ | grep video
```

如下图：

![在这里插入图片描述](https://raw.githubusercontent.com/red-fox-yj/MarkDownPic/main/typora/20200902002011257.png)

安装完毕。

### opencv-python问题

报错

> Traceback (most recent call last):
>   File "monitor_ubuntu.py", line 1, in <module>
>     import cv2
>   File "/usr/local/lib/python3.8/dist-packages/cv2/__init__.py", line 5, in <module>
>     from .cv2 import *
> ImportError: libGL.so.1: cannot open shared object file: No such file or directory

先把之前用上面命令安装的opencv删除，使用这条命令：

```
sudo pip uninstall opencv-python
```

然后用这条命令安装：

```
sudo pip install opencv-python-headless
```

这样就问题就解决了。

