# Web Crawler for API Reconnaissance & Anti-Bot Evasion

## 📌 Overview
This project is part of a **Master’s Report in Cybersecurity & Information Operations** from the **University of Arizona**. It aims to develop a **Python-based web crawler** that progressively increases in complexity, from **basic web scraping** to **bypassing advanced anti-bot protections**.

The crawler aims to demonstrate:
- **Scraping static & dynamic web pages.**
- **Detecting API endpoints for reconnaissance & reverse engineering.**
- **Bypassing anti-bot defenses (Cloudflare, Akamai, Datadome).**
- **Utilizing Playwright, Puppeteer, Scrapy, Selenium, and BeautifulSoup.**

---

## 🚀 Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/ChristianTStu/web_crawler_project.git
   ```
2. **Navigate into the project folder:**
   ```bash
   cd web_crawler_project
   ```
3. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠 Features & Methodology
This project is divided into **4 progressive phases**:

### **1️⃣ Basic Crawler (Scrapy & BeautifulSoup)**
- Crawls and extracts **static web content** from simple pages.
- Stores structured data in **JSON/CSV format**.

### **2️⃣ JavaScript-Based Crawler (Playwright & Selenium)**
- Handles **JavaScript-heavy websites** (AJAX, dynamic loading).
- Simulates **user interactions** in a real browser.

### **3️⃣ API Endpoint Detection (Passive Reconnaissance)**
- Extracts **hidden API endpoints** from JavaScript files.
- Helps analyze **API security vulnerabilities**.

### **4️⃣ Advanced Crawler (Playwright & Puppeteer)**
- Implements **browser fingerprint spoofing** & **headless detection bypass**.
- Uses **proxy rotation & CAPTCHA solving** for anti-bot evasion.

---

## 📂 Project Structure
```plaintext
web_crawler_project/
│── crawlers/             # Web crawler scripts
│── logs/                 # Logs for debugging
│── results/              # Scraped data
│── tests/                # Unit tests
│── utils/                # Helper functions
│── venv/                 # Virtual environment (ignored by Git)
│── .gitignore            # Files to ignore
│── requirements.txt      # Dependencies list
│── main.py               # CLI tool entry point
│── README.md             # This file
```
---
## 🔹 Ethical & Legal Considerations
- **Testing is only conducted on legally permissible targets.**
- **Respects `robots.txt` policies where applicable.**
- **No unauthorized data extraction is performed.**
- **Compliance with data protection laws (GDPR, CCPA).**

---
## 📝 License

The MIT License (MIT)  

Copyright (c) 2025 Christian T Stuart  

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
