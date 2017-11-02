## template_raid

<!-- vim-markdown-toc GFM -->
* [1 安装](#1-安装)
* [2 检验](#2-检验)
* [3 原理](#3-原理)
* [4 版本](#4-版本)
* [5 相关项目](#5-相关项目)

<!-- vim-markdown-toc -->

## 1 安装

template_raid

**agent**

install 中安装执行 install.sh

**server**

* 导入 templates 的模板

* 对要监控的机器关联 templates 模板

## 2 检验

在 agent 上查看检测到的硬盘标号
```
/usr/lib/zabbix/externalscripts/raid.py pd_discovery
```

## 3 原理

* install 里面安装的程序是可以使 agent 采集到要监控的数据
* templates 中包括了要监控机器要监控的指标及报警条件，导入后关联要监控的主机即可

## 4 版本

* v1.0.2 : 优化执行速度

## 5 相关项目

* raid 终端查看工具 [megacli_tui](https://github.com/BillWang139967/megacli_tui)
