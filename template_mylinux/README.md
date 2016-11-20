---
layout: post
title:
subtitle:
date: 2016-11-07 14:42:31
category:
author: meetbill
tags:
   -
---
template_MyLinux

* [安装](#安装)
* [检验](#检验)
* [原理](#原理)

## 安装

**agent**

install中安装执行install.sh

**server**

* 导入templates的模板

* 对要监控的机器关联templates模板(Template OS MyLinux)

## 检验

在agent上查看检测结果
```
mount | awk '{print $NF}'|cut -c 2-3|awk '{if($1~/ro/) {print 0}}'|wc -l|awk '{if($1<=0) {print 1 } else {print 0}}'
```
输出1则说明分区为可读写，如果输出0则说明磁盘为只读状态

## 原理

* templates中包括了要监控机器要监控的指标及报警条件，导入后关联要监控的主机即可
* install里面安装的程序是可以使agent采集到要监控的数据

mount 命令会输出分区的可读写情况最后的，ro就表示只读，如果是可读写，就是rw

```
[root@Linux ~]# mount 
/dev/mapper/vg_linux-lv_root on / type ext4 (rw)
proc on /proc type proc (rw)
sysfs on /sys type sysfs (rw)
devpts on /dev/pts type devpts (rw,gid=5,mode=620)
tmpfs on /dev/shm type tmpfs (rw)
/dev/sda1 on /boot type ext4 (rw)
none on /proc/sys/fs/binfmt_misc type binfmt_misc (rw)
/dev/sdb on /data4 type ext4 (ro)
```
