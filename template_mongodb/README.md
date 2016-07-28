## 说明

template_raid

**agent**

install中安装执行install.sh

修改agent检测程序中mongo客户端位置

/usr/lib/zabbix/externalscripts/mdb_sstat.py
```
pbinpaths = [
            "/opt/mongodb/bin/mongo",
           "/home/mongodb/mongodb/bin/mongo",
            ]

```

**server**

* 导入templates的模板

* 对要监控的机器关联templates模板

## 检验

获取本机器mongodb所有信息
```
/usr/lib/zabbix/externalscripts/mdb_sstat.py -a
```

## 原理

* install里面安装的程序是可以使agent采集到要监控的数据
* templates中包括了要监控机器要监控的指标及报警条件，导入后关联要监控的主机即可

## 运维修改

(1)本程序默认设置AllowRoot=1，即允许使用root身份运行zabbix-agent

若需要使用普通用户运行，则需要以下设置
```
echo "zabbix ALL=(root) NOPASSWD:/bin/netstat" > /etc/sudoers.d/zabbix
echo 'Defaults:zabbix   !requiretty'  >>  /etc/sudoers.d/zabbix
chmod 600  /etc/sudoers.d/zabbix
```

(2)如果连接MongoDB需要账号密码，则需要配置端口、账号、密码的对应关系，配置文件路径如下：

/usr/local/public-ops/conf/.mongodb.passwd

内容如下：
27017 test xxxxx

(3)本检测程序也可以自动检测多实例mongodb,即agent机器上跑着多个mongodb实例
