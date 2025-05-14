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
