#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp


/usr/bin/time -v python Demultiplex.py \
-1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
-2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
-3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
-4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz
