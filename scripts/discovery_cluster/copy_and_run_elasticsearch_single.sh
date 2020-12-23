#!/bin/bash
cp -r /home/haque.s/elasticsearch-7.10.1 /srv/tmp/elasticsearch-7.10.1;
sleep 5;
/srv/tmp/elasticsearch-7.10.1/bin/elasticsearch -d -p /srv/tmp/elasticsearch-7.10.1/pid;