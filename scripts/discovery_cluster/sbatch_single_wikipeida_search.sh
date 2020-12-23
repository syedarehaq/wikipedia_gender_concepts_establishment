#!/bin/bash
#SBATCH --job-name=wiki_s
#SBATCH --partition=netsi_standard
#SBATCH --nodes=1
#SBATCH --mem=200GB
#SBATCH --cpus-per-task=16
#SBATCH --time=30-24:00:00
#SBATCH --exclusive
#SBATCH --output=chronam_%j.out
#SBATCH --error=chronam_%j.err

source ~/.bashrc

module load python/3.8.1
#copy the things to the /srv/ folder
cp -r /home/haque.s/elasticsearch-7.10.1 /srv/elasticsearch-7.10.1
#run elastic in the background, get the process id
/srv/elasticsearch-7.10.1/bin/elasticsearch -d -p /srv/elasticsearch-7.10.1/pid
# sleep for 30 seconds to let it start
sleep 10
# Activate the python environment
source /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/venv/bin/activate
# CD into script folder



achine=$1
input_chunkfiles=$2
source /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/venv/bin/activate
python3 -u 03_01_01_search_concepts_in_chronicling_america.py


#basedir="./untracked/aps_mag_santo/output/128/similarity_improved/aps_mag_santo_doi_vectors_it_1_set_epoch_50_trn_lnth_6_dim_128_prcr_lnth_6_avg_6/"
basedir=$1
#distance_type=positive
distance_type=$2
#binsize=1000
binsize=$3

mkdir -p $basedir"hist"
mkdir -p $basedir"hist/slurm_error"
mkdir -p $basedir"hist/slurm_output"

for machine in $(seq 0 1 99)
do
	echo $machine
	sbatch --output=$basedir"hist/slurm_output/"$machine"_"$distance_type"_"$binsize"_hist_%j.out" --error=$basedir"hist/slurm_error/"$machine"_"$distance_type"_"$binsize"_hist_%j.err" histogram.sh $basedir $machine $distance_type $binsize
	#bash histogram.sh $basedir $machine $distance_type $binsize
done
