# zabbix_templates
<!-- vim-markdown-toc GFM -->
* [1 简介](#1-简介)
* [2 模板](#2-模板)
    * [2.1 硬件层](#21-硬件层)
    * [2.2 系统层](#22-系统层)
    * [2.3 应用层](#23-应用层)
* [3 相关项目](#3-相关项目)
* [4 参加步骤](#4-参加步骤)

<!-- vim-markdown-toc -->

 
## 1 简介

zabbix 常用模板

1. 需要导入 xxx.xml 模板文件。

2. 在被监控机上部署收集数据的程序

这里主要汇总了一些在使用 zabbix 过程中经常用的监控模板。

## 2 模板

### 2.1 硬件层

> * [raid](template_raid/)

### 2.2 系统层

> * [Mylinux](./template_mylinux/)

### 2.3 应用层

> * [mysql](./template_mysql/)
> * [redis](./template_redis/)
> * [mongodb](./template_mongodb/)
> * [es](./template_elasticsearch/)
> * [service](./template_service/)

## 3 相关项目

> * zabbix 安装 -------------------------------------------------[zabbix_install](https://github.com/BillWang139967/zabbix_install)
> * zabbix 报警工具 ---------------------------------------------[zabbix_alert](https://github.com/BillWang139967/zabbix_alert)
> * zabbix 管理工具 ---------------------------------------------[zabbix_manager](https://github.com/BillWang139967/zabbix_manager)

## 4 参加步骤
* 在 GitHub 上 `fork` 到自己的仓库，然后 `clone` 到本地，并设置用户信息。
```
$ git clone https://github.com/BillWang139967/zabbix_templates.git
$ cd zabbix_templates
$ git config user.name "yourname"
$ git config user.email "your email"
```
* 修改代码后提交，并推送到自己的仓库。
```
$ #do some change on the content
$ git commit -am "Fix issue #1: change helo to hello"
$ git push
```
* 在 GitHub 网站上提交 pull request。
* 定期使用项目仓库内容更新自己仓库内容。
```
$ git remote add upstream https://github.com/BillWang139967/zabbix_templates.git
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
$ git push -f origin master
```
