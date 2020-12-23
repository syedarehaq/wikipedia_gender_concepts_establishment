#!/bin/bash
nodename=$1
echo $nodename;
srun --pty --export=ALL --tasks-per-node 16 --nodes 1 --mem=100Gb --partition=netsi_standard --nodelist=$nodename --exclusive /bin/bash;
cp -r /home/haque.s/elasticsearch-7.10.1 /dev/shm/elasticsearch-7.10.1
./srv/elasticsearch-7.10.1/bin/elasticsearch -d -p /srv/elasticsearch-7.10.1/pid
exec sh