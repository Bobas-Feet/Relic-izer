from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import time
import re
import requests
from bs4 import BeautifulSoup
import time

# Set up Chrome in headless mode
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 5)
TARGET_FILE = "lists_database.py"  # target existing .py file
url = "https://swgoh.gg/characters/"

def gather_character_names():
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


def fetch_status_effects():
    driver.get(url)
    effect_to_characters = {}

    try:
        # Step 1–3: Open Filters and Ability Classes tab
        filters_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "body > div.global-container > main > div > div > div.l-sidebar__main > div.js-unit-search > div.paper > div > div:nth-child(3) > button")))
        filters_button.click()

        ability_classes_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "#unit-active-filter-tab-ac")))
        ability_classes_tab.click()

        # Step 4: Scrape the status effect names
        effects_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#unit-active-filter-content-ac")))
        effect_elements = effects_container.find_elements(By.TAG_NAME, "a")

        for i in range(len(effect_elements)):
            # Step 5: Refresh page to reset DOM each time
            driver.get(url)
            filters_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                "body > div.global-container > main > div > div > div.l-sidebar__main > div.js-unit-search > div.paper > div > div:nth-child(3) > button")))
            filters_button.click()
            ability_classes_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#unit-active-filter-tab-ac")))
            ability_classes_tab.click()
            effects_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#unit-active-filter-content-ac")))
            effect_elements = effects_container.find_elements(By.TAG_NAME, "a")

            effect_button = effect_elements[i]
            effect_name = effect_button.text.strip()
            if not effect_name:
                continue
            effect_button.click()

            # Step 6: Scrape character names
            time.sleep(1.5)
            character_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "unit-card__name")))
            character_names = sorted({card.text.strip() for card in character_cards if card.text.strip()})

            effect_to_characters[effect_name] = character_names

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

    return effect_to_characters

def write_to_database(status_effects):
    lines = ["status_effects = {"]
    for effect, names in sorted(status_effects.items()):
        safe_effect = effect.replace('"', r'\"')
        lines.append(f'    "{safe_effect}": [')
        for i in range(0, len(names), 5):
            chunk = names[i:i + 5]
            escaped = [name.replace('"', r'\"') for name in chunk]
            joined = ', '.join(f'"{name}"' for name in escaped)
            lines.append(f'        {joined},')
        lines.append("    ],")
    lines.append("}")
    dict_str = "\n".join(lines)

    try:
        path = Path(TARGET_FILE)
        if path.exists():
            content = path.read_text(encoding="utf-8")
        else:
            content = ""

        updated_content, count = re.subn(
            r'status_effects\s*=\s*\{(?:.|\n)*?\}',
            dict_str,
            content,
            flags=re.DOTALL
        )

        if count == 0:
            updated_content = content + ("\n\n" if content else "") + dict_str
        path.write_text(updated_content, encoding="utf-8")
    except Exception as e:
        print(f"❌ Failed to update file: {e}")


# Run the script
if __name__ == "__main__":
    # ------Status effects (buffs and debuffs list)-----
    effects_map = fetch_status_effects()
    write_to_database(effects_map)
    # toon_names = gather_character_names()

    #     print("\n--- Status Effects Found ---")
    #     for effect in effects:
    #         print(effect)
    #
    #     return effects
    #
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return []
    #
    # finally:
    #     time.sleep(2)
    #     driver.quit()

# def write_status_effects_to_file(effects):
#     if not effects:
#         print("No effects to write.")
#         return
#
#     list_lines = ["status_effects = ["]
#     for effect in effects:
#         safe_effect = effect.replace('"', r'\"')
#         list_lines.append(f'    "{safe_effect}",')
#     list_lines.append("]")
#     list_str = "\n".join(list_lines)
#
#     try:
#         with open(TARGET_FILE, "r", encoding="utf-8") as f:
#             content = f.read()
#
#         updated_content, count = re.subn(
#             r'status_effects\s*=\s*\[[^\]]*\]',
#             list_str,
#             content,
#             flags=re.DOTALL
#         )
#
#         if count == 0:
#             updated_content = content.strip() + "\n\n" + list_str
#             print("No existing 'status_effects' list found — inserted at end of file.")
#
#         with open(TARGET_FILE, "w", encoding="utf-8") as f:
#             f.write(updated_content)
#         print(f"'status_effects' updated successfully in {TARGET_FILE}")
#
#     except FileNotFoundError:
#         print(f"Target file '{TARGET_FILE}' not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

fetch_status_effects()
# gather_character_names()
# write_status_effects_to_file(effects)