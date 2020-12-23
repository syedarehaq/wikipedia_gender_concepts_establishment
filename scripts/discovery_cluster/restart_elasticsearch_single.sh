#!/bin/bash
pkill -F /srv/tmp/elasticsearch-7.10.1/pid;
/srv/tmp/elasticsearch-7.10.1/bin/elasticsearch -d -p /srv/tmp/elasticsearch-7.10.1/pid;