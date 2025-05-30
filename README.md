# Web Crawler for API Reconnaissance & Anti-Bot Evasion

## 📌 Overview
This project is part of a **Master’s Report in Cybersecurity & Information Operations** from the **University of Arizona**. It aims to develop a **Python-based web crawler** that progressively increases in complexity, from **basic web scraping** to **bypassing advanced anti-bot protections**.

## Project Structure

```
web_crawler_project/
├── 1. Basic Crawler/            # Phase 1 scripts
│   ├── version01.py             # urllib implementation
│   ├── version02.py             # requests implementation
│   └── version03.py             # Scrapy + BeautifulSoup
├── 2. Intermediate Crawler/    # Phase 2 scripts
│   ├── version_01.py            # httpx baseline
│   ├── version_02.py            # enhanced headers
│   └── version_03.py            # Selectolax extraction
├── 3. Advanced Crawler/        # Phase 3 scripts
│   ├── version01.py             # Playwright single product
│   ├── version02.py             # Playwright batch processing
│   └── version03.py             # Playwright with proxy/filtering
├── 4. Ouputs/                  # Scraped data output
│   ├── basic_crawler_products.json
│   ├── intermediate_crawler_products.json
│   └── advanced_crawler_products.json
├── LICENSE
└── README.md
```

## Features

### Basic Crawler (Phase 1)
- Crawls and extracts static web content from simple pages
- Demonstrates fundamental HTTP request handling
- Stores structured data in JSON format
- Targets websites with minimal/no anti-bot protection

### Intermediate Crawler (Phase 2)
- Uses modern httpx and Selectolax libraries
- Implements enhanced header configurations to bypass basic protections
- Handles more complex HTML structures
- Demonstrates effective HTML parsing and data extraction
- Targets commercial websites with moderate anti-bot measures

### Advanced Crawler (Phase 3)
- Uses Playwright for API reconnaissance and direct backend access
- Implements proxy rotation for IP address anonymization
- Features selective field extraction and data transformation
- Bypasses sophisticated anti-bot measures
- Demonstrates enterprise-grade techniques for high-quality data extraction
- Targets websites with strong anti-bot protections

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ChristianTStu/web_crawler_project.git
cd web_crawler_project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. For the Advanced Crawler (Phase 3), you'll need to install browser dependencies for Playwright:
```bash
playwright install
```

4. (Optional) Create a `.env` file with proxy settings for the advanced crawler:
```bash
echo "PROXIES=https://username:password@host:port" > .env
```

## Usage

### Basic Crawler

```bash
# Run the urllib implementation
python "1. Basic Crawler/version01.py"

# Run the requests implementation
python "1. Basic Crawler/version02.py"

# Run the Scrapy and BeautifulSoup implementation
python "1. Basic Crawler/version03.py"
```

### Intermediate Crawler

```bash
# Run the basic httpx implementation
python "2. Intermediate Crawler/version_01.py"

# Run the enhanced headers implementation
python "2. Intermediate Crawler/version_02.py"

# Run the data extraction implementation
python "2. Intermediate Crawler/version_03.py"
```

### Advanced Crawler

```bash
# Run the single product API implementation
python "3. Advanced Crawler/version01.py"

# Run the batch processing implementation
python "3. Advanced Crawler/version02.py"

# Run the proxy rotation implementation
python "3. Advanced Crawler/version03.py"
```

## Ethical Considerations

This project is designed for educational purposes and legitimate cybersecurity research. Please use these tools responsibly:

- Always respect robots.txt directives
- Implement appropriate request delays to avoid overloading servers
- Only access publicly available data
- Comply with terms of service and legal requirements
- Do not use these techniques for unauthorized access or data collection

## License

This project is available for educational and research purposes. Please use responsibly and in accordance with all applicable laws and regulations.

## Author

Christian Stuart
University of Arizona
College of Applied Science & Technology
Master of Science in Cyber and Information Operations
Spring 2025
