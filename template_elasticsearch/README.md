## elasticsearch 监控
查看 es 集群健康状态

```
curl -sXGET 'http://localhost:9200/_cluster/health?pretty'
{
  "cluster_name" : "elasticsearch",
  "status" : "green",            #集群状态：green，yellow，red
  "timed_out" : false,
  "number_of_nodes" : 3,         #集群中 node 节点数
  "number_of_data_nodes" : 2,    #集群中 data 节点数
  "active_primary_shards" : 186,
  "active_shards" : 372,
  "relocating_shards" : 0,       #迁移分片到新的 node
  "initializing_shards" : 0,     #初始化分片
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0
}

```

检测方法
```
curl -s -XGET "http://localhost:9200/_cluster/health?pretty" | grep "status"|awk -F '[ "]+' '{print $4}'|grep -c 'green'
```

## 相关

使用此程序时，假如系统无响应时无法返回结果，可通过以下链接方法避免

[python 调用 shell（超时设置）](https://github.com/BillWang139967/MyPythonLib/blob/master/My_lib/easyrun/README.md)
