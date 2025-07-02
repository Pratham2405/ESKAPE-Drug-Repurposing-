# Virtual Screening Pipeline: In Silico Docking Workflow

## Introduction

### Why an in silico pipeline?
To narrow down the search space before an in vitro hit identification. Docking is a probabilistic and empirical calculation for enriching the top of our ranked library with true positives. In other words, docking is a heuristic which gives us a better chance at selecting hits than random chance. Since in vitro testing through assays is expensive and takes time, we can prioritise our bets using a preliminary stage of docking.

### Why use this pipeline?
Several softwares have been developed for carrying out docking calculations over the years. However, most of the widely used and trusted software are often paid, not compatible with all operating systems, have buggy GUIs or don’t support multiple ligands rendering virtual screening unfeasible.

This workflow is an attempt towards democratising Virtual Screening protocols using a widely used and documented docking software (Autodock Vina) combined with automation using Python and Shell scripting. Moreover, in addition to ranking the ligands based on their predicted binding affinity, this tutorial covers post-docking visualisation and generation of 2D interaction diagrams to gain a deeper understanding of the particular interactions that are important for the residues in the binding pocket of your target protein. A general validation protocol has been elucidated in [Insert repo link] to check for the accuracy of this protocol.

---

## General Overview of the Protocol

The docking workflow requires the following three input files:
1. Cleaned Receptor (target protein) file in `.pdbqt` format.
2. Ligand files in `.pdbqt` format.
3. Configuration File.

---

## Steps of the Workflow

### RCSB PDB

After you have carried out a thorough literature survey, you should have a list of PDB IDs of your essential genes. This is an important pre-requisite since you need literature which defines essential genes for the pathogen critical for its survival. Once you have this, you must ensure that the target you pick is not homologous to any human protein using `blastp` tool. This ensures that any hit you generate doesn’t also turn out to be a hit for a human protein. After carrying out this step, look for an experimental structure sourced from the pathogen of interest. In case the experimental structure of the essential gene from your pathogen is not present, you can carry out Homology Modelling (using tools like SWISS_MODEL, I_TASSER, MODELLER etc.).

![RCSB PDB Window](RCSB_PDB.png "RCSB PDB Window")

> Note down the PDB ID for future reference (Ex. `7K99`).

---

### Visualising the Protein in PyMol

Launch PyMol on your device and enter `fetch 7K99` in the PyMol command box to load the protein.

![Loading Protein Using PyMol](fetch.png " Loading Protein Using PyMol")

### Manual Protein Preparation on PyMol

In the PyMol command line, enter the following commands:
```
remove solvent
remove organic
remove inorganic
```

Once done, go to `A(Actions)` -> `hydrogen` -> `add polar` to add polar hydrogens to the receptor, often important in carrying out interactions with the ligand molecules and important for binding in general. All of the above commands are simply equivalent to removing the respective lines in the PDB file of the protein. The PyMol GUI, however, makes it easier to implement the same tasks accurately using an interactive GUI.

![Loading Protein Using PyMol](addpolarH.png " Loading Protein Using PyMol")

---

### Saving the Cleaned Receptor

To save the cleaned receptor as a PDB file, go to `File -> Export Molecule -> PDB Options -> Save`.

Save the file to an appropriate location on your device and name the file `7K99_cleaned` and choose file type as `.pdb` instead of the default `.cif` format.

---

### Receptor Preparation with Open Babel

Now, open the directory where you saved `7K99_cleaned.pdb` in terminal and enter the following command from `Obabel_prep.sh`:

`obabel 7K99_cleaned.pdb -O 7K99_dock.pdbqt -xr --partialcharge gasteiger`

This will output a `.pdbqt` file named `7K99_dock.pdbqt`. Your receptor is now suitable for docking.

---

### Ligand Preparation

You can download the drugs of your particular interest from the Drugbank database using various filters available on their website. In this tutorial, we will be carrying out drug repurposing using a library of all approved drugs, `Drugbank_3D.sdf`. As you will find when you view this file in any text editor, this is a single SDF file which has 3D coordinates of all molecules along with loads of other data like IC50, SMILES Representation, Common Name, physiological parameters etc. separated by a `$$$$` line. This means we have to split this file into individual SDF files. To do so, copy the below written snippet of code from `Obabel_prep.sh` and run the following command in the directory where you want to store your split SDF files:
```
obabel drugbank.sdf -O mol_.sdf -m
```
Now to name the files with their respective DrugBank IDs:

```
for file in mol_*.sdf; do
  id=$(awk '/^>  <DRUGBANK_ID>/{getline; print $0; exit}' "$file" | tr -d ' \t\r\n') # Rename files according to DrugBank ID
  if [ -n "$id" ]; then
    mv "$file" "${id}.sdf"
    echo "Renamed $file to ${id}.sdf"
  else
    echo "No DrugBank ID found in $file"
  fi
done
```
### Energy Minimization

Opening the directory with all the split SDF files, enter the following command:

```
for file in *.sdf; do
base=$(basename "$file")
obabel "$file" -O "min_$base" --minimize --ff MMFF94 --steps 1500 --sd
mv "min_$base" /path/to/your/output/directory
echo "Minimized $file -> min_$base"
done
```
Energy minimization is an essential step in molecular docking to ensure each ligand adopts its most stable, low-energy conformation before docking. Ligands from databases may have unrealistic geometries that, if left uncorrected, can lead to inaccurate docking results because they won’t interact with the protein as they would in reality. Minimization uses a molecular mechanics force field, such as MMFF94, to adjust atomic positions and reduce the molecule’s potential energy, optimizing its geometry. This process results in a physically plausible ligand structure, increasing the reliability of predicted ligand–protein interactions.

---

### Convert Ligands to PDBQT

Once all the ligands have been minimised, we have to convert all the `.sdf` files to `.pdbqt` in order to be suitable for Autodock Vina:

```
for file in *.sdf; do
base=$(basename "$file" .sdf)
out="dock_${base}.pdbqt"
obabel "$file" -opdbqt -O "$out" -p 7.4 --partialcharge gasteiger
mv "$out" /path/to/your/output/directory
echo "Converted $file -> $out"
done
```
This method adds gasteiger charges and protonates(adds hydrogen) to the ligands solving the pKa values at pH \=7.4.
---

### Binding Pocket: Defining the Grid Box

Vina requires an a priori 3D search space in the form of a grid box where it can look for favourable binding poses. This is done primarily to reduce the time required for determination of each pose. Try to keep your grid side length \< 25 Angstrom for optimal performance and ensuring specificity towards your binding pocket. To completely define the grid box, we need the coordinates of its center. More importantly, we need to find a 3D region of the protein which is most likely to favourably bind a ligand molecule, also known as the Binding Pocket of the protein. A few online tools like CavityPlus, DoGSiteScorer, FTMap can help us know the active binding site and its center coordinates.

---

### Other Arguments of the Config. File

- `exhaustiveness`
- `number of poses`
- `cpus`
- `verbosity`

---

### Running VS_Script.py

In order to run `VS_Script.py`, the path of the various input files and directories on your device is to be specified in the code snippet shown below:

![Adding Path to VS_Script.py](VS_Code_Snippet.png "Adding Path to VS_Script.py")

Also, change the name of the output file appropriately. Incomplete/faulty structures would be moved to a `FAULTY_DIR` for you to look at and analyse either manually or using PyMol.

If the file runs succesfully without encountering any error while compiling, the terminal output should look something like this:

![Terminal_Output](Terminal_Output.png "Terminal_Output")

---

### Output Files

- `results_drugbank.csv`: Has a list of all ligands ranked according to their predicted binding affinity (kcal/mol).
- `log.txt`: Generated for each molecule and shows details of the docking run.
- `out.pdbqt`: Contains the top poses with the most favourable binding. Drag this file to a PyMol window with the receptor open and you can see the ligand docked with the receptor in the binding pocket. Pressing the right arrow key sequentially shows you the different poses.

---

### 2D Interaction Diagram

Repeat the above step with ligands on the top of `results_drugbank.csv` and you will see something like this:

![Docked ligand with protein](Docked_Pose.png "Docked ligand with protein")

After saving the file obtained in the previous step, upload it to PoseView. You should see the following:

![PoseView Window](PoseView.png "PoseView Window")

PoseView identifies the ligands and you can generate different 2D interaction diagrams for each ligand you wish to analyse. Using the information obtained from the 2D Interaction Diagram, we can visualise the interactions in 3D for personal visualisation or presentation on PyMol:

![Visualising Interactions on PyMol](Measurements.png "Visualising Interactions on PyMol")

---

### Adjustment for Running on High Performance Computing Node (HPC)

Docking of each molecule takes around 1–2 mins on average. Docking 10,000 ligands then, as you can probably see, will take an impractical amount of time to complete. For carrying out this script for this many ligands, you need to have access to a High Performance Computing Node. An alternate to `VS_Script.py` with suitable modifications catered to HPC has been uploaded to this repository (`VS_Script_HPC.py`). For IITD students working on the HPC, (link to Kanha repo) and (link to HPC IITD) are great resources for end-to-end implementation and troubleshooting.


