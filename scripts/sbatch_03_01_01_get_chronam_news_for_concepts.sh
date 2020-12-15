#!/bin/bash
#SBATCH --job-name=chronam
#SBATCH --partition=netsi_standard
#SBATCH --nodes=1
#SBATCH --mem=200GB
#SBATCH --cpus-per-task=16
#SBATCH --time=7-24:00:00
#SBATCH --output=output/chronam_%j.out
#SBATCH --error=error/chronam_%j.err

source ~/.bashrc

module load python/3.8.1

source /work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/venv/bin/activate
python3 03_01_01_search_concepts_in_chronicling_america.py