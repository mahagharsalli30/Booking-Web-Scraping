from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

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

for country, city in countries.items():

    for checkin, checkout, season in date_scenarios:

        print(f"\n Scraping {country} - {city} | {season}")

        url = (
            f"https://www.booking.com/searchresults.html?ss={city}"
            f"&checkin_year={checkin[:4]}&checkin_month={checkin[5:7]}&checkin_monthday={checkin[8:]}"
            f"&checkout_year={checkout[:4]}&checkout_month={checkout[5:7]}&checkout_monthday={checkout[8:]}"
        )

        # Retry up to 3 times in case of connection drop
        loaded = False
        for attempt in range(3):
            try:
                driver.get(url)
                time.sleep(10)
                loaded = True
                break
            except Exception as e:
                print(f"   [!] Connection error (attempt {attempt+1}/3): {e}")
                print(f"   Waiting 15 seconds before retry...")
                time.sleep(15)

        if not loaded:
            print(f"   [X] Skipping {country} {season} after 3 failed attempts")
            continue

        # Scroll to load more cards
        for _ in range(3):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            except:
                break

        cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")
        print(f"   Found {len(cards)} cards")

        for card in cards:

            # Hotel name
            try:
                name = card.find_element(By.CSS_SELECTOR, "div[data-testid='title']").text
            except:
                name = "N/A"

            # Price
            try:
                price = card.find_element(By.CSS_SELECTOR, "[data-testid='price-and-discounted-price']").text
            except:
                price = "N/A"

            # Review score, label, count
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

            

            # Location / neighborhood
            try:
                location = card.find_element(
                    By.CSS_SELECTOR, "span[data-testid='address']"
                ).text.strip()
            except:
                try:
                    location = card.find_element(
                        By.CSS_SELECTOR, "[data-testid='distance']"
                    ).text.strip()
                except:
                    location = "N/A"

            all_data.append({
                "country":      country,
                "city":         city,
                "season":       season,
                "checkin":      checkin,
                "checkout":     checkout,
                "name":         name,
                "price":        price,
                "score":        score,
                "review_label": review_label,
                "review_count": review_count,
                "location":     location,
            })

        # Save progress after every country+season combo
        # so data won't be lost if the connection drops again
        pd.DataFrame(all_data).to_csv("north_africa_hotels.csv", index=False, encoding="utf-8-sig")
        print(f"   Progress saved — {len(all_data)} records so far")

driver.quit()

df = pd.DataFrame(all_data)
df.to_csv("north_africa_hotels.csv", index=False, encoding="utf-8-sig")
print(f"\nDone! {len(df)} records saved to north_africa_hotels.csv")
print(df.head(10))
