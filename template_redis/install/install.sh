# conf
mkdir -p /etc/zabbix/zabbix_agentd.d/
cp conf/redis.conf /etc/zabbix/zabbix_agentd.d/

# scripts
mkdir -p /usr/lib/zabbix/externalscripts/
cp conf/redis.py /usr/lib/zabbix/externalscripts/
chmod 777 /usr/lib/zabbix/externalscripts/redis.py

# UnsafeUserParameters=1
CHECK=`grep "^Include=/etc/zabbix/zabbix_agentd.d/" /etc/zabbix/zabbix_agentd.conf|wc -l`
if [[ "w$CHECK" == "w0" ]]
then
    echo 'Include=/etc/zabbix/zabbix_agentd.d/' >> /etc/zabbix/zabbix_agentd.conf
fi

# UnsafeUserParameters=1
CHECK=`grep "^UnsafeUserParameters=1" /etc/zabbix/zabbix_agentd.conf|wc -l`
if [[ "w$CHECK" == "w0" ]]
then
    sed -ri '/UnsafeUserParameters=/a UnsafeUserParameters=1' /etc/zabbix/zabbix_agentd.conf
fi

# Timeout=10
CHECK=`grep "^Timeout=3" /etc/zabbix/zabbix_agentd.conf|wc -l`
if [[ "w$CHECK" == "w0" ]]
then
    sed -ri '/Timeout=3/a Timeout=10' /etc/zabbix/zabbix_agentd.conf
fi

# AllowRoot=1
CHECK=`grep "^AllowRoot=1" /etc/zabbix/zabbix_agentd.conf|wc -l`
if [[ "w$CHECK" == "w0" ]]
then
    sed -ri '/AllowRoot=0/a AllowRoot=1' /etc/zabbix/zabbix_agentd.conf
fi
/etc/init.d/zabbix-agent restart
