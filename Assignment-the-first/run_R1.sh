#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition bgmp
#SBATCH --mem=16G
#SBATCH --mail-user=camk@uoregon.edu
#SBATCH --mail-type=ALL

mamba activate plt_env

/usr/bin/time -v ./perbase_dist.py -f "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz" \
 -l 101 -g "R1_graph.png"
