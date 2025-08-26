import time
import json
# from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# =============== CONFIG ===============
SITEMAP_URL = "https://www.gucci.com/us/en/sitemap/PRODUCT-en-0.xml"
MAX_PRODUCTS = 5  # For testing
OUTPUT_FILE = "gucci_products.json"

# =============== TIME CHECK (UTC) ===============
# utc_now = datetime.utcnow().time()
# if not (utc_now >= datetime.strptime("04:00", "%H:%M").time() and
#         utc_now <= datetime.strptime("08:45", "%H:%M").time()):
#     raise SystemExit("⛔ Not within allowed scraping hours (04:00–08:45 UTC).")

# =============== SETUP SELENIUM ===============
def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(options=options)
    return driver

# =============== GET PRODUCT URLS FROM SITEMAP USING SELENIUM ===============
def get_product_urls_with_selenium(driver, sitemap_url):
    driver.get(sitemap_url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    return urls[:MAX_PRODUCTS] # Testing purpose limit
    # return urls

# =============== EXTRACT PRODUCT DATA ===============
def extract_product_data(driver, url):
    driver.get(url)
    time.sleep(8)  # Allow time for page to fully load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        product_brand = "GUCCI"
        product_url = url
        image_urls = [div.contents[0].get("src") for div in soup.find_all("div", class_="image-wrapper")]
        product_name = soup.find("h1").get_text(strip=True)
        price_tag = soup.find("span", class_="is-text-medium").text
        product_id = soup.find("p").text.replace('\u200e', '')
        product_description = str(soup.find_all("header")[0].next_sibling.contents[0])
        product_details = [item.get_text(strip=True).replace('\\', '') for item in soup.select_one('ul[class*="product-details_product-details"]').contents if item.name]  # filters out things like '\n']
        colors = soup.find_all("input", class_="sr-only")
        product_colors = [str(color.next.contents[0]) for color in colors]
        product_color_primary = product_colors[0] if len(product_colors) > 0 else []
        categories = soup.find_all("span", attrs={"itemprop": True})
        category = str(categories[0].contents[0])
        sub_category = ""
        if len(categories) > 2:
            sub_category = str(categories[1].contents[0])
            if len(categories) == 3:
                sub_category = sub_category + " -> " + str(categories[2].contents[0])
        if category == "Women":
            gender = "Female"
        elif category == "Men":
            gender = "Male"
        else:
            gender = ""
        size_options = [span.get_text(strip=True) for span in soup.select('ul[aria-label="Sizes"] li span[class*="display-text"]')]

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

    return {
        "product_name": product_name,
        "product_id": product_id,
        "brand_name": product_brand,
        "category": category,
        "subcategory": sub_category,
        "gender_category": gender,
        "price_current": price_tag,
        "price_original": price_tag,
        "availability_status": True,
        "color_primary": product_color_primary,
        "color_secondary": product_colors,
        "material": product_details,
        "length_detail": size_options,
        "product_url": product_url,
        "image_urls": image_urls,
        "description_raw_text": product_description,
    }

# =============== MAIN SCRAPER LOOP ===============
def run_scraper():
    product_data = []
    driver = setup_driver()

    print("🔍 Getting product URLs from sitemap...")
    urls = get_product_urls_with_selenium(driver, SITEMAP_URL)

    for i, url in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] Scraping: {url}")
        data = extract_product_data(driver, url)
        if data:
            product_data.append(data)
        else:
            print("⚠️ Skipped due to missing fields or errors.")
        time.sleep(10)  # Respect Gucci's crawl delay

    driver.quit()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(product_data, f, indent=4)

    print(f"\n✅ Done! Saved {len(product_data)} products to '{OUTPUT_FILE}'")

# =============== RUN ===============
if __name__ == "__main__":
    run_scraper()
