# LinkedIn Job Tracker

A Python-based tool that automates job searches on LinkedIn, extracts job listings, and exports the data. Built with **Selenium** for browser automation and optionally integrated with a **PyQt6 GUI**.

---

## 🧭 Project Structure

```
linkedin_job_tracker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point: runs from CLI or GUI
│   ├── database/
│   │   └── db.py               # Database setup & ORM models
│   ├── scraper/
│   │   └── linkedin_scraper.py # Contains the LinkedInJobScraper class
│   └── ui/
│       ├── ui_driver.py        # Provides Selenium WebDriver & WebDriverWait
│       └── ui_main.py          # Optional PyQt6 GUI window & widgets
│
├── tests/
│   └── test_*                  # Unit tests for business logic
├── requirements.txt            # Python dependencies
└── README.md                   # Project README (this file)
```

---

## ⚙️ Features

- ✅ Automated LinkedIn login
- 🔎 Keyword + location-based job search
- 🧩 Search filters and scrolling
- 📄 Extraction of job listings
- 💾 Export to CSV or database
- 🎨 Optional PyQt6 GUI interface

---

## ▶️ Getting Started

### Prerequisites

1. Install Python 3.11+
2. Install [Mozilla Firefox](https://www.mozilla.org/firefox/)
3. Download the appropriate WebDriver (e.g., [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/))

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/DeathHashira/linkedin_job_tracker.git
cd linkedin_job_tracker
```

2. **Set your credentials and driver path in the code**

Edit values directly in the relevant Python files (e.g., login credentials, driver path) as there is no `.env` file used.

---

## ▶️ Usage

### Run from Terminal

```bash
python -m app.main
```

This command will:

- Launch the browser
- Log in to LinkedIn
- Perform search and apply filters
- Extract job information
- Export data to CSV or database

---

## 🧩 Code Structure

### Core Class: `LinkedInJobScraper`

```python
class LinkedInJobScraper:
    def __init__(self, driver)
    def login(self)
    def search_combinations(self)
    def search(self)
    def filter(self)
    def go_to_job_url(self)
    def load_jobs(self)
    def extract_jobs(self)
    def export_jobs(self)
```

All functionality is handled inside this single class using Selenium WebDriver.

---

## ✅ Testing

Run tests using:

```bash
pytest
```

Tests ensure logic and data handling works correctly. Selenium automation is not tested in this setup.

---

## 📦 Data Export

Exported job data can be saved as:

- CSV files
- SQLite database (default)
- You can modify the `export_jobs()` method for additional formats

---

## 📞 Contact

For issues, feature requests, or contributions, please open an issue or submit a pull request.

---

Happy job hunting! 🚀
