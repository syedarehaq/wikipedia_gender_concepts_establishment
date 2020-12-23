# Parallel search of concepts using Elasticsearch in Discovery cluster

## Install Elastic
[Elastic installation link](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html)
```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.1-linux-x86_64.tar.gz
cp elasticsearch-7.10.1-linux-x86_64.tar.gz /srv/
tar -xzf /srv/elasticsearch-7.10.1-linux-x86_64.tar.gz 
module load oracle_java/jdk1.8.0_181
curl -XGET "127.0.0.1:9200"
python3 04_01_01_elastic_bulk_index.py --index wikipedia-20200820 --port 9200 --filename /work/nelsongroup/haque.s/wikipedia/enwiki-20200820-pages-articles-multistream.json --bulksize 100
```

```
ssh c3178
cd /srv/tmp
curl -XGET "http://localhost:9200/_cat/indices?v"
curl -XDELETE "http://localhost:9200/wikipedia-20200820"
pkill -F /srv/tmp/elasticsearch-7.10.1/pid
rm -rf /srv/tmp/elasticsearch-7.10.1
```

```
module load python/3.8.1
source /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/venv/bin/activate
python3 /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/scripts/04_01_01_elastic_bulk_index.py --index wikipedia-20200820 --port 9200 --filename /work/nelsongroup/haque.s/wikipedia/enwiki-20200820-pages-articles-multistream.json --bulksize 100
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

Need to run the follwing script  after CD into the repo/scrips/discvoery_cluster directory
```
bash create_all_exclusive_nodes_using_screen.sh
```
Then 
```
bash copy_and_run_elasticsearch_all.sh
```