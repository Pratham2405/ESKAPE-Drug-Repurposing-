# ESKAPE-Drug-Repurposing-
The repo aims at seeking anti-ESKAPE pathogen hits from existing approved drugs using docking(Autodock Vina) and MD simulation(GROMACS) studies.
# Virtual Screening Tutorial

Welcome to the **Virtual Screening Tutorial** repository!  
This guide will walk you through the complete pipeline for performing structure-based virtual screening, from ligand and receptor preparation to running the screening and analyzing results.

---

## Table of Contents

- [Requirements](#requirements)
- [Pipeline Steps](#pipeline-steps)
  - [1. Ligand Preparation](#1-ligand-preparation)
  - [2. Receptor Preparation](#2-receptor-preparation)
  - [3. Pocket Determination](#3-pocket-determination)
  - [4. Config File Preparation](#4-config-file-preparation)
  - [5. Running Virtual Screening](#5-running-virtual-screening)
- [References & Resources](#references--resources)
- [License](#license)

---

## Requirements

Before you begin, make sure you have the following installed:

- [RDKit](https://www.rdkit.org/)
- [Open Babel (obabel)](https://openbabel.org/wiki/Main_Page)
- [AutoDock Vina](http://vina.scripps.edu/)
- [Python 3.x](https://www.python.org/)

You can install Python dependencies using:

---

## Pipeline Steps

### 1. Ligand Preparation

1. **Organize Ligands:**  
   Place all your ligand files ( in `.pdbqt` format) in a single, separate directory.

2. **Sanitize Molecules:**  
   Use `RDKit_validation&addH.py` to check and sanitize your ligand structures:
---

3. **Prepare Ligands with Open Babel:**  
Run the following command in your terminal to convert and prepare ligands:
`obabel input_PDB_file_name -O output_PDB_file_name -xr --partialcharge gasteiger`
This script will convert your ligands into the required format for docking.

---

### 2. Receptor Preparation

1. **Open Receptor in PyMOL:**  
Load your receptor structure (e.g., `.pdb` file) in PyMOL.

2. **Clean the Structure:**  
- Remove water molecules.
- Remove inorganic and organic molecules (if not part of the binding site).

3. **Add Hydrogens:**  
- Add hydrogens, especially polar hydrogens, to the receptor.

4. **Save the Cleaned Receptor:**  
Export the cleaned and prepared receptor structure for docking.

---

### 3. Pocket Determination

1. **Identify Binding Pocket:**  
Use [CavityPlus](http://www.pkumdl.cn:8000/cavityplus/index.php) (or your preferred tool) to analyze the receptor and identify potential binding pockets.

2. **Note Pocket Coordinates:**  
Record the coordinates of the center of the binding pocket for use in the docking configuration.

---

### 4. Config File Preparation

1. **Edit the Docking Config File:**  
- Enter the pocket center coordinates.
- Set the box size (dimensions covering the binding site).
- Choose exhaustiveness, number of CPUs, and other Vina parameters.

Example:
center_x = 12.34
center_y = 56.78
center_z = 90.12
size_x = 20
size_y = 20
size_z = 20
exhaustiveness = 8
cpu = 4


---

### 5. Running Virtual Screening

1. **Update Paths:**  
Open `VS_Script_2.py` and enter the appropriate paths for:
- Ligand directory
- Receptor file
- Config file

2. **Run the Screening Script:**  
Execute the script to start the virtual screening. You would obtain a CSV file ranking the ligands based on Binding Affinity(kJ/mol).
