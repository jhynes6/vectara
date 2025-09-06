#!/usr/bin/env python3
"""
Client Website Content Scraper

This script crawls a client's website using their sitemap and saves each page
as a markdown file in a "website" folder with rich metadata.

Usage:
    python ingest_client_website.py --url https://example.com --client-name "Client Corp"

Required:
    --url: The client's website URL (will look for sitemap.xml)

Optional:
    --workers: Number of parallel workers for faster processing (default: 4)
    --output-dir: Output directory for website folder and logs (default: ingestion/client_ingestion_outputs)
    --no-llm-categories: Disable LLM categorization (LLM is enabled by default)
    --client-name: Client name to add to metadata
    --project-name: Project name to add to metadata
"""

import os
import sys
import argparse
import logging
import re
import time
import json
import psutil
import requests
import asyncio
from pathlib import Path
from urllib.parse import urlparse, urljoin
from dotenv import load_dotenv
from xml.etree import ElementTree
from typing import List, Set, Optional, Dict
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from openai import AsyncOpenAI

load_dotenv()

# Bright Data Configuration
BRIGHTDATA_API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")

print(BRIGHTDATA_API_TOKEN)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_urls_from_sitemap(sitemap_url: str, processed_sitemaps: Optional[Set[str]] = None) -> List[str]:
    """
    Recursively fetches URLs from sitemap, handling both sitemap indexes and regular sitemaps.
    """
    if processed_sitemaps is None:
        processed_sitemaps = set()

    if sitemap_url in processed_sitemaps:
        return []

    processed_sitemaps.add(sitemap_url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
        response = requests.get(sitemap_url, headers=headers, timeout=30)
        response.raise_for_status()

        # Parse the XML
        root = ElementTree.fromstring(response.content)

        # Try different possible namespaces
        namespaces = [
            {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'},
            {},  # No namespace
        ]

        urls = []
        for ns in namespaces:
            # Try to find sitemap locations
            locations = root.findall('.//ns:loc', ns) if ns else root.findall('.//loc')

            for loc in locations:
                if loc.text is None:
                    continue
                url = loc.text.strip()
                if any(url.endswith(ext) for ext in ['.xml', 'sitemap.xml', 'sitemap_index.xml']):
                    # This is a sitemap index
                    logger.info(f"📋 Found nested sitemap: {url}")
                    child_urls = get_urls_from_sitemap(url, processed_sitemaps)
                    urls.extend(child_urls)
                else:
                    urls.append(url)

            if urls:  # If we found URLs with this namespace, stop trying others
                break

        return list(set(urls))  # Remove duplicates

    except Exception as e:
        logger.warning(f"Error processing sitemap {sitemap_url}: {str(e)}")
        return []

def discover_sitemaps(base_url: str) -> List[str]:
    """Discover sitemap URLs from common locations"""
    sitemap_candidates = [
        urljoin(base_url, '/sitemap.xml'),
        urljoin(base_url, '/sitemap_index.xml'),
        urljoin(base_url, '/wp-sitemap.xml'),
        urljoin(base_url, '/sitemap.xml.gz'),
    ]
    
    # Also check robots.txt
    try:
        robots_url = urljoin(base_url, '/robots.txt')
        response = requests.get(robots_url, timeout=15)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                if line.strip().lower().startswith('sitemap:'):
                    sitemap_url = line.split(':', 1)[1].strip()
                    sitemap_candidates.append(sitemap_url)
    except:
        pass
    
    return sitemap_candidates

def clean_markdown_content(markdown_content: str) -> str:
    """
    Clean markdown content by removing navigation, headers, footers, and other boilerplate.
    """
    lines = markdown_content.split('\n')
    
    # First pass: Remove everything before the main content starts
    main_content_start = -1
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Look for company/client name headers that indicate main content
        if re.match(r'^##?\s+[A-Z][A-Z\s]+$', line):  # Headers like "## TRIOSE" or "## IEEE EMBS"
            main_content_start = i
            break
        # Or look for substantial content paragraphs (not navigation)
        elif (line and len(line) > 50 and 
              not line.startswith('*') and 
              not line.startswith('[') and 
              not 'Skip to content' in line and
              not 'logo' in line.lower()):
            main_content_start = i
            break
    
    # If no clear main content found, look for the first substantial paragraph
    if main_content_start == -1:
        for i, line in enumerate(lines):
            line = line.strip()
            if (line and len(line) > 30 and 
                not line.startswith('*') and 
                not line.startswith('[') and
                '(' not in line and
                not line.startswith('#')):
                main_content_start = i
                break
    
    # Second pass: Remove everything after footer content starts
    main_content_end = len(lines)
    footer_patterns = [
        r'^\[See More Case Studies\]',
        r'^## Let\'s Connect$',
        r'^\*\*New Business\*\*',
        r'^## Send Us a Note$',
        r'^Mike DeFabrizio',
        r'^\*\*Careers at D2',
        r'^\*\*Insights\*\*',
    ]
    
    for i in range(main_content_start, len(lines)):
        line = lines[i].strip()
        for pattern in footer_patterns:
            if re.match(pattern, line):
                main_content_end = i
                break
        if main_content_end != len(lines):
            break
    
    # Extract the main content section
    if main_content_start >= 0:
        content_lines = lines[main_content_start:main_content_end]
    else:
        content_lines = lines
    
    # Third pass: Clean up remaining navigation and boilerplate within content
    cleaned_lines = []
    skip_next_empty = False
    
    for line in content_lines:
        line = line.strip()
        
        # Skip navigation bullets
        if line.startswith('*') and '](' in line:
            skip_next_empty = True
            continue
        
        # Skip logo links and images in navigation
        if '[Skip to content]' in line or 'logo' in line.lower():
            continue
        
        # Skip empty lines after removed navigation
        if not line and skip_next_empty:
            skip_next_empty = False
            continue
        
        skip_next_empty = False
        cleaned_lines.append(line)
    
    # Join and clean up excessive whitespace
    cleaned_content = '\n'.join(cleaned_lines)
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content).strip()
    
    return cleaned_content

def crawl_single_url(url: str) -> dict:
    """
    Crawl a single URL using the Bright Data Scraping Browser API and return the content.
    """
    if not BRIGHTDATA_API_TOKEN:
        logger.error("❌ BRIGHTDATA_API_TOKEN not found in environment variables. Cannot scrape.")
        return {
            'url': url, 'title': '', 'content': "Error: BRIGHTDATA_API_TOKEN not set.",
            'success': False, 'word_count': 0, 'extraction_method': 'brightdata_error'
        }

    api_url = "https://api.brightdata.com/request?async=true"
    payload = json.dumps({
      "zone": "web_unlocker1",
      "url": url,
      "format": "raw",
      "method": "GET",
      "country": "US",
      "data_format": "markdown"
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': f'Bearer {BRIGHTDATA_API_TOKEN}'
    }

    try:
        response = requests.request("POST", api_url, headers=headers, data=payload, timeout=120)
        response.raise_for_status()
        
        # Check for Bright Data response headers that might indicate a scraping failure
        if 'x-response-code' in response.headers and response.headers['x-response-code'] != '200':
             logger.error(f"❌ Bright Data failed to load {url}. Status: {response.headers.get('x-response-code')}, Body: {response.text[:200]}")
             return {
                'url': url, 'title': '', 'content': f"Error from Bright Data. Status: {response.headers.get('x-response-code')}",
                'success': False, 'word_count': 0, 'extraction_method': 'brightdata_failed_load'
            }

        markdown_content = response.text

        # Clean the markdown content to remove navigation, headers, and footers
        cleaned_content = clean_markdown_content(markdown_content)

        # Extract title from the first H1 tag in the cleaned markdown, fallback to URL path
        title_match = re.search(r'^#\s+(.*)', cleaned_content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else urlparse(url).path

        return {
            'url': url,
            'title': title,
            'content': cleaned_content,
            'success': True,
            'word_count': len(cleaned_content.split()),
            'extraction_method': 'brightdata_api'
        }

    except requests.RequestException as e:
        logger.error(f"❌ Error during Bright Data API call for {url}: {e}")
        return {
            'url': url, 'title': '', 'content': f"Error calling Bright Data API: {str(e)}",
            'success': False, 'word_count': 0, 'extraction_method': 'brightdata_request_error'
        }

def safe_filename(url: str) -> str:
    """
    Convert a URL into a filesystem-safe markdown filename.
    """
    try:
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        if not path:
            name = 'index'
        else:
            name = path.replace('/', '_')
        # Remove query and fragment markers
        name = name.replace('?', '_').replace('&', '_').replace('=', '_').replace('#', '_')
        # Trim overly long names
        if len(name) > 180:
            name = name[:180]
        return f"{name}.md"
    except Exception:
        return "page.md"

# LLM-based URL categorization system
CATEGORIZATION_SYSTEM_PROMPT = """
You are helping categorize website URLs based on the type of content likely to be on each page.

Categories and definitions:
- homepage: the company's home page
- services_products: pages that detail the company's services or products they are selling
- industry_markets: pages that detail the industries or markets the company serves
- pricing: pages that give information on pricing
- case_studies: pages with case studies detailing success stories
- testimonials: pages exclusively for client testimonials
- blogs_resources: blogs, resources, guides, and other thought leadership content
- about: pages with more information about the company
- careers: career / hiring related pages
- other: use this if you cannot confidently assign the URL to one of the provided categories

Your output should contain only the category name with no other text.
"""

VALID_CATEGORIES = [
    'homepage', 'services_products', 'industry_markets', 'pricing', 
    'case_studies', 'testimonials', 'blogs_resources', 'about', 'careers', 'other'
]

async def categorize_single_url_with_llm(url: str, client: AsyncOpenAI) -> tuple[str, str]:
    """Categorize a single URL using LLM"""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": CATEGORIZATION_SYSTEM_PROMPT},
                {"role": "user", "content": f"categorize the url: {url}"}
            ],
            temperature=0.1,  # Lower temperature for more consistent categorization
            max_tokens=20,
            top_p=1
        )
        
        category = response.choices[0].message.content.strip().lower()
        
        if category not in VALID_CATEGORIES:
            logger.warning(f"⚠️  Invalid category '{category}' for {url}, defaulting to 'other'")
            category = 'other'
            
        return url, category
        
    except Exception as e:
        logger.error(f"❌ Error categorizing {url}: {e}")
        return url, 'other'

async def categorize_urls_with_llm(urls: List[str]) -> Dict[str, str]:
    """Categorize multiple URLs using LLM in parallel"""
    try:
        # Load OpenAI API key
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("❌ OPENAI_API_KEY not found in environment")
            logger.warning("⚠️  Falling back to simple regex-based categorization")
            return {url: categorize_url_simple(url) for url in urls}
        
        client = AsyncOpenAI(api_key=api_key)
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize OpenAI client: {e}")
        logger.warning("⚠️  Falling back to simple regex-based categorization")
        return {url: categorize_url_simple(url) for url in urls}
    
    logger.info(f"🤖 Categorizing {len(urls)} URLs using LLM...")
    
    # Process in batches to avoid rate limits
    batch_size = 10
    results = {}
    
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(urls) + batch_size - 1) // batch_size
        
        logger.info(f"🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} URLs)")
        
        tasks = [categorize_single_url_with_llm(url, client) for url in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in batch_results:
            if isinstance(result, Exception):
                logger.error(f"❌ Batch error: {result}")
            else:
                url, category = result
                results[url] = category
        
        # Rate limiting between batches
        if i + batch_size < len(urls):
            await asyncio.sleep(1)
    
    logger.info(f"✅ LLM categorization complete")
    return results

def categorize_url_simple(url: str) -> str:
    """Simple regex-based categorization as fallback"""
    path = urlparse(url).path.lower()
    
    # Check for homepage
    if path in ['', '/']:
        return 'homepage'
    
    # Simple pattern matching
    if any(keyword in path for keyword in ['/blog', '/news', '/article', '/post', '/resource', '/guide']):
        return 'blogs_resources'
    elif any(keyword in path for keyword in ['/case-study', '/case-studies', '/portfolio']):
        return 'case_studies'
    elif any(keyword in path for keyword in ['/product', '/service', '/solution']):
        return 'services_products'
    elif any(keyword in path for keyword in ['/about', '/company', '/team']):
        return 'about'
    elif any(keyword in path for keyword in ['/pricing', '/plans', '/price']):
        return 'pricing'
    elif any(keyword in path for keyword in ['/career', '/job', '/hiring', '/recruit']):
        return 'careers'
    elif any(keyword in path for keyword in ['/testimonial', '/review', '/client']):
        return 'testimonials'
    elif any(keyword in path for keyword in ['/industry', '/market', '/sector']):
        return 'industry_markets'
    else:
        return 'other'

def crawl_parallel(urls: List[str], custom_metadata: dict, output_dir: str, max_workers: int = 4, url_categories: Dict[str, str] = None) -> dict:
    """Crawl URLs in parallel and save as markdown files with LLM-based categorization"""
    
    logger.info(f"🚀 Processing {len(urls)} URLs with {max_workers} workers")
    
    results = {
        'successful': 0,
        'failed': 0,
        'urls_processed': [],
        'total_words': 0,
        'categories': {}
    }
    
    website_dir = os.path.join(output_dir, 'website')
    os.makedirs(website_dir, exist_ok=True)
    
    def process_single_url(url_data):
        """Process a single URL and save as markdown"""
        url, idx = url_data
        if idx % 10 == 0:
            logger.info(f"📊 Processing URL {idx+1}/{len(urls)}: {urlparse(url).path}")
        
        # Scrape content
        scrape_result = crawl_single_url(url)
        
        if scrape_result['success']:
            # Get LLM-based category or fallback to simple categorization
            content_type = url_categories.get(url, categorize_url_simple(url)) if url_categories else categorize_url_simple(url)
            
            # Create comprehensive metadata
            parsed_url = urlparse(url)
            metadata = {
                'source': 'website',  # Always 'website' for scraped pages
                'content_type': content_type,  # LLM-categorized content type
                'url': url,
                'title': scrape_result['title'],
                'domain': parsed_url.netloc,
                'path': parsed_url.path,
                'scraped_time': datetime.now().isoformat(),
                'url_depth': len([p for p in parsed_url.path.split('/') if p]),
                'word_count': scrape_result['word_count'],
                **custom_metadata
            }
            
            # Save as markdown with frontmatter
            filename = safe_filename(url)
            filepath = os.path.join(website_dir, filename)
            
            # Create markdown content with frontmatter
            frontmatter = "---\n"
            for key, value in metadata.items():
                if isinstance(value, str):
                    # Escape quotes and clean value for YAML frontmatter
                    clean_value = value.replace('"', '\\"').replace('\n', ' ').replace('\r', ' ')
                    frontmatter += f"{key}: \"{clean_value}\"\n"
                else:
                    frontmatter += f"{key}: {value}\n"
            frontmatter += "---\n\n"
            
            markdown_content = frontmatter
            if scrape_result['title']:
                markdown_content += f"# {scrape_result['title']}\n\n"
            
            markdown_content += scrape_result['content']
            
            # Save file
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                return {
                    'url': url,
                    'success': True,
                    'words': scrape_result['word_count'],
                    'category': content_type,
                    'filename': filename
                }
            except Exception as e:
                logger.error(f"❌ Failed to save {filename}: {e}")
        
        return {'url': url, 'success': False, 'words': 0, 'category': 'failed'}
    
    # Process with thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        url_data = [(url, idx) for idx, url in enumerate(urls)]
        futures = [executor.submit(process_single_url, data) for data in url_data]
        
        completed = 0
        for future in as_completed(futures):
            try:
                result = future.result()
                completed += 1
                
                if result['success']:
                    results['successful'] += 1
                    results['urls_processed'].append(result['url'])
                    results['total_words'] += result['words']
                    
                    # Track categories
                    category = result['category']
                    results['categories'][category] = results['categories'].get(category, 0) + 1
                    
                    logger.info(f"💾 Saved: {result['filename']} ({result['words']} words) [{category}]")
                else:
                    results['failed'] += 1
                
                if completed % 10 == 0:
                    progress = completed / len(urls) * 100
                    logger.info(f"📈 Progress: {progress:.1f}% ({completed}/{len(urls)})")
                    
            except Exception as e:
                logger.error(f"❌ Thread error: {e}")
                results['failed'] += 1
                completed += 1
    
    return results

def save_scraping_summary(urls: List[str], results: dict, output_dir: str, custom_metadata: dict):
    """Save comprehensive scraping summary"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save all discovered URLs
    urls_file = os.path.join(output_dir, 'urls_discovered.txt')
    with open(urls_file, 'w', encoding='utf-8') as f:
        for url in sorted(urls):
            f.write(url + '\n')
    
    # Save successful URLs
    success_file = os.path.join(output_dir, 'urls_successful.txt')
    with open(success_file, 'w', encoding='utf-8') as f:
        for url in sorted(results['urls_processed']):
            f.write(url + '\n')
    
    # Save comprehensive summary
    summary = {
        'scraping_summary': {
            'total_urls_discovered': len(urls),
            'successful_scrapes': results['successful'],
            'failed_scrapes': results['failed'],
            'success_rate': f"{(results['successful'] / len(urls) * 100):.1f}%" if urls else "0%",
            'total_words_scraped': results['total_words'],
            'categories': results['categories'],
            'custom_metadata_applied': custom_metadata,
            'scrape_time': datetime.now().isoformat()
        }
    }
    
    summary_file = os.path.join(output_dir, 'scraping_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"💾 Summary saved to {summary_file}")

async def main_async():
    """Async main function to handle LLM categorization"""
    parser = argparse.ArgumentParser(
        description='Scrape client website content and save as markdown files with LLM categorization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Required arguments
    parser.add_argument('--url', '-u', required=True,
                       help='Client website URL (will look for sitemap.xml)')
    
    # Optional arguments
    parser.add_argument('--workers', '-w', type=int, default=4,
                       help='Number of parallel workers for faster processing (default: 4)')
    parser.add_argument('--output-dir', '-o', default='ingestion/client_ingestion_outputs',
                       help='Output directory for website folder and logs (default: ingestion/client_ingestion_outputs)')
    parser.add_argument('--no-llm-categories', action='store_true',
                       help='Disable LLM categorization and use simple keyword-based categorization instead')
    
    # Metadata arguments
    parser.add_argument('--client-name', default='',
                       help='Client name to add to metadata')
    parser.add_argument('--project-name', default='',
                       help='Project name to add to metadata')
    parser.add_argument('--metadata', action='append',
                       help='Custom metadata in key=value format (can be used multiple times)')
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    # Parse custom metadata
    custom_metadata = {}
    
    if args.client_name:
        custom_metadata['client_name'] = args.client_name
    if args.project_name:
        custom_metadata['project_name'] = args.project_name
        
    if args.metadata:
        for meta_arg in args.metadata:
            if '=' in meta_arg:
                key, value = meta_arg.split('=', 1)
                custom_metadata[key.strip()] = value.strip()
            else:
                logger.warning(f"Invalid metadata format: {meta_arg}. Use key=value format.")
    
    logger.info(f"🌐 Starting website scraping: {args.url}")
    logger.info(f"⚡ Workers: {args.workers}")
    logger.info(f"📁 Output: {args.output_dir}/website/")
    use_llm_categories = not args.no_llm_categories
    logger.info(f"🤖 LLM Categorization: {'Enabled' if use_llm_categories else 'Disabled (--no-llm-categories flag used)'}")
    
    if custom_metadata:
        logger.info(f"🏷️  Custom metadata: {custom_metadata}")
    
    try:
        start_time = time.time()
        
        # Step 1: Discover sitemaps and extract URLs
        logger.info("🔍 Discovering URLs from sitemap...")
        
        sitemap_candidates = discover_sitemaps(args.url)
        all_urls = []
        
        for sitemap_url in sitemap_candidates:
            logger.info(f"📋 Checking sitemap: {sitemap_url}")
            urls = get_urls_from_sitemap(sitemap_url)
            if urls:
                all_urls.extend(urls)
                logger.info(f"✅ Found {len(urls)} URLs in {sitemap_url}")
        
        # Remove duplicates and fallback if no URLs found
        all_urls = list(set(all_urls))
        if not all_urls:
            all_urls = [args.url]
            logger.info(f"⚠️  No sitemap URLs found, using base URL only")
        
        logger.info(f"📊 Total unique URLs to process: {len(all_urls)}")
        
        # Save discovered URLs for reference
        os.makedirs(args.output_dir, exist_ok=True)
        urls_file = os.path.join(args.output_dir, 'urls_discovered.txt')
        with open(urls_file, 'w', encoding='utf-8') as f:
            for url in sorted(all_urls):
                f.write(url + '\n')
        
        # Step 2: Categorize URLs with LLM by default
        url_categories = {}
        if use_llm_categories:
            url_categories = await categorize_urls_with_llm(all_urls)
            
            # Save categorization results
            categories_file = os.path.join(args.output_dir, 'url_categories.json')
            with open(categories_file, 'w', encoding='utf-8') as f:
                json.dump(url_categories, f, indent=2, ensure_ascii=False)
            logger.info(f"🏷️  URL categories saved to: {categories_file}")
        
        # Step 3: Crawl URLs in parallel
        results = crawl_parallel(all_urls, custom_metadata, args.output_dir, args.workers, url_categories)
        
        # Step 4: Save summary
        save_scraping_summary(all_urls, results, args.output_dir, custom_metadata)
        
        # Final summary
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"\n🎉 WEBSITE SCRAPING COMPLETE!")
        logger.info(f"⏱️  Total time: {duration:.2f} seconds")
        logger.info(f"📊 URLs discovered: {len(all_urls)}")
        logger.info(f"✅ Successfully scraped: {results['successful']}")
        logger.info(f"❌ Failed: {results['failed']}")
        logger.info(f"📝 Total words scraped: {results['total_words']:,}")
        
        if duration > 0:
            logger.info(f"🚀 Scraping speed: {results['successful']/duration:.1f} URLs/second")
        
        logger.info(f"📂 Content saved to: {args.output_dir}/website/")
        logger.info(f"📂 Content categories:")
        for category, count in results['categories'].items():
            logger.info(f"   {category}: {count} pages")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("🛑 Scraping interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Error during website scraping: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return 1

def main():
    """Wrapper to run async main function"""
    return asyncio.run(main_async())

if __name__ == "__main__":
    sys.exit(main())
