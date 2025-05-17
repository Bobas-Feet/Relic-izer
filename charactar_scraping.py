from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

TARGET_FILE = "lists_database.py"  # target existing .py file

# Set up Chrome in headless mode
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


try:
    driver.get("https://swgoh.gg/characters/")
    time.sleep(5)

    elements = driver.find_elements(By.CLASS_NAME, "unit-card__name")
    names = [el.text.strip() for el in elements if el.text.strip()]

    if names:
        sorted_names = sorted(names)

        # Build the replacement list string
        list_lines = ["character_names = ["]
        for name in sorted_names:
            safe_name = name.replace('"', r'\"')  # Escape internal double quotes
            list_lines.append(f'    "{safe_name}",')
        list_lines.append("]")
        list_str = "\n".join(list_lines)

        # Read the existing file content
        with open(TARGET_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace existing character_names list using regex
        updated_content, count = re.subn(
            r'character_names\s*=\s*\[(?:.|\n)*?\]',
            list_str,
            content,
            flags=re.DOTALL
        )

        if count == 0:
            print("No existing 'character_names' list found — consider inserting manually.")
        else:
            with open(TARGET_FILE, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"'character_names' updated successfully in {TARGET_FILE}")

    else:
        print("No character names found — check selectors or site structure.")
finally:
    driver.quit()
