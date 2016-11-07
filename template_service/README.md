## 说明

template_service_old

使用低层次自动发现，因为需要在agent上设置环节，相对来说不好管理

**agent**

install中安装执行install.sh

**server**

* 导入templates的模板

* 对要监控的机器关联templates模板

## 原理

* install里面安装的程序是可以使agent采集到要监控的数据
* templates中包括了要监控机器要监控的指标及报警条件，导入后关联要监控的主机即可


