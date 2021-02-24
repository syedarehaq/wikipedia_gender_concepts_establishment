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

Allocate a node in exclusive mode just for testing
```
srun --pty --export=ALL --nodes=1 --partition=netsi_standard --nodelist=c3116 --exclusive /bin/bash;

```

### Actual running starts here:

**Caveat: Do not use c3177, you do not have write permission in `/srv/tmp` in c3177, and also right now c3200 in down mode**\
First create a proper list of evailable nodes indiscovery cluster using sinfo and put the names in `available_nodelist.txt`.

Need to run the follwing script  after CD into the `repo/scripts/discvoery_cluster` directory
```
bash create_all_exclusive_nodes_using_screen.sh
```
Then 
```
bash copy_and_run_elasticsearch_all.sh
```
Then first change the corpus name inside `python_search_all.sh`. 
Also create two directories using the following command:
```
mkdir -p /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/output/untracked/chunked_output/
```

Then 
```
bash python_search_all.sh
```
Then for cleanup we neeed to do a few things:

First
Remove all the screens with the "pythonsearch" suffix:
```
screen -ls | grep -E 'pythonsearch' | awk -F ' ' '{print $1}'| while read s; do screen -XS $s quit; done

```
Then remove all the initial screens, all of the screen started with "c" for example c3117 is a nodename in the discovery cluster:
```
screen -ls | grep -E 'c' | awk -F ' ' '{print $1}'| while read s; do screen -XS $s quit; done

```
source: https://unix.stackexchange.com/questions/20435/killing-multiple-gnu-screen-sessions-with-the-same-name

Then inside all of the session delete the /srv/tmp/elasticsearch