## template_raid

<!-- vim-markdown-toc GFM -->
* [1 使用](#1-使用)
    * [1.1 安装](#11-安装)
    * [1.2 检验](#12-检验)
        * [1.2.1 agent 端检验](#121-agent-端检验)
        * [1.2.2 server 端检验](#122-server-端检验)
* [2 原理](#2-原理)
    * [2.1 megacli](#21-megacli)
    * [2.2 监控值说明](#22-监控值说明)
* [3 版本](#3-版本)
* [4 相关项目](#4-相关项目)

<!-- vim-markdown-toc -->

## 1 使用

### 1.1 安装

**agent**

install 中安装执行 install.sh

**server**

* 导入 templates 的模板

* 对要监控的机器关联 templates 模板

### 1.2 检验
#### 1.2.1 agent 端检验
在 agent 上查看检测到的硬盘标号
```
/usr/lib/zabbix/externalscripts/raid.py pd_discovery
```
#### 1.2.2 server 端检验
```
zabbix_get -s 10.20.129.183 -k raid.phy.discovery
```
将其中 IP 更换为对应 IP 即可

## 2 原理

* install 里面安装的程序是可以使 agent 采集到要监控的数据
* templates 中包括了要监控机器要监控的指标及报警条件，导入后关联要监控的主机即可

### 2.1 megacli 

megacli 程序需要 sudo 权限执行

### 2.2 监控值说明

> * 监控项应用名为`MegaRAID`
> * 物理磁盘使用`/opt/MegaRAID/MegaCli/MegaCli64 -PDList -aALL -nolog` 中的 `Device Id` 作为标识符
> * 逻辑磁盘使用`/opt/MegaRAID/MegaCli/MegaCli64 -LDInfo -Lall -aALL -nolog` 中的 `Virtual Drive`作为标识符

|监控项|key|更新时间|历史数据保留时间|趋势数据保留时间|触发器|
|---|---|---|---|---|---|
|物理磁盘状态|raid.phy.fw_state[{#DISK_ID}]|1m|7d|365d|Unconfigured(bad),Failed(连续3次)
|物理磁盘mec|raid.phy.mec[{#DISK_ID}]|2m|7d|365d|>30(连续3次)|
|物理磁盘oec|raid.phy.oec[{#DISK_ID}]|2m|7d|365d|>1000(连续3次)|
|物理磁盘pfc|raid.phy.pfc[{#DISK_ID}]|2m|7d|365d|>2(连续3次)|
|逻辑磁盘状态|raid.ld.state[{#LD_ID}]|1m|7d|365d|不是Optimal状态(连续3次)|

## 3 版本

* v1.0.3 20171104: 添加对逻辑磁盘的监控
* v1.0.2 --------: 优化执行速度

## 4 相关项目

* raid 终端查看工具 [megacli_tui](https://github.com/BillWang139967/megacli_tui)
