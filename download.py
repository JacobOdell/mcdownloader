import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# ========== CONFIG ==========
MOD_LINKS = [
    "https://www.curseforge.com/minecraft/mc-mods/xaeros-world-map"
]

MINECRAFT_VERSION = "1.20.1"
MODLOADER = "Forge"
DOWNLOAD_DIR = os.path.abspath("mods_1.20.1")
# =============================

# Setup Firefox with proper download handling
options = Options()
options.headless = False  # Set to True after testing if needed

# Set download preferences directly on the options
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", DOWNLOAD_DIR)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/java-archive,application/x-java-archive,application/octet-stream")
options.set_preference("pdfjs.disabled", True)
options.set_preference("browser.download.manager.showWhenStarting", False)

driver = webdriver.Firefox(options=options)

# Create download directory
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

for url in MOD_LINKS:
    print(f"Checking: {url}")
    try:
        files_url = url.rstrip("/") + "/files"
        driver.get(files_url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        file_cards = soup.select("div.file-row") 
        
        print(type(file_cards))
        print(len(file_cards))

        for card in file_cards:
            print("CARD:", card.text.strip())

            file_details = card.select_one("a.file-row-details")
            if not file_details:
                continue

            divs = file_details.find_all("div", recursive=False)
            
            for i in range(0, len(divs)):
                print(f"{i}: {divs[i].get_text(strip=True)}")

            mc_version_div = divs[4]
            modloader_text = divs[5].get_text(strip=True)
            mc_version_span = mc_version_div.select_one("div:nth-child(1) > span:nth-child(2)")
            mc_version_text = mc_version_span.get_text(strip=True)

            if MINECRAFT_VERSION not in mc_version_text:
                print(f"Skipping because: {mc_version_text}")
                continue
            if MODLOADER.lower() not in modloader_text.lower():
                print(f"Skipping because: {modloader_text}")
                continue

            file_page = "https://www.curseforge.com" + card.find("a")["href"]
            print(f"Found matching file: {file_page}")

            # Go to file page
            driver.get(file_page)
            time.sleep(3)

            # Click the download button
            download_button = driver.find_element(By.CSS_SELECTOR, "a.download-cta")
            download_button.click()

            print("Download initiated, waiting...")
            time.sleep(15)  # Wait for download to finish
            break
    except Exception as e:
        print(f"Error with {url}: {e}")
        time.sleep(10)

driver.quit()
print("\nAll done!")
