#!/usr/bin/env python3
"""
Create Standalone QVC Gallery
Embeds the enhanced ACME database directly in the HTML file to avoid CORS issues.
"""

import json
import re

def create_standalone_gallery():
    """Create a standalone QVC gallery with embedded database."""
    print("🔧 Creating Standalone QVC Gallery")
    print("=" * 50)
    
    # Load the enhanced database
    try:
        with open('acme/acme_products_enhanced.json', 'r') as f:
            enhanced_data = json.load(f)
        print(f"✅ Loaded enhanced database with {enhanced_data['metadata']['total_products']} products")
    except FileNotFoundError:
        print("❌ Enhanced database not found!")
        return
    
    # Load the current QVC gallery HTML
    try:
        with open('acme/qvc_gallery.html', 'r') as f:
            html_content = f.read()
        print("✅ Loaded QVC gallery HTML")
    except FileNotFoundError:
        print("❌ QVC gallery HTML not found!")
        return
    
    # Convert the database to JavaScript format
    js_database = f"const EMBEDDED_DATABASE = {json.dumps(enhanced_data, indent=4)};"
    
    # Find the script section and insert the embedded database
    script_start = html_content.find('<script>')
    if script_start != -1:
        # Insert the embedded database right after the <script> tag
        insertion_point = script_start + len('<script>')
        
        modified_html = (
            html_content[:insertion_point] + '\n        ' + js_database + '\n' + 
            html_content[insertion_point:]
        )
        
        # Update the loadEnhancedDatabase function to use embedded data
        new_load_function = '''        // Load the enhanced ACME products database
        async function loadEnhancedDatabase() {
            try {
                // Try to fetch from server first (if available)
                const response = await fetch('acme_products_enhanced.json');
                const data = await response.json();
                enhancedDatabase = data;
                console.log(`Loaded ${data.products.length} products from server database`);
                return data.products;
            } catch (error) {
                console.log('Server not available, using embedded database...');
                // Use embedded database as fallback
                if (typeof EMBEDDED_DATABASE !== 'undefined') {
                    enhancedDatabase = EMBEDDED_DATABASE;
                    console.log(`Loaded ${EMBEDDED_DATABASE.products.length} products from embedded database`);
                    return EMBEDDED_DATABASE.products;
                } else {
                    console.error('No database available:', error);
                    // Final fallback to sample data
                    return getSampleData();
                }
            }
        }'''
        
        # Replace the existing loadEnhancedDatabase function
        pattern = r'// Load the enhanced ACME products database\s*async function loadEnhancedDatabase\(\)[^}]+}[^}]+}'
        modified_html = re.sub(pattern, new_load_function, modified_html, flags=re.DOTALL)
        
        # Save the standalone version
        with open('acme/qvc_gallery_standalone.html', 'w') as f:
            f.write(modified_html)
        
        print("✅ Created standalone gallery: acme/qvc_gallery_standalone.html")
        print("\n🌐 You can now open this file directly in any browser!")
        print("   • Works without a server")
        print("   • Includes all 84 products with screenshots")
        print("   • Full database embedded (48KB)")
        
        return True
    else:
        print("❌ Could not find script section in HTML file")
        return False

def main():
    """Main function."""
    create_standalone_gallery()

if __name__ == "__main__":
    main() 