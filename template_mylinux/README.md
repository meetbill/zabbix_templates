## template_MyLinux


<!-- vim-markdown-toc GFM -->
* [1 安装](#1-安装)
* [2 检验](#2-检验)
* [3 原理](#3-原理)

<!-- vim-markdown-toc -->
## 1 安装

**agent**

install 中安装执行 install.sh

**server**

* 导入 templates 的模板

* 对要监控的机器关联 templates 模板 (Template OS MyLinux)

## 2 检验

在 agent 上查看检测结果
```
mount | awk '{print $NF}'|cut -c 2-3|awk '{if($1~/ro/) {print 0}}'|wc -l|awk '{if($1<=0) {print 1 } else {print 0}}'
```
输出 1 则说明分区为可读写，如果输出 0 则说明磁盘为只读状态

## 3 原理

* templates 中包括了要监控机器要监控的指标及报警条件，导入后关联要监控的主机即可
* install 里面安装的程序是可以使 agent 采集到要监控的数据

mount 命令会输出分区的可读写情况最后的，ro 就表示只读，如果是可读写，就是 rw

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
