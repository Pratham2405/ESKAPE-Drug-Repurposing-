import os
import subprocess
import glob
import csv

# Define paths and filenames (FILL IN YOUR ACTUAL PATHS AND FILENAMES)
RECEPTOR_FILE = "/Users/prathamdhanoa/Downloads/Docking/molecule-generator-master/drive-download-20250104T145431Z-001/NCAT/7d1i/final_7d1i_2.pdbqt"
LIGAND_DIR = "/Users/prathamdhanoa/Downloads/Docking/molecule-generator-master/drive-download-20250104T145431Z-001/NCAT"
OUTPUT_DIR = "/Users/prathamdhanoa/Downloads/Docking/molecule-generator-master/drive-download-20250104T145431Z-001/NCAT/drugbank_output"
CONF_FILE = "/Users/prathamdhanoa/Downloads/Docking/molecule-generator-master/drive-download-20250104T145431Z-001/NCAT/VS_Config_7d1i.txt"
VINA_PATH = "/opt/homebrew/bin/Vina"  # Leave empty if vina is in your system PATH

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to run Vina docking with error handling and timeout
def run_vina_docking(receptor, ligand, config, out_pdbqt, out_log):
    try:
        cmd = f"{VINA_PATH} --receptor {receptor} --ligand {ligand} --config {config} --out {out_pdbqt}"
        subprocess.run(
            cmd,
            shell=True,
            check=True,
            timeout=30,  # Timeout set to 30 seconds
            stdout=open(out_log, 'w'),
            stderr=subprocess.STDOUT
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error processing {ligand}: {str(e)}")
        return False
    except subprocess.TimeoutExpired:
        print(f"Timeout (30s) exceeded for {ligand}")
        return False

# Perform virtual screening
ligand_files = sorted(glob.glob(os.path.join(LIGAND_DIR, "*.pdbqt")))

for idx, ligand_file in enumerate(ligand_files, start=1):
    ligand_name = os.path.splitext(os.path.basename(ligand_file))[0]
    out_pdbqt = os.path.join(OUTPUT_DIR, f"{ligand_name}_out.pdbqt")
    out_log = os.path.join(OUTPUT_DIR, f"{ligand_name}_log.txt")

    print(f"Processing {ligand_name}: {idx}/{len(ligand_files)}")

    if not os.path.exists(out_pdbqt) or not os.path.exists(out_log):
        success = run_vina_docking(RECEPTOR_FILE, ligand_file, CONF_FILE, out_pdbqt, out_log)
        if not success:
            # Clean up partial outputs if docking fails
            for fpath in [out_pdbqt, out_log]:
                if os.path.exists(fpath):
                    os.remove(fpath)
            continue  # Skip to the next ligand
    else:
        print(f"Skipping {ligand_name}: structure already processed.")

# Function to parse Vina results
def parse_vina_results(log_file):
    lowest_affinity = None
    with open(log_file, 'r') as f:
        for line in f:
            if line.strip().startswith('1 '):  # Parse the first result line
                first_result = line.split()
                if len(first_result) >= 2:
                    lowest_affinity = float(first_result[1])
                break
    return lowest_affinity

# Rank results
results = []
for log_file in glob.glob(os.path.join(OUTPUT_DIR, "*_log.txt")):
    ligand_name = os.path.splitext(os.path.basename(log_file))[0].replace("_log", "")
    binding_affinity = parse_vina_results(log_file)
    if binding_affinity is not None:
        imphy_id = ligand_name.split('_')[1]
        results.append((imphy_id, binding_affinity))

# Sort results by binding affinity
results.sort(key=lambda x: x[1])

# Save results to CSV file
csv_file = os.path.join(OUTPUT_DIR, "docking_results_drugbank.csv")
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Rank", "drugbank ID", "Binding Affinity (kcal/mol)"])
    for idx, (imphy_id, binding_affinity) in enumerate(results, start=1):
        writer.writerow([idx, imphy_id, binding_affinity])

print(f"Results have been saved to {csv_file}")
