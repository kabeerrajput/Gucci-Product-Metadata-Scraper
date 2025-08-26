# Gucci-Product-Metadata-Scraper
This repository contains a Python-based web scraper designed to extract product information from the official Gucci website. It utilizes Selenium for web automation and BeautifulSoup for parsing HTML content, collecting data such as product names, prices, descriptions, and more. The scraped data is then saved into a structured JSON file.

## Features
- Automated Scraping: Uses Selenium to navigate the Gucci website's sitemap and individual product pages.

- Data Extraction: Extracts a wide range of product metadata, including:

- Product Name, ID, and Brand

- Price (Current and Original)

- Category and Subcategory

- Color, Material, and Sizing details

- Raw description text and image URLs

- Structured Output: Saves all scraped data into a clean, easy-to-use JSON format.

- Robustness: Includes utility functions for handling common scraping challenges like element waiting and error handling.

## Files
- Gucci_MetaData.py: The main scraping script. It contains the core logic for setting up the web driver, navigating the site, extracting data, and saving the output.

- Selenium_Utils.py: A utility class with helper functions to simplify interactions with Selenium, such as waiting for elements and handling different browser actions.

- Model.py: A Python file defining the data model (dictionary structure) for the product information, which serves as a blueprint for the scraped data.

- gucci_products.json: An example output file containing a small sample of the scraped product data.

## Getting Started
### Prerequisites
- Python 3.x

- pip package manager

## Installation
- 1. Clone this repository:
     - git clone https://github.com/your-username/your-repository-name.git
     - cd your-repository-name

- 2. Install the required Python libraries:
     - pip install selenium
     - pip install beautifulsoup4
   

- 3. Ensure you have the appropriate Selenium WebDriver for your browser (e.g., ChromeDriver for Chrome). The script assumes chromedriver is in your system's PATH.
 
## Usage
To run the scraper, simply execute the main script from your terminal:
- python Gucci_MetaData.py

## Configuration
You can modify the following variables in Gucci_MetaData.py to customize the scraping process:

- SITEMAP_URL: The URL of the sitemap to scrape.

- MAX_PRODUCTS: The maximum number of products to scrape. This is useful for testing or limited runs. Set to None to scrape all products found in the sitemap.

- OUTPUT_FILE: The name of the JSON file where the data will be saved.

