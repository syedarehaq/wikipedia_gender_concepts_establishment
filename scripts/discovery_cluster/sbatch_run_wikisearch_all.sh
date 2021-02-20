#!/bin/bash
#SBATCH --job-name=wiki_all
#SBATCH --partition=netsi_standard
#SBATCH --nodes=1
#SBATCH --mem=200GB
#SBATCH --cpus-per-task=16
#SBATCH --time=30-24:00:00
#SBATCH --exclusive
#SBATCH --output=chronam_%j.out
#SBATCH --error=chronam_%j.err


#basedir="./untracked/aps_mag_santo/output/128/similarity_improved/aps_mag_santo_doi_vectors_it_1_set_epoch_50_trn_lnth_6_dim_128_prcr_lnth_6_avg_6/"
basedir=$1
corpus=$2

mkdir -p $basedir$corpus
sbatch_output_dir=$basedir$corpus"/slurm_output"
sbatch_error_dir=$basedir$corpus"/slurm_error"
mkdir -p $sbatch_output_dir
mkdir -p $sbatch_error_dir

for nodename in c3178 c3179
do
	sbatch --output=sbatch_output_dir"/"$nodename_%j.out --error=sbatch_error_dir"/"$nodename_%j.err --nodelist=$nodename run_wikisearch_single.sh $nodename $corpus
done
do
	echo $machine
	sbatch --output=$basedir"hist/slurm_output/"$machine"_"$distance_type"_"$binsize"_hist_%j.out" --error=$basedir"hist/slurm_error/"$machine"_"$distance_type"_"$binsize"_hist_%j.err" histogram.sh $basedir $machine $distance_type $binsize
	#bash histogram.sh $basedir $machine $distance_type $binsize
done
