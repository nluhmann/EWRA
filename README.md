# EWRA - Edge-Weighted Reconstruction integrating aDNA Assembly graph

The EWRA algorithm computes a parsimonious reconstruction of marker adjacencies minimizing the Single-Cut-or-Join (SCJ) distance along a given phylogenetic tree, including the information provided by an assembly graph of ancient DNA (aDNA) data at one internal node of the tree.

## Requirements

The complete pipeline can be run with the provided bash-script. Additionally, the following programs are required:

* FPSAC
* python + networkx
* blast

## Input

* Assembled extant reference genomes (multiple-fasta file)
* phylogenetic tree in newick format, placement of the ancient sample marked with @
* aDNA assembly graph in dot format
* aDNA assembly contigs (multiple-fasta file)


## Running the pipeline
The following bash script runs through the process of computing marker families using FPSAC, extracting adjacencies from the provided assembly graph and running the reconstruction along the phylogenetic tree.

```
run_program.sh -fasta <extant_genomes> -contigs <aDNA_contigs> -dot <assembly_graph> -tree <phylogenetic_tree> -weight <length of assembly graph leaf>
```

Note that if an alternative graph is used different from an assembly graph in dot format (produced by an assembly tool), the pipeline can easily be adapted by skipping steps in the bash script and providing alternative parsing.


## Reproducing experiments reconstructing Yersinia pestis ancestral genomes (paper to be published)

The experiment presented in [1] can be run following the steps below. 

### Run EWRA with contig assembly graph

We provide all required input files to run EWRA in this repository in the experiments folder.

```
run_program.sh -tree ./experiments/input/pestis_tree.txt -contigs ./experiments/input/unitigsGreater500.fa -fasta ./experiments/input/extant_genomes.fa -dot ./experiments/input/pestis_k21.dot -weight 0.005
```

### Run EWRA with marker assembly graph

To infer the marker assembly graph, [AGapEs](https://github.com/nluhmann/AGapEs) can be used to analyse the gap coverage for all potentially adjacent marker pairs. Following the instructions for this tool, 
a coordinates file for all filled gaps will be produced, which can be parsed to use with EWRA.


## References
[1] Luhmann N, Chauve C, Stoye J, and Wittler R. "Scaffolding of Ancient Contigs and Ancestral Reconstruction in a Phylogenetic Framework". Under review. 2018.
[2] Bos KI, Schuenemann VJ, Golding GB, Burbano HA, Waglechner N, Coombes BK, McPhee JB, DeWitte SN, Meyer M, Schmedes S, Wood J. "A draft genome of Yersinia pestis from victims of the Black Death". Nature. 2011 Oct 27;478(7370):506-10.



