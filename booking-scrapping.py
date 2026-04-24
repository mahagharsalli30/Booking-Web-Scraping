from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import re

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

countries = {
    "Tunisia": "Tunis",
    "Morocco": "Marrakech",
    "Algeria": "Algiers",
    "Libya": "Tripoli",
    "Mauritania": "Nouakchott"
}

date_scenarios = [
    ("2026-05-10", "2026-05-11", "May_Spring"), 
    ("2026-07-10", "2026-07-11", "July_Summer"), 
    ("2026-09-10", "2026-09-11", "September_LowSeason")
]

all_data = []

# -----------------------------
# EXTRACT SIZE FUNCTION
# -----------------------------
def extract_size(features_text):
    if features_text == "N/A":
        return "N/A"

    match = re.search(r"(\d+)\s*m²", features_text)
    return match.group(1) if match else "N/A"

# -----------------------------
# EXTRACT BEDROOMS
# -----------------------------
def extract_bedrooms(features_text):
    if features_text == "N/A":
        return "N/A"

    match = re.search(r"(\d+)\s*bedroom", features_text.lower())
    return match.group(1) if match else "1"  # default = 1 if not mentioned

# -----------------------------
# EXTRACT FACILITY TYPE
# -----------------------------
def extract_facility_type(features_text):
    if features_text == "N/A":
        return "N/A"

    keywords = ["studio", "apartment", "villa", "suite", "room"]
    for word in keywords:
        if word in features_text.lower():
            return word.capitalize()

    return "Other"


for country, city in countries.items():

    for checkin, checkout, season in date_scenarios:

        print(f"\n🌍 Scraping {country} - {city} | {season}")

        url = f"https://www.booking.com/searchresults.html?ss={city}&checkin_year={checkin[:4]}&checkin_month={checkin[5:7]}&checkin_monthday={checkin[8:]}&checkout_year={checkout[:4]}&checkout_month={checkout[5:7]}&checkout_monthday={checkout[8:]}"

        driver.get(url)
        time.sleep(10)

        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")

        for card in cards:

            try:
                name = card.find_element(By.CSS_SELECTOR, "div[data-testid='title']").text
            except:
                name = "N/A"

            try:
                price = card.find_element(By.CSS_SELECTOR, "[data-testid='price-and-discounted-price']").text
            except:
                price = "N/A"

            try:
                review_block = card.find_element(By.CSS_SELECTOR, "div[data-testid='review-score']").text.split("\n")

                score = "N/A"
                review_label = "N/A"
                review_count = "N/A"

                for line in review_block:
                    clean = line.strip()

                    if clean.replace(".", "").isdigit():
                        score = clean
                    elif "review" in clean.lower():
                        review_count = clean
                    elif clean.lower() not in ["scored", ""]:
                        review_label = clean

            except:
                score = review_label = review_count = "N/A"

            try:
                features = card.find_element(By.CSS_SELECTOR, "div[data-testid='property-card-unit-configuration']").text
            except:
                features = "N/A"

            # -----------------------------
            # NEW EXTRACTIONS
            # -----------------------------
            facility_size = extract_size(features)
            num_bedrooms = extract_bedrooms(features)
            facility_type = extract_facility_type(features)

            all_data.append({
                "country": country,
                "season": season,

                "name": name,
                "price": price,
                "score": score,
                "review_label": review_label,
                "review_count": review_count,

                "facility_size_m2": facility_size,
                "num_bedrooms": num_bedrooms,
                "facility_type": facility_type
            })

driver.quit()

df = pd.DataFrame(all_data)
df.to_csv("north_africa_final_dataset_cleaned.csv", index=False)

print(df.head())