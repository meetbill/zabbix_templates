# zabbix_templates

## 简介

zabbix常用模板

1.需要导入xxx.xml模板文件。

2.在被监控机上部署收集数据的程序

这里主要汇总了一些在使用zabbix过程中经常用的监控模板。

zabbix template 分为以下3类

+ 硬件层

+ 系统层OS

+ 应用层App

## 模板

硬件层

> * [raid](template_raid/)

系统层

> * [Mylinux](./template_mylinux/)

应用层

> * [mysql](./template_mysql/)
> * [redis](./template_redis/)
> * [mongodb](./template_mongodb/)

## 参加步骤
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
