import os
import subprocess
import glob
import csv
import shutil
import concurrent.futures  # Added for parallel processing

# Configuration constants (unchanged)
RECEPTOR_FILE = "/Users/prathamdhanoa/Downloads/Docking/molecule-generator-master/drive-download-20250104T145431Z-001/NCAT/3X1J/3X1J.pdbqt"
LIGAND_DIR = "/Users/prathamdhanoa/Downloads/Docking/VS_Config/pdbqt_structures"
OUTPUT_DIR = "/Users/prathamdhanoa/Downloads/Docking/VS_Config/output_coaD_3X1J"
CONF_FILE = "/Users/prathamdhanoa/Downloads/Docking/VS_Config/VS_Config_3X1J.txt"
VINA_PATH = "/opt/homebrew/bin/Vina"
FAULTY_DIR = "/Users/prathamdhanoa/Downloads/Docking/VS_Config/faulty_structures"

# Create output directory if needed
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_vina_docking(receptor, ligand, config, out_pdbqt, out_log):
    """Run Vina-GPU docking with CPU parallelization"""
    try:
        # Added --cpu 1 to limit each Vina instance to 1 core
        cmd = f"{VINA_PATH} --receptor {receptor} --ligand {ligand} --config {config} --out {out_pdbqt} --cpu 1"
        subprocess.run(
            cmd,
            shell=True,
            check=True,
            timeout=120,
            stdout=open(out_log, 'w'),
            stderr=subprocess.STDOUT
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error processing {ligand}: {str(e)}")
        return False
    except subprocess.TimeoutExpired:
        print(f"Timeout (120s) exceeded for {ligand}")
        return False

def process_ligand(idx, total, ligand_file):
    """Process individual ligand in parallel, with index tracking"""
    ligand_name = os.path.splitext(os.path.basename(ligand_file))[0]
    out_pdbqt = os.path.join(OUTPUT_DIR, f"{ligand_name}_out.pdbqt")
    out_log = os.path.join(OUTPUT_DIR, f"{ligand_name}_log.txt")

    if os.path.exists(out_pdbqt) or os.path.exists(out_log):
        print(f"Skipping {ligand_name}: {idx+1}/{total} (already processed)")
        return True

    print(f"Processing {ligand_name}: {idx+1}/{total}")
    success = run_vina_docking(RECEPTOR_FILE, ligand_file, CONF_FILE, out_pdbqt, out_log)

    if not success:
        # Clean up failed outputs
        for fpath in [out_pdbqt, out_log]:
            if os.path.exists(fpath):
                os.remove(fpath)
        # Move faulty structure
        dest_path = os.path.join(FAULTY_DIR, os.path.basename(ligand_file))
        shutil.move(ligand_file, FAULTY_DIR)
        print(f"Moved faulty structure to: {dest_path}")
        return False
    return True

if __name__ == "__main__":
    ligand_files = sorted(glob.glob(os.path.join(LIGAND_DIR, "*.pdbqt")))
    total = len(ligand_files)

    with concurrent.futures.ProcessPoolExecutor(
        max_workers=min(os.cpu_count(), 64)
    ) as executor:
        # Pair each ligand with its index
        futures = {
            executor.submit(process_ligand, idx, total, lig): lig
            for idx, lig in enumerate(ligand_files)
        }

        for future in concurrent.futures.as_completed(futures):
            ligand_file = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Exception processing {ligand_file}: {e}")


    # Post-processing of results (unchanged)
    def parse_vina_results(log_file):
        lowest_affinity = None
        with open(log_file, 'r') as f:
            for line in f:
                if line.strip().startswith('1 '):
                    first_result = line.split()
                    if len(first_result) >= 2:
                        lowest_affinity = float(first_result[1])
                    break
        return lowest_affinity

    results = []
    for log_file in glob.glob(os.path.join(OUTPUT_DIR, "*_log.txt")):
        ligand_name = os.path.splitext(os.path.basename(log_file))[0].replace("_log", "")
        binding_affinity = parse_vina_results(log_file)
        if binding_affinity is not None:
            drugbank_id = ligand_name.split('_')[1]
            results.append((drugbank_id, binding_affinity))

    # Sort and save results
    results.sort(key=lambda x: x[1])
    csv_file = os.path.join(OUTPUT_DIR, "docking_results_drugbank_.csv")
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "drugbank ID", "Binding Affinity (kcal/mol)"])
        for idx, (drugbank_id, binding_affinity) in enumerate(results, start=1):
            writer.writerow([idx, drugbank_id, binding_affinity])

    print(f"Results have been saved to {csv_file}")
