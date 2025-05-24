#!/usr/bin/env python3
"""
ACME Products Extractor
Parses the Looney Tunes Wiki mhtml file to extract ACME product information.
"""

import re
import json
import os
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

def extract_mhtml_content(mhtml_file):
    """Extract HTML content from MHTML file."""
    with open(mhtml_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find the main HTML content after the MHTML headers
    html_start = content.find('<html')
    if html_start == -1:
        html_start = content.find('<HTML')
    
    if html_start != -1:
        return content[html_start:]
    
    return content

def parse_acme_products(html_content):
    """Parse ACME products from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all tables
    tables = soup.find_all('table')
    products = []
    
    for table in tables:
        # Look for table rows that might contain product data
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 4:  # Assuming at least 4 columns: Screenshot, Product Name, Usage, Episode, Series
                # Check if this looks like a product row
                product_data = {}
                for i, cell in enumerate(cells):
                    text = cell.get_text(strip=True)
                    
                    # Extract images (screenshots)
                    images = cell.find_all('img')
                    if images:
                        product_data['screenshot_url'] = images[0].get('src', '')
                        if product_data['screenshot_url'].startswith('//'):
                            product_data['screenshot_url'] = 'https:' + product_data['screenshot_url']
                    
                    # Store cell content
                    if i == 0 and not text:  # Likely screenshot column
                        continue
                    elif i == 1 or (i == 0 and text):  # Product name
                        product_data['product_name'] = text
                    elif 'usage' not in product_data and text:  # Usage
                        product_data['usage'] = text
                    elif 'episode' not in product_data and text:  # Episode
                        product_data['episode'] = text
                    elif 'series' not in product_data and text:  # Series
                        product_data['series'] = text
                
                # Only add if we have a product name
                if product_data.get('product_name') and len(product_data.get('product_name', '')) > 2:
                    products.append(product_data)
    
    return products

def extract_series_abbreviations(html_content):
    """Extract the series abbreviations key."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    abbreviations = {
        'LT': 'Looney Tunes',
        'MM': 'Merrie Melodies',
        'TTA': 'Tiny Toon Adventures',
        'AMS': 'Animaniacs',
        'TM': 'Taz-Mania',
        'STM': 'The Sylvester and Tweety Mysteries',
        'DD': 'Duck Dodgers',
        'TLTS': 'The Looney Tunes Show',
        'PATB': 'Pinky and the Brain'
    }
    
    # Try to find the abbreviations in the text
    text = soup.get_text()
    lines = text.split('\n')
    
    for line in lines:
        if '=' in line and any(abbr in line for abbr in abbreviations.keys()):
            parts = line.split('=')
            if len(parts) == 2:
                abbr = parts[0].strip()
                full_name = parts[1].strip()
                if abbr in abbreviations:
                    abbreviations[abbr] = full_name
    
    return abbreviations

def download_screenshot(url, filename):
    """Download a screenshot image."""
    try:
        if not url or not url.startswith('http'):
            return False
            
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        os.makedirs('acme/screenshots', exist_ok=True)
        filepath = f'acme/screenshots/{filename}'
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {filename}")
        return True
        
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def main():
    """Main function to extract ACME products."""
    mhtml_file = 'acme/List of ACME Products _ Looney Tunes Wiki _ Fandom.mhtml'
    
    if not os.path.exists(mhtml_file):
        print(f"MHTML file not found: {mhtml_file}")
        return
    
    print("Extracting HTML content from MHTML file...")
    html_content = extract_mhtml_content(mhtml_file)
    
    print("Parsing ACME products...")
    products = parse_acme_products(html_content)
    
    print("Extracting series abbreviations...")
    abbreviations = extract_series_abbreviations(html_content)
    
    print(f"Found {len(products)} products")
    
    # Save to JSON
    data = {
        'series_abbreviations': abbreviations,
        'products': products,
        'total_count': len(products)
    }
    
    with open('acme/acme_products.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Saved to acme/acme_products.json")
    
    # Download screenshots
    print("Downloading screenshots...")
    for i, product in enumerate(products):
        if 'screenshot_url' in product and product['screenshot_url']:
            filename = f"product_{i:03d}_{product.get('product_name', 'unknown').replace(' ', '_').replace('/', '_')[:50]}.jpg"
            # Clean filename
            filename = re.sub(r'[^\w\-_\.]', '_', filename)
            download_screenshot(product['screenshot_url'], filename)
    
    # Print summary
    print("\n=== ACME PRODUCTS SUMMARY ===")
    print(f"Total products found: {len(products)}")
    print("\nSeries abbreviations:")
    for abbr, full_name in abbreviations.items():
        print(f"  {abbr} = {full_name}")
    
    print("\nFirst 5 products:")
    for i, product in enumerate(products[:5]):
        print(f"{i+1}. {product.get('product_name', 'Unknown')}")
        if 'episode' in product:
            print(f"   Episode: {product['episode']}")
        if 'series' in product:
            print(f"   Series: {product['series']}")
        print()

if __name__ == "__main__":
    main() 