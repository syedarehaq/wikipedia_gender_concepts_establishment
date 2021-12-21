#!/bin/bash
#SBATCH --job-name=wiki_all
#SBATCH --partition=netsi_standard
#SBATCH --nodes=1
#SBATCH --mem=200GB
#SBATCH --cpus-per-task=16
#SBATCH --time=30-24:00:00
#SBATCH --exclusive
#SBATCH --output=wiki_all_%j.out
#SBATCH --error=wiki_all_%j.err


corpus=$1
basedir="/work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/scripts/discovery_cluster/"

mkdir -p $basedir$corpus

sbatch_output_dir=$basedir$corpus"/slurm_output"
sbatch_error_dir=$basedir$corpus"/slurm_error"
mkdir -p $sbatch_output_dir
mkdir -p $sbatch_error_dir

python_search_output_dir_page_title="/work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/output/untracked/chunked_output/"$corpus"/searched_in_page_title";
python_search_output_dir_page_text="/work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/output/untracked/chunked_output/"$corpus"/searched_in_text";
mkdir -p $python_search_output_dir_page_title;
mkdir -p $python_search_output_dir_page_text;


for nodename in c3200
do
	sbatch --output=$sbatch_output_dir"/"$nodename"_%j.out" --error=$sbatch_error_dir"/"$nodename"_%j.err" --partition=netsi_standard --nodelist=$nodename run_wikisearch_single.sh $nodename $corpus
done

# while IFS= read -r nodename || [ -n "$nodename" ];
# ## correction for missing last line
# ## https://stackoverflow.com/questions/12916352/shell-script-read-missing-last-line
# do
# 	sbatch --output=$sbatch_output_dir"/"$nodename"_%j.out" --error=$sbatch_error_dir"/"$nodename"_%j.err" --partition=netsi_standard --nodelist=$nodename run_wikisearch_single.sh $nodename $corpus
# done < "available_nodelist.txt"