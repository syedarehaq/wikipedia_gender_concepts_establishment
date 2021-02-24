#!/bin/bash
nodename=$1
echo $nodename;
module load python/3.8.1;
source /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/venv/bin/activate;
corpus=$2
input_file_current_node="/work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/input/derived/discovery_input_for_each_node/"$corpus"/"$1".txt"
## reading line by line of a file 
## https://www.cyberciti.biz/faq/unix-howto-read-line-by-line-from-file/
while IFS= read -r line || [ -n "$line" ];
## correction for missing last line
## https://stackoverflow.com/questions/12916352/shell-script-read-missing-last-line
do
	echo $line;
	python3 /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/scripts/02_03_03_search_concepts_only_with_dash_from_alexander_street_in_wikipedia_elastic_get_page_titles_from_file_chunks.py --input $line --corpus $corpus;
done < "$input_file_current_node"