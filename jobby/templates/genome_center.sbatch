#!/bin/bash
#SBATCH --partition=production
#SBATCH --job-name=<name>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem={{10000}} 
#SBATCH --time={{1:00:00}} 
#SBATCH --output=<name>.out # STDOUT
#SBATCH --error=<name>.err # STDERR
#SBATCH --mail-user=etholleman@ucdavis.edu
#SBATCH --mail-type=ALL

{{}}

# This script was last run <time>
<sign>