# Virtual Screening Pipeline: In Silico Docking Workflow

## Introduction

### Why an in silico pipeline?
To narrow down the search space before an in vitro hit identification. Docking is a probabilistic and empirical calculation for enriching the top of our ranked library with true positives. In other words, docking is a heuristic which gives us a better chance at selecting hits than random chance. Since in vitro testing through assays is expensive and takes time, we can prioritise our bets using a preliminary stage of docking.

### Why use this pipeline?
Several softwares have been developed for carrying out docking calculations over the years. However, most of the widely used and trusted software are often paid, not compatible with all operating systems, have buggy GUIs or don’t support multiple ligands rendering virtual screening unfeasible.

This workflow is an attempt towards democratising Virtual Screening protocols using a widely used and documented docking software (**Autodock Vina**) combined with automation using Python and Shell scripting. Moreover, in addition to ranking the ligands based on their predicted binding affinity, this tutorial covers post-docking visualisation and generation of 2D interaction diagrams to gain a deeper understanding of the particular interactions that are important for the residues in the binding pocket of your target protein.

A general validation protocol has been elucidated in `[Insert repo link]` to check for the accuracy of this protocol.

---

## General Overview of the Protocol

The docking workflow requires the following three input files:

1. Cleaned Receptor (target protein) file in `.pdbqt` format.
2. Ligand files in `.pdbqt` format.
3. Configuration File.

---

## Steps of the Workflow

### RCSB PDB: Target Selection

After you have carried out a thorough literature survey, you should have a list of PDB IDs of your essential genes. This is an important pre-requisite since you need literature which defines essential genes for the pathogen critical for its survival. Once you have this, you must ensure that the target you pick is not homologous to any human protein using `blastp` tool. This ensures that any hit you generate doesn’t also turn out to be a hit for a human protein. After carrying out this step, look for an experimental structure sourced from the pathogen of interest. In case the experimental structure of the essential gene from your pathogen is not present, you can carry out Homology Modelling (using tools like SWISS_MODEL, I_TASSER, MODELLER etc.).

> Note down the PDB ID for future reference (Ex. `7K99`)

---

### Visualising the Protein in PyMol

Launch PyMol on your device and enter `fetch 7K99` in the PyMol command box to load the protein.

---

### Manual Protein Preparation on PyMol

In the PyMol command line, enter the following commands:
``` remove solvent
    remove organic
    remove inorganic```



