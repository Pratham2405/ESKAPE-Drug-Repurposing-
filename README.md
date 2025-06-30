
---

## Table of Contents

- [Requirements](#requirements)
- [Pipeline Steps](#pipeline-steps)
  - [1. Ligand Preparation](#1-ligand-preparation)
  - [2. Receptor Preparation](#2-receptor-preparation)
  - [3. Pocket Determination](#3-pocket-determination)
  - [4. Config File Preparation](#4-config-file-preparation)
  - [5. Running Virtual Screening](#5-running-virtual-screening)
  - [6. Analysis & Visualization](#6-analysis--visualization)
- [References & Resources](#references--resources)
- [License](#license)

---

## Requirements

- **Python 3.x**
- **RDKit**
- **Open Babel (obabel)**
- **AutoDock Vina**
- **PyMOL**
- **PoseView**

---

## Pipeline Steps

### 1. Ligand Preparation

- **Input:** `Drugbank_3D.sdf` or other ligand libraries.
- **Split & Rename:**  
  Use `Split&Rename.py` to split multi-molecule SDF files and rename individual ligand files.
- **Format Conversion:**  
  Use `Obabel_prep.sh` to convert ligands to `.pdbqt` format required for docking.

### 2. Receptor Preparation

- **Input:** PDB ID of the target protein.
- **Manual Preparation in PyMOL:**  
  - Remove water and non-essential molecules.
  - Add hydrogens (especially polar hydrogens).
  - Save the cleaned structure.
- **Format Conversion:**  
  Use `Obabel_prep.sh` to convert the receptor to `.pdbqt` format.

### 3. Pocket Determination

- **Binding Site Identification:**  
  Use **CavityPlus** or **DoGSiteScorer** to identify and score binding pockets.
- **Record Pocket Coordinates:**  
  Note the center coordinates for use in the configuration file.

### 4. Config File Preparation

- **Edit `VS_Config.txt`:**  
  Specify pocket center coordinates, box size, exhaustiveness, CPUs, etc.

  Example:

### 5. Running Virtual Screening

- **Run `VS_Script.py`:**  
Provide the prepared ligands, receptor, and config file as input.
- **Outputs:**
- `out.pdbqt`: Docked ligand poses.
- `log.txt`: Docking logs.
- `results.csv`: Ranked results based on binding affinity.

### 6. Analysis & Visualization

- **Visualize Docking Poses:**  
Load `out.pdbqt` in PyMOL for 3D visualization.
- **2D Interaction Diagrams:**  
Use **PoseView** to generate 2D interaction diagrams from docking results.

---

## References & Resources

- [CavityPlus](http://www.pkumdl.cn:8000/cavityplus/index.php)
- [AutoDock Vina](http://vina.scripps.edu/)
- [Open Babel](https://openbabel.org/wiki/Main_Page)
- [RDKit](https://www.rdkit.org/)

---

## License

See LICENSE file for details.

---

**Note:**  
This workflow reflects the latest updates, including automated ligand splitting, enhanced preparation scripts, and new visualization steps for post-docking analysis.

