#!/usr/bin/env python3
"""
Enhance ACME Database
Merges QVC gallery data with the clean ACME products database.
Adds emojis, pricing, and relative screenshot paths.
"""

import json
import os
import random
from pathlib import Path

def load_qvc_gallery_data():
    """Extract product data from the QVC gallery HTML."""
    # This is the data currently hardcoded in the HTML gallery
    qvc_products = [
        {
            "name": "Anvil",
            "episode": "LT/MM",
            "usage": "Classic gravity-powered percussive device. Perfect for dropping on unsuspecting roadrunners!",
            "price": "$299.99",
            "originalPrice": "$599.99",
            "emoji": "🗿"
        },
        {
            "name": "Super Outfit",
            "episode": "Fast and Furry-ous (LT)",
            "usage": "Doesn't give one the ability to fly, but looks great while falling!",
            "price": "$149.99",
            "originalPrice": "$299.99",
            "emoji": "🦸"
        },
        {
            "name": "Rocket-Powered Roller Skates",
            "episode": "Beep, Beep (MM)",
            "usage": "Let you skate at unlimited speed! Warning: May cause road burn.",
            "price": "$199.99",
            "originalPrice": "$399.99",
            "emoji": "🛼"
        },
        {
            "name": "Giant Kite Kit",
            "episode": "Zipping Along (MM)",
            "usage": "Can be used as a regular kite, or to fly and drop weapons. Assembly required.",
            "price": "$89.99",
            "originalPrice": "$179.99",
            "emoji": "🪁"
        },
        {
            "name": "Nitroglycerin",
            "episode": "Zipping Along (MM)",
            "usage": "HANDLE WITH EXTREME CARE! Not recommended for beginners.",
            "price": "$799.99",
            "originalPrice": "$1299.99",
            "emoji": "💥"
        },
        {
            "name": "Detonator",
            "episode": "Zipping Along (MM)",
            "usage": "Can be used as activation for explosives. Satisfaction guaranteed or your money back!",
            "price": "$129.99",
            "originalPrice": "$259.99",
            "emoji": "🧨"
        },
        {
            "name": "Bird Seed Ver. 2",
            "episode": "Stop! Look! And Hasten! (MM)",
            "usage": "Different box, same great taste! 'Silly kiddies, seeds are for birds!' (Parody of Trix)",
            "price": "$12.99",
            "originalPrice": "$24.99",
            "emoji": "🌱"
        },
        {
            "name": "Triple-Strength Fortified Leg Muscle Vitamins",
            "episode": "Stop! Look! And Hasten! (MM)",
            "usage": "Gives your legs the vitamins needed to run faster than ever before!",
            "price": "$59.99",
            "originalPrice": "$119.99",
            "emoji": "💊"
        },
        {
            "name": "Female Road Runner Costume",
            "episode": "Ready.. Set.. Zoom! (LT)",
            "usage": "Disguise yourself as a female Road Runner. Just watch out for other coyotes!",
            "price": "$179.99",
            "originalPrice": "$359.99",
            "emoji": "🐦"
        },
        {
            "name": "Smoke Screen Bomb",
            "episode": "Sheep Ahoy (MM)",
            "usage": "Creates a cloud of smoke for camouflage. Perfect for dramatic exits!",
            "price": "$39.99",
            "originalPrice": "$79.99",
            "emoji": "💨"
        },
        {
            "name": "Bat-Man's Outfit",
            "episode": "Gee Whiz-z-z-z-z-z-z (LT)",
            "usage": "Unlike the DC superhero, this outfit will actually let you fly high in the sky!",
            "price": "$499.99",
            "originalPrice": "$999.99",
            "emoji": "🦇"
        },
        {
            "name": "Dehydrated Boulders",
            "episode": "Scrambled Aches (LT)",
            "usage": "Makes instant boulders with just a drop of water. Compact and convenient!",
            "price": "$249.99",
            "originalPrice": "$499.99",
            "emoji": "🪨"
        },
        {
            "name": "Do-It-Yourself Tornado Kit",
            "episode": "Whoa, Be-Gone! (MM)",
            "usage": "Lets you 'seed' your own tornadoes. Weather manipulation made easy!",
            "price": "$1299.99",
            "originalPrice": "$2599.99",
            "emoji": "🌪️"
        },
        {
            "name": "Hi-Speed Tonic",
            "episode": "Hip- Hip- Hurry! (MM)",
            "usage": "Lets one run super fast! Side effects may include dizziness and dust clouds.",
            "price": "$79.99",
            "originalPrice": "$159.99",
            "emoji": "🏃"
        },
        {
            "name": "Indestructo Steel Ball",
            "episode": "Wild About Hurry (MM)",
            "usage": "Lets you roll in a ball that's literally indestructible. Fun for the whole family!",
            "price": "$399.99",
            "originalPrice": "$799.99",
            "emoji": "⚽"
        },
        {
            "name": "Christmas Package Machine",
            "episode": "Hopalong Casualty (LT)",
            "usage": "Puts anything and ANYONE into small packaged-wrapped presents.",
            "price": "$899.99",
            "originalPrice": "$1799.99",
            "emoji": "🎁"
        },
        {
            "name": "Earthquake Pills",
            "episode": "Hopalong Casualty (LT)",
            "usage": "Makes instant earthquakes! CAUTION: No effect on Road-Runners.",
            "price": "$699.99",
            "originalPrice": "$1399.99",
            "emoji": "🌍"
        },
        {
            "name": "Boomerang",
            "episode": "Zoom at the Top (MM)",
            "usage": "Guaranteed to return! Perfect for remote hunting applications.",
            "price": "$49.99",
            "originalPrice": "$99.99",
            "emoji": "🪃"
        },
        {
            "name": "Invisible Paint",
            "episode": "War and Pieces (LT)",
            "usage": "Makes anything completely invisible! Can you see the value?",
            "price": "$299.99",
            "originalPrice": "$599.99",
            "emoji": "🎨"
        },
        {
            "name": "TNT",
            "episode": "Multiple episodes (Various)",
            "usage": "Classic explosive for all your demolition needs. Reliable and effective!",
            "price": "$599.99",
            "originalPrice": "$1199.99",
            "emoji": "🧨"
        }
    ]
    return qvc_products

def generate_default_emoji_mapping():
    """Generate default emojis for products that don't have them."""
    emoji_categories = {
        'explosive': ['💥', '🧨', '💣', '🎆', '🔥'],
        'vehicle': ['🚗', '🛸', '🚁', '🛩️', '🚂'],
        'tool': ['🔨', '🔧', '⚒️', '🪓', '⛏️'],
        'weapon': ['⚔️', '🏹', '🪃', '🔫', '🛡️'],
        'clothing': ['👕', '🎽', '👔', '🧥', '👗'],
        'food': ['🌰', '🌱', '🍯', '🥜', '🌾'],
        'machine': ['⚙️', '🔩', '⚡', '🎛️', '🖲️'],
        'misc': ['📦', '🎪', '🎨', '🧪', '⭐']
    }
    
    def get_emoji_for_product(product_name):
        """Get appropriate emoji based on product name."""
        name_lower = product_name.lower()
        
        # Specific mappings
        if any(word in name_lower for word in ['tnt', 'bomb', 'explosive', 'grenade', 'earthquake']):
            return random.choice(emoji_categories['explosive'])
        elif any(word in name_lower for word in ['skate', 'bike', 'sled', 'unicycle', 'rocket']):
            return random.choice(emoji_categories['vehicle'])
        elif any(word in name_lower for word in ['outfit', 'costume', 'glove']):
            return random.choice(emoji_categories['clothing'])
        elif any(word in name_lower for word in ['seed', 'carrot', 'vitamin']):
            return random.choice(emoji_categories['food'])
        elif any(word in name_lower for word in ['kit', 'machine', 'motor', 'trap']):
            return random.choice(emoji_categories['machine'])
        elif any(word in name_lower for word in ['anvil', 'hammer', 'grease', 'glue']):
            return random.choice(emoji_categories['tool'])
        elif any(word in name_lower for word in ['boomerang', 'slingshot', 'bolt']):
            return random.choice(emoji_categories['weapon'])
        else:
            return random.choice(emoji_categories['misc'])
    
    return get_emoji_for_product

def find_screenshot_path(product_name, screenshots_dir='acme/screenshots'):
    """Find the screenshot file for a product."""
    if not os.path.exists(screenshots_dir):
        return None
    
    # Clean product name for filename matching
    clean_name = product_name.replace(' ', '_').replace('/', '_').replace('-', '_')
    clean_name = ''.join(c for c in clean_name if c.isalnum() or c in ['_', '.'])
    
    # Look for files that contain the product name
    for filename in os.listdir(screenshots_dir):
        if clean_name.lower() in filename.lower():
            return f"screenshots/{filename}"
    
    # Try partial matches
    name_words = clean_name.lower().split('_')
    for filename in os.listdir(screenshots_dir):
        filename_lower = filename.lower()
        if any(word in filename_lower for word in name_words if len(word) > 3):
            return f"screenshots/{filename}"
    
    return None

def generate_pricing(product_name):
    """Generate realistic pricing for products."""
    # Base prices based on product type
    base_prices = {
        'explosive': (500, 1500),
        'machine': (800, 3000),
        'vehicle': (200, 2000),
        'clothing': (50, 400),
        'tool': (25, 300),
        'misc': (10, 500)
    }
    
    name_lower = product_name.lower()
    
    # Determine category and price range
    if any(word in name_lower for word in ['tnt', 'bomb', 'explosive', 'earthquake']):
        min_price, max_price = base_prices['explosive']
    elif any(word in name_lower for word in ['machine', 'kit', 'tornado']):
        min_price, max_price = base_prices['machine']
    elif any(word in name_lower for word in ['skate', 'bike', 'sled', 'unicycle']):
        min_price, max_price = base_prices['vehicle']
    elif any(word in name_lower for word in ['outfit', 'costume']):
        min_price, max_price = base_prices['clothing']
    elif any(word in name_lower for word in ['anvil', 'grease', 'glue']):
        min_price, max_price = base_prices['tool']
    else:
        min_price, max_price = base_prices['misc']
    
    # Generate sale price and original price
    sale_price = random.randint(min_price, max_price)
    original_price = int(sale_price * random.uniform(1.5, 2.5))
    
    return f"${sale_price:.2f}", f"${original_price:.2f}"

def enhance_database():
    """Enhance the ACME products database with QVC gallery data."""
    print("🔧 Enhancing ACME Products Database")
    print("=" * 50)
    
    # Load existing clean database
    try:
        with open('acme/acme_products_clean.json', 'r') as f:
            clean_data = json.load(f)
        print(f"✅ Loaded clean database with {len(clean_data['products'])} products")
    except FileNotFoundError:
        print("❌ Clean database not found!")
        return
    
    # Load QVC gallery data
    qvc_data = load_qvc_gallery_data()
    qvc_lookup = {item['name']: item for item in qvc_data}
    print(f"✅ Loaded QVC gallery data with {len(qvc_data)} products")
    
    # Initialize emoji generator
    get_emoji = generate_default_emoji_mapping()
    
    # Enhance each product
    enhanced_products = []
    stats = {
        'total_products': 0,
        'with_screenshots': 0,
        'with_qvc_data': 0,
        'generated_emojis': 0,
        'generated_pricing': 0
    }
    
    for product in clean_data['products']:
        # Skip header rows
        if product.get('product_name') in ['Screenshot:', 'Product Name:', 'Product Name']:
            continue
        
        enhanced_product = product.copy()
        product_name = product.get('product_name', '')
        
        if not product_name or len(product_name) < 3:
            continue
        
        stats['total_products'] += 1
        
        # Check for existing screenshot URL and add relative path
        if 'screenshot_url' in product:
            stats['with_screenshots'] += 1
            # Find local screenshot file
            screenshot_path = find_screenshot_path(product_name)
            if screenshot_path:
                enhanced_product['local_screenshot'] = screenshot_path
        
        # Check if we have QVC data for this product
        qvc_match = None
        for qvc_name, qvc_item in qvc_lookup.items():
            if qvc_name.lower() in product_name.lower() or product_name.lower() in qvc_name.lower():
                qvc_match = qvc_item
                break
        
        if qvc_match:
            # Use QVC data
            enhanced_product['emoji'] = qvc_match['emoji']
            enhanced_product['price'] = qvc_match['price']
            enhanced_product['original_price'] = qvc_match['originalPrice']
            enhanced_product['enhanced_usage'] = qvc_match['usage']
            stats['with_qvc_data'] += 1
        else:
            # Generate missing data
            enhanced_product['emoji'] = get_emoji(product_name)
            stats['generated_emojis'] += 1
            
            sale_price, orig_price = generate_pricing(product_name)
            enhanced_product['price'] = sale_price
            enhanced_product['original_price'] = orig_price
            stats['generated_pricing'] += 1
            
            # Use existing usage or enhance it
            if 'usage' in product and product['usage']:
                enhanced_product['enhanced_usage'] = product['usage']
            else:
                enhanced_product['enhanced_usage'] = f"Premium ACME quality {product_name.lower()}!"
        
        # Add featured status for gallery
        enhanced_product['featured'] = product_name in [item['name'] for item in qvc_data[:20]]
        
        enhanced_products.append(enhanced_product)
    
    # Create enhanced database
    enhanced_data = {
        'metadata': {
            'version': '2.0',
            'enhancement_date': __import__('datetime').datetime.now().isoformat(),
            'total_products': stats['total_products'],
            'products_with_screenshots': stats['with_screenshots'],
            'products_with_qvc_data': stats['with_qvc_data'],
            'generated_emojis': stats['generated_emojis'],
            'generated_pricing': stats['generated_pricing']
        },
        'series_abbreviations': clean_data['series_abbreviations'],
        'products': enhanced_products,
        'total_count': len(enhanced_products)
    }
    
    # Save enhanced database
    with open('acme/acme_products_enhanced.json', 'w') as f:
        json.dump(enhanced_data, f, indent=2)
    
    print(f"\n📊 Enhancement Results:")
    print(f"   • Total products processed: {stats['total_products']}")
    print(f"   • Products with screenshots: {stats['with_screenshots']}")
    print(f"   • Products with QVC data: {stats['with_qvc_data']}")
    print(f"   • Generated emojis: {stats['generated_emojis']}")
    print(f"   • Generated pricing: {stats['generated_pricing']}")
    
    print(f"\n💾 Enhanced database saved to: acme/acme_products_enhanced.json")
    
    # Show some examples
    print(f"\n🎯 Sample Enhanced Products:")
    for i, product in enumerate(enhanced_products[:5]):
        name = product.get('product_name', 'Unknown')
        emoji = product.get('emoji', '❓')
        price = product.get('price', 'N/A')
        has_screenshot = '📸' if 'local_screenshot' in product else '❌'
        print(f"   {i+1}. {emoji} {name} - {price} {has_screenshot}")
    
    return enhanced_data

def main():
    """Main function."""
    enhance_database()

if __name__ == "__main__":
    main() 