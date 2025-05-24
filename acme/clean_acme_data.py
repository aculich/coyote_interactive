#!/usr/bin/env python3
"""
Clean ACME Products Data
Cleans up the extracted ACME data and prepares it for the comprehensive list.
"""

import json
import re
import html

def clean_text(text):
    """Clean up text from HTML encoding issues."""
    if not text:
        return text
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove HTML encoding artifacts
    text = re.sub(r'3D"', '"', text)
    text = re.sub(r'3D', '', text)
    text = re.sub(r'=\n', '', text)
    text = re.sub(r'=3D', '=', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&amp;', '&', text)
    
    # Clean up excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def clean_url(url):
    """Clean up URL from encoding issues."""
    if not url:
        return url
    
    url = clean_text(url)
    
    # Fix common URL encoding issues
    url = re.sub(r'^"?https:', 'https:', url)
    url = re.sub(r'".*$', '', url)
    url = url.split('=')[0] if '=' in url else url
    
    return url

def main():
    """Clean up the ACME products data."""
    
    # Load the raw data
    with open('acme/acme_products.json', 'r') as f:
        data = json.load(f)
    
    # Clean series abbreviations
    clean_abbreviations = {}
    for abbr, full_name in data['series_abbreviations'].items():
        clean_abbreviations[abbr] = clean_text(full_name)
    
    # Clean products
    clean_products = []
    
    for product in data['products']:
        # Skip header rows
        if product.get('product_name') in ['Product Name:', 'Product Name']:
            continue
        
        clean_product = {}
        
        for key, value in product.items():
            if key == 'screenshot_url':
                clean_product[key] = clean_url(value)
            else:
                clean_product[key] = clean_text(value)
        
        # Only add products with valid names
        if clean_product.get('product_name') and len(clean_product['product_name']) > 2:
            clean_products.append(clean_product)
    
    # Create cleaned data
    cleaned_data = {
        'series_abbreviations': clean_abbreviations,
        'products': clean_products,
        'total_count': len(clean_products)
    }
    
    # Save cleaned data
    with open('acme/acme_products_clean.json', 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    
    print(f"Cleaned data saved. Found {len(clean_products)} valid products.")
    
    # Print summary
    print("\n=== CLEANED ACME PRODUCTS SUMMARY ===")
    print(f"Total products: {len(clean_products)}")
    
    print("\nSeries abbreviations:")
    for abbr, full_name in clean_abbreviations.items():
        print(f"  {abbr} = {full_name}")
    
    print("\nSample products:")
    for i, product in enumerate(clean_products[:10]):
        print(f"{i+1}. {product['product_name']}")
        if 'episode' in product:
            print(f"   Episode: {product['episode']}")
        if 'series' in product:
            print(f"   Series: {product['series']}")
        if 'usage' in product:
            usage = product['usage'][:80] + "..." if len(product['usage']) > 80 else product['usage']
            print(f"   Usage: {usage}")
        print()

if __name__ == "__main__":
    main() 