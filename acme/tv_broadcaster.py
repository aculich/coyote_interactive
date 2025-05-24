#!/usr/bin/env python3
"""
ACME TV Broadcasting System
Broadcasts ACME product demonstrations to TV and audio systems.
Integrates with existing coyote project infrastructure.
"""

import json
import random
import time
import subprocess
import threading
from pathlib import Path
import sys
import os

# Add the parent directory to the path to import from the main project
sys.path.append(str(Path(__file__).parent.parent))

try:
    from speak_text import speak_text
    from comment_on_television import comment_on_television
    from config import Config
except ImportError as e:
    print(f"Warning: Could not import project modules: {e}")
    print("Running in standalone mode.")

class ACMEBroadcaster:
    def __init__(self):
        self.hosts = {
            'bob': {
                'name': 'Bob "Boom" Richardson',
                'specialty': 'Explosives Expert',
                'voice_style': 'deep and authoritative',
                'catchphrases': [
                    "That's explosive value!",
                    "Guaranteed to make a big impression!",
                    "Now that's what I call a blast!",
                    "BOOM! Another satisfied customer!"
                ]
            },
            'sally': {
                'name': 'Sally Speedster',
                'specialty': 'Velocity Specialist',
                'voice_style': 'energetic and fast-paced',
                'catchphrases': [
                    "Faster than a speeding roadrunner!",
                    "Zoom zoom! Look at that speed!",
                    "Beep beep! That's a great deal!",
                    "Quick! Don't let this deal get away!"
                ]
            },
            'chuck': {
                'name': 'Chuck Contraption',
                'specialty': 'Gadget Guru',
                'voice_style': 'intellectual and excited',
                'catchphrases': [
                    "The engineering is simply marvelous!",
                    "Such ingenious design!",
                    "A masterpiece of cartoon physics!",
                    "Even Wile E. Coyote would be impressed!"
                ]
            },
            'betty': {
                'name': 'Betty Bargain',
                'specialty': 'Deal Detective',
                'voice_style': 'friendly and persuasive',
                'catchphrases': [
                    "What a steal!",
                    "You won't find prices like these anywhere else!",
                    "This deal is too good to pass up!",
                    "Your wallet will thank you!"
                ]
            }
        }
        
        self.current_host = 'bob'
        self.load_products()
        self.is_broadcasting = False
        
    def load_products(self):
        """Load ACME products from the clean JSON file."""
        try:
            with open('acme/acme_products_clean.json', 'r') as f:
                data = json.load(f)
                self.products = data['products']
                self.series_abbreviations = data['series_abbreviations']
        except FileNotFoundError:
            print("Product data not found. Using sample data.")
            self.products = self._get_sample_products()
            self.series_abbreviations = {
                'LT': 'Looney Tunes',
                'MM': 'Merrie Melodies'
            }
    
    def _get_sample_products(self):
        """Get sample products if the main data file isn't available."""
        return [
            {
                'product_name': 'Anvil',
                'episode': 'LT/MM',
                'usage': 'Classic gravity-powered percussive device',
                'series': 'Various'
            },
            {
                'product_name': 'TNT',
                'episode': 'Multiple episodes',
                'usage': 'Classic explosive for all your demolition needs',
                'series': 'Various'
            },
            {
                'product_name': 'Rocket-Powered Roller Skates',
                'episode': 'Beep, Beep',
                'usage': 'Let you skate at unlimited speed',
                'series': 'MM'
            }
        ]
    
    def generate_product_pitch(self, product, host_key=None):
        """Generate a sales pitch for a product."""
        if not host_key:
            host_key = self.current_host
            
        host = self.hosts[host_key]
        
        # Generate price (for demonstration)
        base_price = random.randint(50, 1000)
        sale_price = base_price * 0.7  # 30% off
        
        pitch_templates = [
            f"Ladies and gentlemen, {host['name']} here with an AMAZING deal on the {product['product_name']}! {product.get('usage', 'Perfect for all your cartoon needs!')}",
            
            f"Don't blink or you'll miss this incredible offer! The {product['product_name']} - as seen in {product.get('episode', 'classic cartoons')}!",
            
            f"I've personally tested this {product['product_name']} and let me tell you - {random.choice(host['catchphrases'])}",
            
            f"For the next 10 minutes only, we're offering the {product['product_name']} at the unbelievable price of just ${sale_price:.2f}! That's down from ${base_price:.2f}!"
        ]
        
        main_pitch = random.choice(pitch_templates)
        
        # Add usage information
        if 'usage' in product and product['usage']:
            main_pitch += f" {product['usage']}"
        
        # Add episode reference
        if 'episode' in product:
            main_pitch += f" You remember this from {product['episode']}!"
        
        # Add catchphrase
        main_pitch += f" {random.choice(host['catchphrases'])}"
        
        # Add urgency
        urgency_phrases = [
            "Call now! Lines are standing by!",
            "But wait, there's more! Order in the next 5 minutes and get FREE shipping!",
            "Don't let this deal run away like the Road Runner!",
            "This offer won't last long - just like Wile E. Coyote's schemes!"
        ]
        
        main_pitch += f" {random.choice(urgency_phrases)}"
        
        return main_pitch
    
    def speak_pitch(self, pitch_text):
        """Speak the pitch using the project's text-to-speech system."""
        try:
            # Try to use the project's speak_text function
            speak_text(pitch_text)
        except Exception as e:
            print(f"Could not use project TTS: {e}")
            # Fallback to system TTS if available
            try:
                subprocess.run(['say', pitch_text], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"TTS not available. Pitch: {pitch_text}")
    
    def display_on_tv(self, product, host_info):
        """Display product information on TV using the project's TV system."""
        try:
            # Try to use the project's TV comment system
            tv_message = f"🏺 ACME PRODUCT SHOWCASE 🏺\n\n"
            tv_message += f"Host: {host_info['name']}\n"
            tv_message += f"Product: {product['product_name']}\n\n"
            tv_message += f"Featured in: {product.get('episode', 'Various episodes')}\n\n"
            tv_message += f"Description: {product.get('usage', 'Premium ACME quality!')}\n\n"
            tv_message += f"💥 {random.choice(host_info['catchphrases'])} 💥"
            
            comment_on_television(tv_message)
        except Exception as e:
            print(f"Could not use project TV system: {e}")
            print(f"TV Display: {product['product_name']} - {host_info['name']}")
    
    def broadcast_product(self, product=None, host_key=None):
        """Broadcast a single product demonstration."""
        if not product:
            product = random.choice(self.products)
        
        if not host_key:
            host_key = self.current_host
        
        host_info = self.hosts[host_key]
        
        print(f"\n🎬 Broadcasting: {product['product_name']} with {host_info['name']}")
        
        # Generate and speak the pitch
        pitch = self.generate_product_pitch(product, host_key)
        print(f"Pitch: {pitch}")
        
        # Display on TV
        self.display_on_tv(product, host_info)
        
        # Speak the pitch
        self.speak_pitch(pitch)
        
        return pitch
    
    def start_continuous_broadcast(self, interval=30):
        """Start continuous broadcasting of ACME products."""
        self.is_broadcasting = True
        
        def broadcast_loop():
            while self.is_broadcasting:
                try:
                    # Randomly switch hosts occasionally
                    if random.random() < 0.3:  # 30% chance to switch hosts
                        self.current_host = random.choice(list(self.hosts.keys()))
                    
                    # Broadcast a random product
                    self.broadcast_product()
                    
                    # Wait for the interval
                    time.sleep(interval)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Broadcast error: {e}")
                    time.sleep(5)  # Wait a bit before retrying
        
        # Start broadcasting in a separate thread
        self.broadcast_thread = threading.Thread(target=broadcast_loop)
        self.broadcast_thread.daemon = True
        self.broadcast_thread.start()
        
        print(f"🎯 Started ACME TV Broadcasting! Broadcasting every {interval} seconds.")
        print("Press Ctrl+C to stop.")
    
    def stop_broadcast(self):
        """Stop the continuous broadcast."""
        self.is_broadcasting = False
        print("🔇 ACME TV Broadcasting stopped.")
    
    def broadcast_special_show(self, duration_minutes=5):
        """Broadcast a special ACME shopping show."""
        print(f"🎪 Starting Special ACME Shopping Show! Duration: {duration_minutes} minutes")
        
        end_time = time.time() + (duration_minutes * 60)
        show_products = random.sample(self.products, min(10, len(self.products)))
        
        # Opening announcement
        opening = f"Welcome to the ACME Shopping Network Special! I'm {self.hosts[self.current_host]['name']}, and for the next {duration_minutes} minutes, we have INCREDIBLE deals on genuine ACME products! Let's get started!"
        
        print(f"Opening: {opening}")
        self.speak_pitch(opening)
        
        # Show products with shorter intervals
        product_index = 0
        while time.time() < end_time and product_index < len(show_products):
            product = show_products[product_index]
            
            # Add special show flair
            special_intro = f"Next up in our special show - the amazing {product['product_name']}!"
            print(f"Special intro: {special_intro}")
            self.speak_pitch(special_intro)
            
            # Brief pause
            time.sleep(2)
            
            # Main product pitch
            self.broadcast_product(product)
            
            product_index += 1
            
            # Wait before next product (shorter interval for special show)
            time.sleep(15)
        
        # Closing
        closing = "That concludes our ACME Shopping Network Special! Remember, if it's ACME, it's guaranteed to work... eventually! Thank you for shopping with us!"
        print(f"Closing: {closing}")
        self.speak_pitch(closing)
    
    def interactive_mode(self):
        """Interactive mode for manual broadcasting control."""
        print("\n🎮 ACME Broadcasting Interactive Mode")
        print("Commands:")
        print("  'broadcast' or 'b' - Broadcast random product")
        print("  'show <minutes>' - Special show for X minutes")
        print("  'host <name>' - Switch host (bob, sally, chuck, betty)")
        print("  'list' - List all products")
        print("  'continuous' or 'c' - Start continuous broadcasting")
        print("  'stop' - Stop continuous broadcasting")
        print("  'quit' or 'q' - Exit")
        
        while True:
            try:
                command = input("\n🎬 ACME Command: ").strip().lower()
                
                if command in ['quit', 'q', 'exit']:
                    self.stop_broadcast()
                    break
                elif command in ['broadcast', 'b']:
                    self.broadcast_product()
                elif command.startswith('show '):
                    try:
                        minutes = int(command.split()[1])
                        self.broadcast_special_show(minutes)
                    except (IndexError, ValueError):
                        print("Usage: show <minutes>")
                elif command.startswith('host '):
                    try:
                        host_name = command.split()[1]
                        if host_name in self.hosts:
                            self.current_host = host_name
                            print(f"Switched to {self.hosts[host_name]['name']}")
                        else:
                            print(f"Unknown host. Available: {', '.join(self.hosts.keys())}")
                    except IndexError:
                        print("Usage: host <name>")
                elif command == 'list':
                    print(f"\n📋 Available Products ({len(self.products)}):")
                    for i, product in enumerate(self.products[:10]):  # Show first 10
                        print(f"  {i+1}. {product['product_name']}")
                    if len(self.products) > 10:
                        print(f"  ... and {len(self.products) - 10} more!")
                elif command in ['continuous', 'c']:
                    interval = input("Broadcast interval in seconds (default 30): ").strip()
                    try:
                        interval = int(interval) if interval else 30
                    except ValueError:
                        interval = 30
                    self.start_continuous_broadcast(interval)
                elif command == 'stop':
                    self.stop_broadcast()
                else:
                    print("Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                self.stop_broadcast()
                break

def main():
    """Main function to run the ACME broadcaster."""
    print("🏺 ACME TV Broadcasting System 🏺")
    print("================================")
    
    broadcaster = ACMEBroadcaster()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'demo':
            # Demo mode - broadcast a few products
            print("🎯 Demo Mode: Broadcasting 3 products...")
            for i in range(3):
                broadcaster.broadcast_product()
                if i < 2:  # Don't wait after the last one
                    time.sleep(10)
                    
        elif command == 'continuous':
            # Continuous mode
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            broadcaster.start_continuous_broadcast(interval)
            try:
                while broadcaster.is_broadcasting:
                    time.sleep(1)
            except KeyboardInterrupt:
                broadcaster.stop_broadcast()
                
        elif command == 'show':
            # Special show mode
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            broadcaster.broadcast_special_show(duration)
            
        else:
            print(f"Unknown command: {command}")
            print("Usage: python tv_broadcaster.py [demo|continuous|show] [options]")
    else:
        # Interactive mode
        broadcaster.interactive_mode()

if __name__ == "__main__":
    main() 