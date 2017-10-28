## template_mongodb
<!-- vim-markdown-toc GFM -->
* [1 安装](#1-安装)
* [2 检验](#2-检验)
* [3 原理](#3-原理)
* [4 运维修改](#4-运维修改)
* [5 说明](#5-说明)

<!-- vim-markdown-toc -->


## 1 安装
**agent**

install 中安装执行 install.sh

修改 agent 检测程序中 mongo 客户端位置

/usr/lib/zabbix/externalscripts/mdb_sstat.py
```
pbinpaths = [
            "/opt/mongodb/bin/mongo",
           "/home/mongodb/mongodb/bin/mongo",
            ]

```

**server**

* 导入 templates 的模板

* 对要监控的机器关联 templates 模板

## 2 检验

获取本机器 mongodb 所有信息
```
/usr/lib/zabbix/externalscripts/mdb_sstat.py -a
```

## 3 原理

* install 里面安装的程序是可以使 agent 采集到要监控的数据
* templates 中包括了要监控机器要监控的指标及报警条件，导入后关联要监控的主机即可

## 4 运维修改

(1) 本程序默认设置 AllowRoot=1，即允许使用 root 身份运行 zabbix-agent

若需要使用普通用户运行，则需要以下设置

在 sudoers 中添加 zabbix 用户
```
echo "zabbix ALL=(root) NOPASSWD:/bin/netstat" > /etc/sudoers.d/zabbix
echo 'Defaults:zabbix   !requiretty'  >>  /etc/sudoers.d/zabbix
chmod 600  /etc/sudoers.d/zabbix
```
更改 /usr/lib/zabbix/externalscripts/mdb_sstat.py
```

将 cmdstr = "netstat  -nlpt | grep '%s' | awk '{print $4}'|awk -F: '{print $2}'|uniq" % (binname)
修改为：cmdstr = "sudo netstat  -nlpt | grep '%s' | awk '{print $4}'|awk -F: '{print $2}'|uniq" % (binname)
```

(2) 如果连接 MongoDB 需要账号密码，则需要配置端口、账号、密码的对应关系，配置文件路径如下：

/usr/local/public-ops/conf/.mongodb.passwd

内容如下：
27017 test xxxxx

(3) 程序默认为只汇报指定端口 mongodb

旧版程序每次检测时会通过 netstat  -nlpt | grep '%s' | awk '{print $4}'|awk -F: '{print $2}'|uniq 进行检测所有实例的 mongodb 端口

即可以自动检测多实例 mongodb, 即 agent 机器上跑着多个 mongodb 实例

某些机器的机器数连接过多的时候，会导致程序执行超时，故默认为手动进行配置需要监控的 mongodb 的端口

修改方式如下：

/usr/lib/zabbix/externalscripts/mdb_sstat.py

```
port_list=[27017]
```

## 5 说明

> * 检测时间：2m
> * history 保留时间：7d
> * trend 保留时间：365d

