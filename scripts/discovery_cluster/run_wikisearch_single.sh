#!/bin/bash
#SBATCH --mem=200GB
#SBATCH --exclusive

nodename=$1
echo $nodename;
corpus=$2
## Copy the elasticsearch first to the /srv/tmp
## It has the index preloaded
cp -r /home/haque.s/elasticsearch-7.10.1 /srv/tmp/elasticsearch-7.10.1;
sleep 5;
/srv/tmp/elasticsearch-7.10.1/bin/elasticsearch -d -p /srv/tmp/elasticsearch-7.10.1/pid;
## Using elasticsearch with curl inside discovery cluster requires unsetting proxy
unset http_proxy;
sleep 5;
module load python/3.8.1
source /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/venv/bin/activate
input_file_current_node="/work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/input/derived/discovery_input_for_each_node/"$corpus"/"$nodename".txt"
## reading line by line of a file 
## https://www.cyberciti.biz/faq/unix-howto-read-line-by-line-from-file/
while IFS= read -r line || [ -n "$line" ];
## correction for missing last line
## https://stackoverflow.com/questions/12916352/shell-script-read-missing-last-line
do
	echo $line;
	#python3 /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/scripts/02_03_03_search_concepts_only_with_dash_from_alexander_street_in_wikipedia_elastic_get_page_titles_from_file_chunks.py --input $line --corpus $corpus;
done < "$input_file_current_node"