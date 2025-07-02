# 1. Split a multi-molecule SDF file into individual SDF files
obabel -isdf input.sdf -osdf -m
# Output: OBabel0.sdf, OBabel1.sdf, ...

# 2. Energy minimize all SDF files using the MMFF94 force field (1000 steps)
obminimize -ff MMFF94 -n 1000 OBabel*.sdf
# Output: Minimized SDF files (overwrites originals unless you specify output)

# For atoms not accounted for by the MMFF94 Force Field:
obabel input.pdb -O output_minimized.pdb --minimize --steps 500 --ff UFF

# 5. Convert all minimized SDF files directly to PDBQT with protonation and 3D generation
obabel OBabel*.sdf -opdbqt -p 7.4 --gen3d --partialcharge gasteiger -m
# Output: OBabel0.pdbqt, OBabel1.pdbqt, ...

#Protein preparation
obabel 7K99_cleaned.pdb -O 7K99_dock.pdbqt -xr --partialcharge gasteiger

#moving files to a specific directory
for file in min_DB*.sdf; do                                             
    if [ -e "$file" ]; then
        mv "$file" DB_pdbqt_structs
        echo "Moved $file to DB_pdbqt_structs"
    fi
done

#Converting all SDF files to PDBQT format
for file in *.sdf; do                                                   
  base=$(basename "$file" .sdf)
  out="dock_${base}.pdbqt"
  obabel "$file" -opdbqt -O "$out" -p 7.4 --partialcharge gasteiger
  mv "$out" /Users/prathamdhanoa/Downloads/Docking/VS_Config/Validation_ROC/inactives_806_pdbqt
  echo "Converted $file -> $out"
done

#Minimizing all SDF files
for file in *.sdf; do                                                   
  base=$(basename "$file")
  obabel "$file" -O "min_$base" --minimize --ff MMFF94 --steps 1500 --sd
  mv "min_$base" /Users/prathamdhanoa/Downloads/Docking/VS_Config/Validation_ROC/min_inactives_592_sdf
  echo "Minimized $file -> min_$base"
done


# Split the multi-molecule SDF into separate files and name them with their corresponding drugbank IDs.
obabel drugbank.sdf -O mol_.sdf -m

for file in mol_*.sdf; do
  id=$(awk '/^>  <DRUGBANK_ID>/{getline; print $0; exit}' "$file" | tr -d ' \t\r\n') # Rename files according to DrugBank ID
  if [ -n "$id" ]; then
    mv "$file" "${id}.sdf"
    echo "Renamed $file to ${id}.sdf"
  else
    echo "No DrugBank ID found in $file"
  fi
done


