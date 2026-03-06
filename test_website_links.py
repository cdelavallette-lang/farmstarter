#!/usr/bin/env python3
"""
Website Link Validator for Santa Puala Farm
Tests all links on the website to ensure they're working correctly.
"""

import os
import re
from pathlib import Path
from urllib.parse import urlparse, unquote
import sys

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class LinkValidator:
    def __init__(self, docs_dir):
        self.docs_dir = Path(docs_dir)
        self.errors = []
        self.warnings = []
        self.successes = []
        self.external_links = []
        
    def extract_links(self, html_content, file_path):
        """Extract all href and src links from HTML content"""
        links = []
        
        # Find href links
        href_pattern = r'href=["\']([^"\']+)["\']'
        for match in re.finditer(href_pattern, html_content):
            links.append(('href', match.group(1)))
        
        # Find src links (for images, scripts, etc.)
        src_pattern = r'src=["\']([^"\']+)["\']'
        for match in re.finditer(src_pattern, html_content):
            links.append(('src', match.group(1)))
        
        return links
    
    def is_external_link(self, url):
        """Check if a link is external (http/https)"""
        return url.startswith('http://') or url.startswith('https://')
    
    def is_anchor_link(self, url):
        """Check if link is just an anchor (#)"""
        return url.startswith('#')
    
    def is_special_protocol(self, url):
        """Check if link uses special protocols (mailto, tel, etc.)"""
        special_protocols = ['mailto:', 'tel:', 'javascript:', 'data:']
        return any(url.startswith(proto) for proto in special_protocols)
    
    def resolve_relative_path(self, current_file, link_url):
        """Resolve a relative path from current file"""
        current_dir = current_file.parent
        
        # Remove anchor/fragment
        link_url = link_url.split('#')[0]
        
        # Handle parent directory references
        if link_url.startswith('../'):
            target_path = (current_dir.parent / link_url.replace('../', '')).resolve()
        else:
            target_path = (current_dir / link_url).resolve()
        
        return target_path
    
    def validate_link(self, link_type, link_url, source_file):
        """Validate a single link"""
        # Skip anchor-only links
        if self.is_anchor_link(link_url):
            return
        
        # Skip special protocol links (mailto, tel, etc.)
        if self.is_special_protocol(link_url):
            return
        
        # Track external links
        if self.is_external_link(link_url):
            self.external_links.append({
                'source': source_file.name,
                'url': link_url
            })
            return
        
        # Validate internal link
        try:
            target_path = self.resolve_relative_path(source_file, link_url)
            
            if target_path.exists():
                self.successes.append({
                    'source': source_file.name,
                    'link': link_url,
                    'resolved': str(target_path.relative_to(self.docs_dir.parent))
                })
            else:
                self.errors.append({
                    'source': source_file.name,
                    'link': link_url,
                    'type': link_type,
                    'error': 'File not found',
                    'expected_path': str(target_path)
                })
        except Exception as e:
            self.errors.append({
                'source': source_file.name,
                'link': link_url,
                'type': link_type,
                'error': str(e)
            })
    
    def validate_file(self, file_path):
        """Validate all links in a single HTML file"""
        print(f"{BLUE}Checking {file_path.name}...{RESET}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            links = self.extract_links(content, file_path)
            
            for link_type, link_url in links:
                self.validate_link(link_type, link_url, file_path)
                
        except Exception as e:
            self.errors.append({
                'source': file_path.name,
                'error': f'Failed to read file: {e}'
            })
    
    def run_validation(self):
        """Run validation on all HTML files"""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}Santa Puala Farm - Website Link Validator{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")
        
        # Find all HTML files
        html_files = list(self.docs_dir.glob('*.html'))
        
        if not html_files:
            print(f"{RED}No HTML files found in {self.docs_dir}{RESET}")
            return False
        
        print(f"Found {len(html_files)} HTML files to validate\n")
        
        # Validate each file
        for html_file in html_files:
            self.validate_file(html_file)
        
        # Print results
        self.print_results()
        
        return len(self.errors) == 0
    
    def print_results(self):
        """Print validation results"""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}VALIDATION RESULTS{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")
        
        # Successful links
        print(f"{GREEN}✓ Successful Links: {len(self.successes)}{RESET}")
        if self.successes:
            grouped = {}
            for success in self.successes:
                source = success['source']
                if source not in grouped:
                    grouped[source] = []
                grouped[source].append(success)
            
            for source, links in sorted(grouped.items()):
                print(f"\n  {source}:")
                for link in links:
                    print(f"    ✓ {link['link']} → {link['resolved']}")
        
        # Errors
        if self.errors:
            print(f"\n{RED}✗ Broken Links: {len(self.errors)}{RESET}")
            for error in self.errors:
                print(f"\n  {RED}Error in {error['source']}:{RESET}")
                print(f"    Link: {error['link']}")
                print(f"    Issue: {error['error']}")
                if 'expected_path' in error:
                    print(f"    Expected: {error['expected_path']}")
        else:
            print(f"\n{GREEN}✓ No broken links found!{RESET}")
        
        # External links
        if self.external_links:
            print(f"\n{YELLOW}ℹ External Links (not validated): {len(self.external_links)}{RESET}")
            grouped_external = {}
            for ext in self.external_links:
                source = ext['source']
                if source not in grouped_external:
                    grouped_external[source] = []
                grouped_external[source].append(ext['url'])
            
            for source, urls in sorted(grouped_external.items()):
                print(f"\n  {source}:")
                for url in sorted(set(urls)):
                    print(f"    → {url}")
        
        # Summary
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}SUMMARY{RESET}")
        print(f"{BLUE}{'='*60}{RESET}")
        print(f"  {GREEN}Valid internal links: {len(self.successes)}{RESET}")
        print(f"  {RED}Broken links: {len(self.errors)}{RESET}")
        print(f"  {YELLOW}External links: {len(self.external_links)}{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")

def main():
    """Main entry point"""
    # Get docs directory
    script_dir = Path(__file__).parent
    docs_dir = script_dir / 'docs'
    
    if not docs_dir.exists():
        print(f"{RED}Error: docs directory not found at {docs_dir}{RESET}")
        return 1
    
    # Run validation
    validator = LinkValidator(docs_dir)
    success = validator.run_validation()
    
    # Exit with appropriate code
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
