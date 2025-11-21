#!/bin/bash

if [ ! -d ./logs ]; then
	mkdir ./logs
fi

if [ ! -d ./confs ]; then
	mkdir ./confs
fi

grep logs ./topo.yml | awk -F":" '{print $1}' | sed 's/- //g' | while read host; do
        touch $host
	chmod 666 $host
done

grep confs ./topo.yml | awk -F":" '{print $1}' | sed 's/- //g' | while read host; do
        echo "log file /var/log/frr.log" >  $host
	echo "log stdout informational" >> $host
	chmod 666 $host
done
