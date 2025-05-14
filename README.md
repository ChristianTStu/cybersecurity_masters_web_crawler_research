# Web Crawler for API Reconnaissance & Anti-Bot Evasion

## 📌 Overview
This project is part of a **Master’s Report in Cybersecurity & Information Operations** from the **University of Arizona**. It aims to develop a **Python-based web crawler** that progressively increases in complexity, from **basic web scraping** to **bypassing advanced anti-bot protections**.

## Project Structure

```
web_crawler_project/
│── crawlers/              # Web crawler implementations
│   ├── basic/             # Phase 1: Basic web crawling techniques
│   │   ├── urllib_crawler.py         # Version 1: urllib implementation
│   │   ├── requests_crawler.py       # Version 2: requests implementation
│   │   └── scrapy_bs_crawler.py      # Version 3: Scrapy and BeautifulSoup 
│   │
│   ├── intermediate/      # Phase 2: Intermediate techniques
│   │   ├── httpx_basic.py            # Version 1: Basic httpx approach
│   │   ├── httpx_enhanced.py         # Version 2: Enhanced headers approach
│   │   └── httpx_extraction.py       # Version 3: Data extraction and output
│   │
│   └── advanced/         # Phase 3: Advanced techniques
│       ├── playwright_single.py      # Version 1: Direct API access
│       ├── playwright_batch.py       # Version 2: Batch processing
│       └── playwright_proxy.py       # Version 3: Proxy and field filtering
│
│── utils/                # Helper functions
│   ├── header_generator.py           # Browser-like header generation
│   └── proxy_manager.py              # Proxy rotation utilities
│
│── results/              # Scraped data output
│   ├── basic_crawler_products.json
│   ├── intermediate_crawler_products.json
│   └── advanced_crawler_products.json
│
│── logs/                 # Logs for debugging
│
│── .env.example          # Example environment variables
│── requirements.txt      # Dependencies list
│── main.py               # CLI tool entry point
│── README.md             # This file
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

4. Create a `.env` file from the example (for proxy support):
```bash
cp .env.example .env
```

## Usage

### Basic Crawler

```bash
# Run the urllib implementation
python -m crawlers.basic.urllib_crawler

# Run the requests implementation
python -m crawlers.basic.requests_crawler

# Run the Scrapy and BeautifulSoup implementation
python -m crawlers.basic.scrapy_bs_crawler
```

### Intermediate Crawler

```bash
# Run the basic httpx implementation
python -m crawlers.intermediate.httpx_basic

# Run the enhanced headers implementation
python -m crawlers.intermediate.httpx_enhanced

# Run the data extraction implementation
python -m crawlers.intermediate.httpx_extraction
```

### Advanced Crawler

```bash
# Run the single product API implementation
python -m crawlers.advanced.playwright_single

# Run the batch processing implementation
python -m crawlers.advanced.playwright_batch

# Run the proxy rotation implementation
python -m crawlers.advanced.playwright_proxy
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
