#!/bin/bash
nodename=$1
echo $nodename;
module load python/3.8.1;
source /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/venv/bin/activate;
input_file_current_node="/work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/input/derived/discovery_input_for_each_node/"$1".txt"
while IFS= read -r line
do
	echo $line;
	python3 /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/scripts/02_03_03_search_concepts_only_with_dash_from_alexander_street_in_wikipedia_elastic_get_page_titles_from_file_chunks.py --input $line;
done < "$input_file_current_node"