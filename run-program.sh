#!/bin/bash
echo "Starting..."
# paths to required programs, edit if necessary.
pathTo_makeblastdb=makeblastdb;
pathTo_makembindex=makembindex;
pathTo_blastn=blastn;
pathTo_python=python;



# check if required program paths are okay to use.
command -v $pathTo_makeblastdb >/dev/null 2>&1 || { echo "I require blast, please provide the right path. Aborting." >&2; exit 1; }
command -v $pathTo_makembindex >/dev/null 2>&1 || { echo "I require blast, please provide the right path. Aborting." >&2; exit 1; }
command -v $pathTo_blastn >/dev/null 2>&1 || { echo "I require blastn, please provide the right path. Aborting." >&2; exit 1; }
command -v $pathTo_python >/dev/null 2>&1 || { echo "I require python, please provide the right path. Aborting." >&2; exit 1; }
echo "Required program path are okay to use"


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC=$DIR/src



echo "Checking provided input"

EXTANT_GENOMES="";
CONTIGS="";
GRAPH="";
TREE="";


#read parameters from input and check if all parameters are provided
if [ $# -ne 8 ]
then
   echo "Please provide the expected parameter!"
   echo "usage: $0 -fasta <extant_genomes.fa> "
   exit 1
fi
while [ $# -gt 0 ]
do
    case "$1" in
	-fasta) EXTANT_GENOMES="$2"; shift;;
	-contigs) CONTIGS="$2"; shift;;
	-dot) GRAPH="$2"; shift;;
	-tree) TREE="$2"; shift;;
	--)	shift; break;;
	-*)
	    echo >&2 \
	    "usage: $0 -sl <segmentLength> -r <reference.fasta> -m <mapping.sam/bam>"
	    exit 1;;
	*)  break;;	# terminate while loop
    esac
    shift
done





echo "creating file structure"

INTERIM=./interim
RESULTS=./results
EXTANT_GENOMES_DB=$INTERIM/extant_genomes_db
MEGABLAST_HITS=$INTERIM/megablast_hits
FPSAC=./FPSAC/src
ANCIENT_CONTIGS_LENGTH=$INTERIM/ancient_contigs_length
ANCIENT_EXTANT_HITS=$INTERIM/ancient_extant_hits
FAMILIES_WITH_CONTIG_NAMES=$INTERIM/families_with_contig_names
FAMILIES_PROFILES=$INTERIM/families_profiles
FAMILIES_WITH_CONTIG_NAMES_CORRECTED=$INTERIM/families_with_contig_names_corrected
FAMILIES_PROFILES_CORRECTED=$INTERIM/families_profiles_corrected
FAMILIES_ERRORS=$INTERIM/families_errors
FILTERED_CONTIGS=$INTERIM/filtered_contigs
FILTERED_CONTIGS_IDS=$INTERIM/filtered_contigs_ids
PRUNED_GRAPH=$INTERIM/pruned_graph.dot
ALL_ADJACENCIES=$INTERIM/all_adjacencies
OUTPUT_ADJACENCIES=$RESULTS/adjacencies/
OUTPUT_SCAFFOLDS=$RESULTS/scaffolds/
FILTERED_FAMILIES=$INTERIM/filtered_families


mkdir -p $INTERIM
mkdir -p $RESULTS
mkdir -p $OUTPUT_ADJACENCIES
mkdir -p $OUTPUT_SCAFFOLDS


echo "Filtering assembly contigs"

#filter contigs longer than 500bp
python $SRC/biggestContigs.py $CONTIGS $FILTERED_CONTIGS 500 $FILTERED_CONTIGS_IDS $ANCIENT_CONTIGS_LENGTH

#get all contig ids from original file
biggestContigID=`tail -n 2 $CONTIGS | grep ">" | awk '{ print $1 }' | cut -c 2-`


echo "Prune assembly graph to only include biggest contigs"
#prune assembly graph so that it only contains filtered contigs
python $SRC/pruneAssemblyGraph.py $GRAPH $FILTERED_CONTIGS_IDS $biggestContigID $PRUNED_GRAPH



echo "Preprocessing reads to find marker sequence"

echo "Index extant genomes"
#indexing extant genomes fasta
makembindex -input $EXTANT_GENOMES -old_style_index true -output $EXTANT_GENOMES_DB -verbosity quiet

echo "Create database from extant genomes"
#creating database from extant genomes
makeblastdb -in $EXTANT_GENOMES -dbtype nucl

echo "blast contigs"
#blast contigs from ancient genome (assembly graph) against extant genomes
blastn -task megablast -db $EXTANT_GENOMES -query $FILTERED_CONTIGS -use_index True -index_name $EXTANT_GENOMES_DB -out $MEGABLAST_HITS -outfmt 6


echo "format blast hits"
#format blast hits
python $FPSAC/fpsac_format_blast_hits.py \
    ${MEGABLAST_HITS} \
    ${ANCIENT_CONTIGS_LENGTH} \
    ${ANCIENT_EXTANT_HITS}


echo "find families"
#find families
python $FPSAC/fpsac_compute_families_coordinates_and_profiles.py $ANCIENT_EXTANT_HITS $FAMILIES_WITH_CONTIG_NAMES $FAMILIES_PROFILES 100 95

echo "error correction step"
#error correction
python $FPSAC/fpsac_correct_families.py $FAMILIES_WITH_CONTIG_NAMES $FAMILIES_PROFILES $FAMILIES_WITH_CONTIG_NAMES_CORRECTED $FAMILIES_PROFILES_CORRECTED $FAMILIES_ERRORS


python $SRC/correctFamilies.py $FAMILIES_WITH_CONTIG_NAMES_CORRECTED $FILTERED_FAMILIES $TREE

echo "Compute adjacency set for internal nodes of the phylogeny"

#extract adjacencies for extant genomes and assembly graph
python $SRC/extractAdjacencies.py $FILTERED_FAMILIES $PRUNED_GRAPH $TREE $ALL_ADJACENCIES

#compute Fitch on extracted adjacencies
python $SRC/Main.py $TREE $ALL_ADJACENCIES $OUTPUT_ADJACENCIES $OUTPUT_SCAFFOLDS 

