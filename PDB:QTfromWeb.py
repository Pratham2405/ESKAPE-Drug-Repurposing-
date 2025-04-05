from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests
import time
import os

# Create output directory for pdb files
os.makedirs("pdbqt_structures", exist_ok=True)

# Configuration
INPUT_CSV = "imppat_druglike_ids.csv"
BASE_URL = "https://cb.imsc.res.in/imppat/phytochemical-detailedpage/"

# Setup Chrome driver (headless)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def download_pdb(imphy_id, pdb_url):
    response = requests.get(pdb_url, stream=True)
    if response.status_code == 200:
        file_size = int(response.headers.get('content-length', 0))
        pdb_file_path = os.path.join("pdbqt_structures", f"{imphy_id}.pdbqt")
        with open(pdb_file_path, 'wb') as pdb_file:
            downloaded = 0
            for data in response.iter_content(chunk_size=4096):
                downloaded += len(data)
                pdb_file.write(data)
                print(f"\rDownloading {imphy_id}.pdbqt: {downloaded}/{file_size} bytes", end='')
        print(f"\n✅ Downloaded: {imphy_id}.pdbqt")
        return True
    else:
        print(f"❌ Failed to download {imphy_id}.pdbqt (HTTP Status: {response.status_code})")
        return False

try:
    # Read IMPHY IDs from CSV using Pandas
    df = pd.read_csv(INPUT_CSV)
    imphy_ids = df['IMPHY_ID'].tolist()

    # Iterate through each IMPHY ID to download PDB files
    # In case you want to start with a particular index. Apply the below code:
    start_index = 1110

# Iterate through IMPHY IDs starting from the nth structure
    for idx, imphy_id in enumerate(imphy_ids[start_index:], start=start_index+1):
    # for idx, imphy_id in enumerate(imphy_ids):
        url = f"{BASE_URL}{imphy_id}"
        driver.get(url)
        print(f"Processing {idx+1}/{len(imphy_ids)}: {imphy_id}")

        try:
            # Wait explicitly for the PDB download link/button to load
            pdb_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[contains(@href, '_3D.pdbqt') and contains(., '3D PDBQT')]")
                )
            )

            pdb_relative_url = pdb_element.get_attribute('href')
            pdb_url = f"https://cb.imsc.res.in{pdb_relative_url}" if pdb_relative_url.startswith('/') else pdb_relative_url

            # Download the PDB file
            if download_pdb(imphy_id, pdb_url):
                # Verify file size
                file_path = os.path.join("pdbqt_structures", f"{imphy_id}.pdbqt")
                file_size = os.path.getsize(file_path)
                if file_size > 0:
                    print(f"✅ Verified: {imphy_id}.pdbqt (Size: {file_size} bytes)")
                else:
                    print(f"❌ Verification failed: {imphy_id}.pdbqt (Size: 0 bytes)")
            
        except Exception as e:
            print(f"❌ Error processing {imphy_id}: {str(e)}")

        # Polite delay between requests
        time.sleep(2)

    print("\n🎉 All available PDBQT files have been processed.")

except Exception as e:
    print(f"Critical error: {str(e)}")

finally:
    driver.quit()
