import os
import subprocess
from rdkit import Chem
from rdkit.Chem import AllChem
import shutil

def prepare_pdbqt(input_sdf, output_dir, faulty_dir):
    """Convert SDF to PDBQT with comprehensive error checking"""
    try:
        # 1. Load molecule with sanitization
        mol = Chem.MolFromMolFile(input_sdf, sanitize=True)
        if mol is None:
            raise ValueError("Failed to load molecule")

        # 2. Add hydrogens while preserving coordinates
        mol = Chem.AddHs(mol, addCoords=True)

        # 3. Generate 3D coordinates with multiple attempts
        embed_result = AllChem.EmbedMolecule(mol, 
                                           maxAttempts=50,
                                           useRandomCoords=True)
        if embed_result == -1:
            raise RuntimeError("Embedding failed after 50 attempts")

        # 4. Energy minimization with convergence check
        minimize_result = AllChem.UFFOptimizeMolecule(mol, maxIters=500)
        if minimize_result == -1:
            print(f"Warning: Minimization didn't converge for {input_sdf}")

        # 5. Temporary PDB file creation
        temp_pdb = os.path.join(output_dir, "temp.pdb")
        Chem.MolToPDBFile(mol, temp_pdb)

        # 6. Open Babel conversion with charge assignment
        output_pdbqt = os.path.join(output_dir, 
                                  os.path.basename(input_sdf).replace(".sdf", ".pdbqt"))
        cmd = f"obabel {temp_pdb} -O {output_pdbqt} -xh --partialcharge gasteiger"
        subprocess.run(cmd, shell=True, check=True)
        
        print(f"Success: {input_sdf} -> {output_pdbqt}")
        return True

    except Exception as e:
        print(f"Error processing {input_sdf}: {str(e)}")
        # Move faulty file
        dest = os.path.join(faulty_dir, os.path.basename(input_sdf))
        shutil.move(input_sdf, dest)
        print(f"Moved faulty file to: {dest}")
        return False

def batch_convert(input_dir, output_dir, faulty_dir):
    """Batch process with progress tracking"""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(faulty_dir, exist_ok=True)
    
    sdf_files = [f for f in os.listdir(input_dir) if f.endswith(".sdf")]
    total = len(sdf_files)
    
    for idx, sdf_file in enumerate(sdf_files, 1):
        input_path = os.path.join(input_dir, sdf_file)
        print(f"Processing {idx}/{total}: {sdf_file}")
        prepare_pdbqt(input_path, output_dir, faulty_dir)

# Usage
input_dir = "/Users/prathamdhanoa/Downloads/Docking/molecule-generator-master/drive-download-20250104T145431Z-001/NCAT/VS_mols"
output_dir = "/Users/prathamdhanoa/Downloads/Docking/molecule-generator-master/drive-download-20250104T145431Z-001/NCAT/drugbank_3D_PDBQT" 
faulty_dir = "/Users/prathamdhanoa/Downloads/Docking/molecule-generator-master/drive-download-20250104T145431Z-001/NCAT/faulty_RDKit"

batch_convert(input_dir, output_dir, faulty_dir)
