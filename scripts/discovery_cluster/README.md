# Parallel search of concepts using Elasticsearch in Discovery cluster

## Install Elastic
[Elastic installation link](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html)
```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.1-linux-x86_64.tar.gz
cp elasticsearch-7.10.1-linux-x86_64.tar.gz /srv/
tar -xzf /srv/elasticsearch-7.10.1-linux-x86_64.tar.gz 
module load oracle_java/jdk1.8.0_181
curl -XGET "127.0.0.1:9200"
```

```
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1',80))
if result == 0:
   print("Port is open")
else:
   print("Port is not open")
sock.close()
```