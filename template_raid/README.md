## template_raid

<!-- vim-markdown-toc GFM -->
* [1 安装](#1-安装)
* [2 检验](#2-检验)
* [3 原理](#3-原理)

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
