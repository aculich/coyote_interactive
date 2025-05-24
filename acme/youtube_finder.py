#!/usr/bin/env python3
"""
YouTube Episode Finder
Searches for and downloads classic Looney Tunes episodes featuring ACME products.
"""

import json
import subprocess
import re
import os
from urllib.parse import quote
import requests
import time

class YouTubeEpisodeFinder:
    def __init__(self):
        self.load_products()
        self.youtube_base_url = "https://www.youtube.com"
        self.search_queries = []
        
    def load_products(self):
        """Load ACME products data."""
        try:
            with open('acme/acme_products_clean.json', 'r') as f:
                data = json.load(f)
                self.products = data['products']
                self.series_abbreviations = data['series_abbreviations']
        except FileNotFoundError:
            print("Product data not found.")
            self.products = []
            self.series_abbreviations = {}
    
    def extract_episode_names(self):
        """Extract unique episode names from the products."""
        episodes = set()
        
        for product in self.products:
            episode = product.get('episode', '')
            if episode and episode not in ['LT/MM', 'MM', 'LT']:
                # Clean up episode names
                episode = episode.replace('"', '').strip()
                if episode and len(episode) > 3:
                    episodes.add(episode)
        
        return sorted(list(episodes))
    
    def generate_search_queries(self):
        """Generate YouTube search queries for episodes."""
        episodes = self.extract_episode_names()
        queries = []
        
        # Basic episode searches
        for episode in episodes:
            queries.append(f"Looney Tunes {episode}")
            queries.append(f"Merrie Melodies {episode}")
            queries.append(f"Road Runner {episode}")
            queries.append(f"Wile E Coyote {episode}")
        
        # General searches
        queries.extend([
            "Road Runner Wile E Coyote compilation",
            "ACME products Looney Tunes",
            "Wile E Coyote fails compilation",
            "Road Runner vs Wile E Coyote",
            "Classic Looney Tunes Road Runner",
            "Merrie Melodies Road Runner episodes",
            "Looney Tunes ACME products",
            "Wile E Coyote inventions"
        ])
        
        return queries
    
    def search_youtube_urls(self, query, max_results=5):
        """Search for YouTube URLs using yt-dlp."""
        try:
            # Use yt-dlp to search YouTube
            cmd = [
                'yt-dlp',
                '--get-url',
                '--get-title',
                '--get-duration',
                '--no-download',
                f'ytsearch{max_results}:{query}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                videos = []
                
                # Parse the output (title, duration, url pattern)
                for i in range(0, len(lines), 3):
                    if i + 2 < len(lines):
                        title = lines[i]
                        duration = lines[i + 1]
                        url = lines[i + 2]
                        
                        videos.append({
                            'title': title,
                            'duration': duration,
                            'url': url,
                            'query': query
                        })
                
                return videos
            else:
                print(f"Search failed for '{query}': {result.stderr}")
                return []
                
        except subprocess.TimeoutExpired:
            print(f"Search timeout for '{query}'")
            return []
        except Exception as e:
            print(f"Search error for '{query}': {e}")
            return []
    
    def download_video(self, url, output_dir='acme/episodes'):
        """Download a video using yt-dlp."""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            cmd = [
                'yt-dlp',
                '--output', f'{output_dir}/%(title)s.%(ext)s',
                '--format', 'best[height<=480]',  # Limit quality to save space
                '--write-info-json',
                '--write-description',
                url
            ]
            
            print(f"Downloading: {url}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Successfully downloaded: {url}")
                return True
            else:
                print(f"Download failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Download error: {e}")
            return False
    
    def find_episodes(self, search_limit=3, download=False):
        """Find (and optionally download) episodes."""
        queries = self.generate_search_queries()[:search_limit]
        all_results = []
        
        print(f"🔍 Searching for episodes with {len(queries)} queries...")
        
        for i, query in enumerate(queries):
            print(f"\n[{i+1}/{len(queries)}] Searching: '{query}'")
            
            videos = self.search_youtube_urls(query)
            
            if videos:
                print(f"Found {len(videos)} videos:")
                for j, video in enumerate(videos):
                    print(f"  {j+1}. {video['title']} ({video['duration']})")
                    print(f"     {video['url']}")
                    
                    all_results.append(video)
                    
                    if download:
                        self.download_video(video['url'])
            else:
                print("  No videos found.")
            
            # Be nice to YouTube
            time.sleep(1)
        
        return all_results
    
    def create_episode_database(self, results):
        """Create a database of found episodes."""
        database = {
            'search_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_videos': len(results),
            'episodes': results,
            'products_with_episodes': []
        }
        
        # Match products to episodes
        for product in self.products:
            episode_name = product.get('episode', '').replace('"', '').strip()
            matching_videos = []
            
            for video in results:
                if episode_name.lower() in video['title'].lower():
                    matching_videos.append(video)
            
            if matching_videos:
                database['products_with_episodes'].append({
                    'product': product['product_name'],
                    'episode': episode_name,
                    'usage': product.get('usage', ''),
                    'matching_videos': matching_videos
                })
        
        # Save database
        with open('acme/episode_database.json', 'w') as f:
            json.dump(database, f, indent=2)
        
        print(f"\n📊 Episode database saved with {len(results)} videos")
        print(f"Found {len(database['products_with_episodes'])} products with matching episodes")
        
        return database
    
    def generate_youtube_report(self):
        """Generate a report of YouTube findings."""
        episodes = self.extract_episode_names()
        
        report = f"""# ACME Products YouTube Episode Guide

## Episode Search Report
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Classic Episodes Found
Based on the ACME products database, here are the episodes that feature ACME products:

"""
        
        for episode in episodes:
            # Find products from this episode
            products_in_episode = [p for p in self.products if episode in p.get('episode', '')]
            
            report += f"### {episode}\n"
            report += f"**ACME Products Featured:**\n"
            
            for product in products_in_episode:
                report += f"- {product['product_name']}"
                if 'usage' in product:
                    report += f": {product['usage'][:80]}..."
                report += "\n"
            
            # Add YouTube search suggestions
            report += f"\n**YouTube Search Suggestions:**\n"
            report += f"- `Looney Tunes {episode}`\n"
            report += f"- `Road Runner {episode}`\n"
            report += f"- `Wile E Coyote {episode}`\n\n"
        
        report += """
## Download Commands

To download episodes using yt-dlp:

```bash
# Search and download specific episode
yt-dlp "ytsearch:Looney Tunes Fast and Furry-ous"

# Download with specific format
yt-dlp --format "best[height<=480]" "ytsearch:Road Runner Beep Beep"

# Download compilation videos
yt-dlp "ytsearch:Road Runner Wile E Coyote compilation"
```

## Usage Instructions

1. Install yt-dlp: `pip install yt-dlp`
2. Run the episode finder: `python acme/youtube_finder.py search`
3. Download episodes: `python acme/youtube_finder.py download`

## Legal Note
Please respect YouTube's terms of service and copyright laws when downloading content.
Only download videos for personal use and educational purposes.
"""
        
        with open('acme/YOUTUBE_GUIDE.md', 'w') as f:
            f.write(report)
        
        print("📋 YouTube guide saved to acme/YOUTUBE_GUIDE.md")
        return report
    
    def interactive_search(self):
        """Interactive search mode."""
        print("\n🎬 ACME YouTube Episode Finder")
        print("==============================")
        
        episodes = self.extract_episode_names()
        
        print(f"\nFound {len(episodes)} unique episodes from ACME products:")
        for i, episode in enumerate(episodes[:10]):
            print(f"  {i+1}. {episode}")
        if len(episodes) > 10:
            print(f"  ... and {len(episodes) - 10} more!")
        
        print("\nCommands:")
        print("  'search' - Search for all episodes")
        print("  'search <query>' - Search for specific episode")
        print("  'download <url>' - Download specific video")
        print("  'list' - List all episodes")
        print("  'report' - Generate YouTube guide")
        print("  'quit' - Exit")
        
        while True:
            try:
                command = input("\n🎥 YouTube Command: ").strip()
                
                if command.lower() in ['quit', 'q', 'exit']:
                    break
                elif command.lower() == 'search':
                    results = self.find_episodes(search_limit=5)
                    self.create_episode_database(results)
                elif command.lower().startswith('search '):
                    query = command[7:]
                    videos = self.search_youtube_urls(query)
                    for video in videos:
                        print(f"🎥 {video['title']} ({video['duration']})")
                        print(f"   {video['url']}")
                elif command.lower().startswith('download '):
                    url = command[9:]
                    self.download_video(url)
                elif command.lower() == 'list':
                    print(f"\n📋 All Episodes ({len(episodes)}):")
                    for episode in episodes:
                        print(f"  • {episode}")
                elif command.lower() == 'report':
                    self.generate_youtube_report()
                else:
                    print("Unknown command.")
                    
            except KeyboardInterrupt:
                break

def main():
    """Main function."""
    import sys
    
    finder = YouTubeEpisodeFinder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'search':
            results = finder.find_episodes(search_limit=10)
            finder.create_episode_database(results)
            
        elif command == 'download':
            results = finder.find_episodes(search_limit=5, download=True)
            finder.create_episode_database(results)
            
        elif command == 'report':
            finder.generate_youtube_report()
            
        elif command == 'episodes':
            episodes = finder.extract_episode_names()
            print(f"Found {len(episodes)} episodes:")
            for episode in episodes:
                print(f"  • {episode}")
                
        else:
            print(f"Unknown command: {command}")
            print("Usage: python youtube_finder.py [search|download|report|episodes]")
    else:
        finder.interactive_search()

if __name__ == "__main__":
    main() 