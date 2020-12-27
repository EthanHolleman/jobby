#!/bin/bash
#SBATCH --partition=production
#SBATCH --job-name=Arguement
#SBATCH --nodes=1 # single node, anything more than 1 will not run
#SBATCH --ntasks=1 # equivalent to cpus
#SBATCH --mem=30000 
#SBATCH --time=99:00:00 
#SBATCH --output=MULTI.out # STDOUT
#SBATCH --error=MULTI.err # STDERR
#SBATCH --mail-user=etholleman@ucdavis.edu #
#SBATCH --mail-type=ALL #
aklog
hostname
module load R
Rscript ./multitask.r
run_good

<sign>