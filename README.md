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
run_program.sh -fasta <extant_genomes> -contigs <aDNA_contigs> -dot <assembly_graph> -tree <phylogenetic_tree>
```

Note that if an alternative graph is used different from an assembly graph in dot format (produced by an assembly tool), the pipeline can easily be adapted by skipping steps in the bash script and providing alternative parsing.


