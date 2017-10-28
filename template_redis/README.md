##  template_redis
<!-- vim-markdown-toc GFM -->
* [1 安装](#1-安装)
* [2 检验](#2-检验)
* [3 原理](#3-原理)
* [4 运维修改](#4-运维修改)
* [5 说明](#5-说明)

<!-- vim-markdown-toc -->

## 1 安装


**agent**

install中安装执行install.sh

修改agent检测程序中redis客户端位置

/usr/lib/zabbix/externalscripts/redis.py
```
pbinpaths = [
            "/usr/local/bin/redis-cli",
            ]

```

**server**

* 导入templates的模板

* 对要监控的机器关联templates模板

## 2 检验

获取本机器redis端口
```
/usr/lib/zabbix/externalscripts/redis.py -l
```
获取本机器redis 使用内存
```
/usr/lib/zabbix/externalscripts/redis.py -p 6379 -k used_memory
```

## 3 原理

* install里面安装的程序是可以使agent采集到要监控的数据
* templates中包括了要监控机器要监控的指标及报警条件，导入后关联要监控的主机即可

## 4 运维修改

(1)本程序默认设置AllowRoot=1，即允许使用root身份运行zabbix-agent

若需要使用普通用户运行，则需要以下设置

在sudoers中添加zabbix用户
```
echo "zabbix ALL=(root) NOPASSWD:/bin/netstat" > /etc/sudoers.d/zabbix
echo 'Defaults:zabbix   !requiretty'  >>  /etc/sudoers.d/zabbix
chmod 600  /etc/sudoers.d/zabbix
```

(2)如果连接redis需要账号密码，则需要配置端口、账号、密码的对应关系，配置文件路径如下：

/usr/local/public-ops/conf/.redis.passwd

内容如下：
6379 passwd

(3)程序默认为只汇报指定端口redis


修改方式如下：

/usr/lib/zabbix/externalscripts/redis.py

```
port_list=[6379]
```

## 5 说明

> * 检测时间：1m
> * history保留时间：14d
> * trend保留时间：365d
