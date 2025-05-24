# ACME Products Complete System

## Overview

Welcome to the **ACME Products Complete Shopping Network System** - a comprehensive implementation featuring every ACME product Wile E. Coyote ever used, complete with interactive shopping experiences, TV broadcasting, and YouTube episode integration!

> *"If it's ACME, it's gotta be good!"* - Wile E. Coyote (probably)

## 🎯 What's Implemented

### ✅ Complete Product Database
- **84 ACME products** extracted from the Looney Tunes Wiki
- Product names, usage descriptions, episode references
- **76 product screenshots** downloaded and organized
- Comprehensive episode and series information
- Clean JSON database with structured data

### ✅ QVC-Style Shopping Gallery  
- Interactive HTML gallery showcasing all products
- **4 Shopping Hosts** with unique personalities:
  - **Bob "Boom" Richardson** - Explosives Expert
  - **Sally Speedster** - Velocity Specialist  
  - **Chuck Contraption** - Gadget Guru
  - **Betty Bargain** - Deal Detective
- Product search and filtering
- Shopping cart functionality
- Animated product displays with host commentary

### ✅ TV/Audio Broadcasting System
- Integrated with existing coyote project infrastructure
- Text-to-speech product pitches
- TV display integration via `comment_on_television()`
- Multiple host personalities with catchphrases
- Continuous broadcasting mode
- Special shopping show mode
- Interactive command-line interface

### ✅ YouTube Episode Finder
- **25 unique episodes** identified from product database
- YouTube search query generation
- yt-dlp integration for downloading episodes
- Comprehensive episode guide with product cross-references
- Episode-to-product mapping

## 📁 File Structure

```
acme/
├── README.md                           # This file
├── ACME.md                            # Complete product documentation (454 lines)
├── YOUTUBE_GUIDE.md                   # Episode finder guide (277 lines)
│
├── 📊 Data Files
├── acme_products.json                 # Raw extracted data
├── acme_products_clean.json           # Cleaned structured data (84 products)
├── acme_products_enhanced.json        # Enhanced with additional metadata
│
├── 🎪 Interactive Gallery
├── qvc_gallery.html                   # Original gallery
├── qvc_gallery_standalone.html        # Complete standalone gallery (708 lines)
├── qvc_gallery_fixed.html             # Fixed version
│
├── 📺 Broadcasting System
├── tv_broadcaster.py                  # Main TV/audio broadcaster (393 lines)
├── demo_complete_system.py            # Complete system demo (328 lines)
│
├── 🎥 YouTube Integration
├── youtube_finder.py                  # Episode finder/downloader (361 lines)
│
├── 🛠️ Utilities
├── extract_acme_products.py           # MHTML parser (184 lines)
├── clean_acme_data.py                 # Data cleaning utility (113 lines)
├── enhance_acme_database.py           # Database enhancement (407 lines)
├── create_standalone_gallery.py       # Gallery generator (96 lines)
│
├── 🖼️ Media
├── screenshots/                       # 76 product images
├── *.mp4                             # Demo videos
├── *.mhtml                           # Source wiki files
└── *.webp                            # Banner images
```

## 🚀 Quick Start

### 1. Run the Complete Demo
```bash
# Full interactive demonstration
python acme/demo_complete_system.py

# Quick overview (no pauses)
python acme/demo_complete_system.py quick
```

### 2. Open the QVC Gallery
```bash
# Open the interactive shopping gallery
open acme/qvc_gallery_standalone.html
# or
python -m webbrowser acme/qvc_gallery_standalone.html
```

### 3. Start TV Broadcasting
```bash
# Interactive mode
python acme/tv_broadcaster.py

# Continuous broadcasting (every 30 seconds)
python acme/tv_broadcaster.py continuous 30

# Special 5-minute shopping show
python acme/tv_broadcaster.py show 5

# Demo mode (3 products)
python acme/tv_broadcaster.py demo
```

### 4. Find YouTube Episodes
```bash
# Interactive episode finder
python acme/youtube_finder.py

# Search for episodes
python acme/youtube_finder.py search

# Download episodes (requires yt-dlp)
python acme/youtube_finder.py download
```

## 🎮 Usage Examples

### Interactive TV Broadcasting
```bash
python acme/tv_broadcaster.py
```
Commands:
- `broadcast` or `b` - Broadcast random product
- `show 5` - 5-minute special shopping show
- `host bob` - Switch to Bob "Boom" Richardson
- `continuous` - Start continuous mode
- `list` - Show all products

### YouTube Episode Downloads
```bash
# Install yt-dlp first
pip install yt-dlp

# Download classic episodes
yt-dlp "ytsearch:Looney Tunes Fast and Furry-ous"
yt-dlp "ytsearch:Road Runner Beep Beep"
yt-dlp "ytsearch:Wile E Coyote compilation"
```

### Product Database Access
```python
import json
with open('acme/acme_products_clean.json', 'r') as f:
    data = json.load(f)
    products = data['products']  # 84 products
    series = data['series_abbreviations']  # 9 series
```

## 🔗 Integration with Coyote Project

The ACME system seamlessly integrates with the main coyote project:

### Text-to-Speech Integration
```python
from speak_text import speak_text
speak_text("Welcome to ACME! Today we have TNT on sale!")
```

### TV Display Integration  
```python
from comment_on_television import comment_on_television
comment_on_television("🏺 ACME PRODUCT SHOWCASE 🏺\n\nProduct: Anvil\nPrice: $99.99")
```

### Configuration Support
Uses existing `config.py` for system settings and hardware integration.

## 📊 System Capabilities

| Feature | Status | Details |
|---------|--------|---------|
| **Product Database** | ✅ Complete | 84 products, 25 episodes, 9 series |
| **Screenshots** | ✅ Complete | 76 product images downloaded |
| **QVC Gallery** | ✅ Complete | 4 hosts, interactive shopping |
| **TV Broadcasting** | ✅ Complete | TTS, TV display, multiple modes |
| **YouTube Integration** | ✅ Complete | Episode finder, download support |
| **Coyote Integration** | ✅ Complete | TTS, TV, config compatibility |
| **Documentation** | ✅ Complete | Comprehensive guides and examples |

## 🎪 Host Personalities

### Bob "Boom" Richardson - Explosives Expert
- **Voice:** Deep and authoritative
- **Catchphrases:** "That's explosive value!", "BOOM! Another satisfied customer!"
- **Specialty:** TNT, Bombs, Dynamite, Nitroglycerin

### Sally Speedster - Velocity Specialist  
- **Voice:** Energetic and fast-paced
- **Catchphrases:** "Faster than a speeding roadrunner!", "Beep beep! That's a great deal!"
- **Specialty:** Rocket Skates, Jet Motors, Speed Vitamins

### Chuck Contraption - Gadget Guru
- **Voice:** Intellectual and excited  
- **Catchphrases:** "The engineering is simply marvelous!", "Even Wile E. Coyote would be impressed!"
- **Specialty:** Complex gadgets, Kits, Scientific devices

### Betty Bargain - Deal Detective
- **Voice:** Friendly and persuasive
- **Catchphrases:** "What a steal!", "Your wallet will thank you!"
- **Specialty:** Finding the best deals and special offers

## 🎬 Notable Episodes & Products

| Episode | Featured Products | Series |
|---------|------------------|--------|
| **Fast and Furry-ous** | Super Outfit | LT |
| **Beep, Beep** | Matches, Rocket-Powered Roller Skates | MM |
| **Gee Whiz-z-z-z-z-z-z** | Bat-Man's Outfit, Jet Bike Kit, Giant Rubber Band | LT |
| **Zipping Along** | Giant Kite Kit, Nitroglycerin, Detonator | MM |
| **Wild About Hurry** | Giant Rubber Band V3, Indestructo Steel Ball | MM |

## 🛠️ Dependencies

### Required for Basic Functionality
- Python 3.8+
- JSON support (built-in)
- Web browser for gallery

### Optional for Full Features
- **yt-dlp** - For YouTube episode downloads
- **speak_text module** - For TTS (from main coyote project)
- **comment_on_television module** - For TV display (from main coyote project)

### Installation
```bash
# Install yt-dlp for YouTube features
pip install yt-dlp

# For macOS TTS fallback
# Uses built-in 'say' command

# Main coyote project modules should be available from parent directory
```

## 🎯 Demo Scenarios

### 1. Complete System Demo
```bash
python acme/demo_complete_system.py
```
Shows all features: product extraction, QVC gallery, TV broadcasting, YouTube finder, and system integration.

### 2. Shopping Experience Demo
1. Open `qvc_gallery_standalone.html`
2. Browse products by category
3. Switch between different hosts
4. Use search and filtering
5. Add items to cart

### 3. Broadcasting Demo
```bash
python acme/tv_broadcaster.py show 3
```
Demonstrates a 3-minute special shopping show with multiple products and dynamic host commentary.

### 4. Episode Discovery Demo
```bash
python acme/youtube_finder.py search
```
Shows how to find and download classic Looney Tunes episodes featuring ACME products.

## 🔄 What's Next

### Potential Enhancements
- [ ] **Real-time Price Updates** - Dynamic pricing based on demand
- [ ] **Customer Reviews** - Add Wile E. Coyote testimonials
- [ ] **Product Recommendations** - "Customers who bought TNT also bought..."
- [ ] **Inventory Tracking** - Stock levels and reorder alerts
- [ ] **Multi-language Support** - Broadcast in different languages
- [ ] **Voice Recognition** - Voice commands for TV broadcaster
- [ ] **Mobile App** - ACME shopping on the go
- [ ] **AR/VR Integration** - Try before you buy in the desert

### Integration Opportunities
- **GPIO Integration** - Physical buttons for product selection
- **LED Displays** - Show current deals and specials
- **Audio System** - Surround sound for dramatic product reveals
- **Camera Integration** - Live product demonstrations

## 🎪 Fun Facts

- **84 Products** extracted from the Looney Tunes Wiki
- **76 Screenshots** successfully downloaded (89.4% success rate)
- **25 Episodes** identified across 9 different series
- **4 Unique Hosts** with distinct personalities and catchphrases
- **600+ Lines** of Python code for the complete system
- **2000+ Lines** of HTML/CSS/JavaScript for the interactive gallery

## 📞 Support

If you experience any issues:

1. **Check Dependencies** - Ensure Python 3.8+ and optional modules are installed
2. **Verify File Paths** - All commands should be run from the project root
3. **Test Integration** - Ensure main coyote project modules are accessible
4. **Review Logs** - Check console output for error messages

## 🎉 Conclusion

The ACME Products Complete System brings the classic cartoon experience to life with:
- ✅ **Comprehensive Database** of every ACME product
- ✅ **Interactive Shopping** with personality-driven hosts  
- ✅ **TV/Audio Broadcasting** integrated with existing hardware
- ✅ **YouTube Integration** for episode discovery and download
- ✅ **Seamless Integration** with the coyote project ecosystem

Ready to start shopping? Fire up the demo and experience the ACME difference!

```bash
python acme/demo_complete_system.py
```

---

*"Remember, if it's ACME, it's guaranteed to work... eventually!"* 💥🏺✨
