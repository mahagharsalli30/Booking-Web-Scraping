# 🏨 North African Hotel Pricing & Satisfaction Monitor

A web scraping and business intelligence project that collects, cleans, and analyses hotel data from Booking.com across five North African countries — building Power BI dashboards to surface pricing patterns and guest satisfaction insights.

---

## 📌 Project Overview

| | |
|---|---|
| **Data source** | Booking.com (Selenium scraper) |
| **Countries covered** | Tunisia, Morocco, Algeria, Libya, Mauritania |
| **Cities** | Tunis, Marrakech, Algiers, Tripoli, Nouakchott |
| **Seasons scraped** | Spring (May), Summer (July), Low Season (September) |
| **Hotels in dataset** | 806 |
| **Total guest reviews** | ~540,000 |
| **Visualisation tool** | Microsoft Power BI |

---

## 🗂️ Project Structure

```
├── booking_scraper.py       # Selenium scraper — collects raw hotel data from Booking.com
├── clean_hotels2.py         # Data cleaning script — standardises and prepares the dataset
├── north_africa_hotels.csv  # Output dataset (generated after running the scraper)
└── dashboards/              # Power BI (.pbix) file with all four dashboards
```

---

## ⚙️ How It Works

### 1. Scraping (`booking_scraper.py`)

Uses **Selenium** and **ChromeDriver** to navigate Booking.com search result pages programmatically.

For each country/city and season combination, the scraper:
- Builds a Booking.com search URL with the correct check-in/check-out dates
- Scrolls the page to trigger lazy-loaded hotel cards
- Extracts from each card: hotel name, price, review score, review label, review count, and address/distance
- Retries up to 3 times on connection failure and saves progress incrementally to `north_africa_hotels.csv`

**Output columns:**

| Column | Description |
|---|---|
| `country` | Country name |
| `city` | City scraped |
| `season` | Season label (May_Spring, July_Summer, September_LowSeason) |
| `checkin` / `checkout` | Dates used for the search |
| `name` | Hotel name |
| `price` | Nightly rate as displayed on Booking.com |
| `score` | Numeric review score (e.g. 8.7) |
| `review_label` | Booking.com label (Excellent, Wonderful, etc.) |
| `review_count` | Number of reviews |
| `location` | Address or distance from downtown |

### 2. Cleaning (`clean_hotels2.py`)

Processes the raw CSV to prepare it for Power BI, including:
- Parsing numeric prices and scores from raw strings
- Extracting distance values from location text
- Handling missing values and deduplication
- Standardising column names and data types

### 3. Dashboards (Power BI)

Four dashboards built on the cleaned dataset:

| Dashboard | Focus |
|---|---|
| **1 — Regional Overview** | KPI cards (806 hotels, 8.41 avg score, 540K reviews) + hotel slicer |
| **2 — Price Distribution** | Average price by country, city, hotel name, and season |
| **3 — Distance vs. Price** | Scatter plot exploring whether city-centre proximity predicts price |
| **4 — Review Quality & Score** | Seasonal score trends, review label breakdown, country benchmarking |

---

## 🔍 Key Findings

- **Regional quality is strong**: the portfolio-wide average score is **8.41/10** (Excellent tier), backed by over half a million reviews.
- **Morocco is the most expensive** market (~370 TND avg); **Tunisia the most affordable**, representing a deliberate value-destination positioning.
- **Seasonal pricing is nearly flat** across the region — a missed revenue opportunity, especially given the measurable quality peak in Spring (May).
- **Distance from downtown does not predict price**: the market splits into city hotels and resort/beachfront hotels, and analyses that ignore this distinction are unreliable.
- **Algeria shows a value-for-money gap**: it is the second most expensive country yet scores lowest (~8.2), signalling guest dissatisfaction risk.
- **Spring (May) is the most strategically valuable season**: it is the only period where both price and satisfaction peak simultaneously.

---

## 🛠️ Requirements

```bash
pip install selenium webdriver-manager pandas
```

You will also need:
- **Google Chrome** installed
- **ChromeDriver** (managed automatically by `webdriver-manager`)

---

## 🚀 Running the Scraper

```bash
python booking_scraper.py
```

Progress is saved to `north_africa_hotels.csv` after each country/season combination, so the script is safe to interrupt and resume.

Then clean the data:

```bash
python clean_hotels2.py
```

Load the cleaned CSV into Power BI to explore the dashboards.

---

## ⚠️ Ethical & Legal Notice

This project was developed for academic research purposes as part of a university cybersecurity course (IT-360, Tunis Business School). Web scraping should always be conducted in accordance with the target website's Terms of Service and applicable data protection regulations. No personal user data was collected — only publicly visible hotel listings and aggregate review statistics.

---

## 👩‍💻 Authors

| Name | Email |
|---|---|
| Chadha Werghemi | chadha1werghemi@gmail.com |
| Maha Gharsalli | mahagharsalli3@gmail.com |
| Imen Saad | imensaad46@gmail.com |
| Roudayna Azizi | roudayna.az505@gmail.com |
| Sirine Othmene | sirineothmene1@gmail.com |

*Academic Year 2024–2025 — IT-360 Information Assurance and Security, Pr. Manel Abdelkader*