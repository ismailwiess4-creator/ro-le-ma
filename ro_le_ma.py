#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RO-LE-MA: The Open Source Language of Things
Convert anything into readable 3-letter codes

EIF-TOW = Eiffel Tower
LIB-STA = Liberty Statute
COC-COL-CAN = Coca-Cola Can

MIT License - Free for everyone, built by everyone
"""

import re
import json
import csv
from datetime import datetime
from typing import List, Dict, Optional
import pyperclip
import sys
import os

__version__ = "0.1.0"
__author__ = "The RO-LE-MA Community"
__license__ = "MIT"


class ROLemaCore:
    """Core converter for RO-LE-MA codes"""
    
    def __init__(self):
        self.version = __version__
        self.special_cases = {
            # Common abbreviations that should stay as-is
            'mcdonalds': 'MCD',
            'kfc': 'KFC',
            'bmw': 'BMW',
            'iphone': 'IPH',
            'usa': 'USA',
            'uk': 'UKX',  # Pad to 3 letters
            'ai': 'AIX',
        }
        
        self.stop_words = ['the', 'and', 'of', 'for', 'in', 'on', 'at', 'by', 'a', 'an']
        self.stats = {'conversions': 0, 'unique_codes': set()}
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize input text"""
        if not text:
            return ""
        # Remove special characters but keep spaces and hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        # Replace hyphens with spaces
        text = text.replace('-', ' ')
        # Convert to uppercase and remove extra spaces
        text = ' '.join(text.upper().split())
        return text
    
    def get_three_letters(self, word: str) -> str:
        """Extract first 3 letters intelligently"""
        word = word.upper()
        
        # Check special cases (case-insensitive)
        if word.lower() in self.special_cases:
            return self.special_cases[word.lower()]
        
        # Handle numbers
        if word.isdigit():
            return word.zfill(3)[:3]
        
        # Handle short words
        if len(word) == 1:
            return word + 'XX'
        elif len(word) == 2:
            return word + 'X'
        else:
            return word[:3]
    
    def convert(self, text: str, skip_stop_words: bool = True) -> Dict:
        """Convert text to RO-LE-MA code"""
        original = text
        cleaned = self.clean_text(text)
        
        if not cleaned:
            return {
                'error': 'Empty input',
                'original': original
            }
        
        # Split into words
        words = cleaned.split()
        
        # Optional: filter stop words
        if skip_stop_words:
            words = [w for w in words if w.lower() not in self.stop_words]
        
        # Generate chunks
        chunks = [self.get_three_letters(word) for word in words]
        
        # Update stats
        self.stats['conversions'] += 1
        code = '-'.join(chunks)
        self.stats['unique_codes'].add(code)
        
        return {
            'original': original,
            'cleaned': cleaned,
            'words': words,
            'code': code,
            'compact': ''.join(chunks),
            'chunks': chunks,
            'length': len(chunks),
            'timestamp': datetime.now().isoformat()
        }
    
    def batch_convert(self, items: List[str], save_to: Optional[str] = None) -> List[Dict]:
        """Convert multiple items"""
        results = []
        for item in items:
            if item.strip():
                results.append(self.convert(item))
        
        if save_to:
            self.export_csv(results, save_to)
        
        return results
    
    def export_csv(self, results: List[Dict], filename: str):
        """Export results to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Original', 'RO-LE-MA Code', 'Compact', 'Words', 'Timestamp'])
            for r in results:
                writer.writerow([
                    r['original'], 
                    r['code'], 
                    r['compact'], 
                    r['length'],
                    r['timestamp']
                ])
        print(f"💾 Saved to {filename}")
    
    def get_stats(self) -> Dict:
        """Get converter statistics"""
        return {
            'version': self.version,
            'total_conversions': self.stats['conversions'],
            'unique_codes_generated': len(self.stats['unique_codes']),
            'special_cases': len(self.special_cases)
        }


class ROLemaCLI:
    """Command line interface"""
    
    def __init__(self):
        self.core = ROLemaCore()
        self.history = []
    
    def display_banner(self):
        banner = """
╔══════════════════════════════════════╗
║     RO-LE-MA v0.1.0                  ║
║     The Universal Code for Everything║
║     MIT License - Open Source         ║
╚══════════════════════════════════════╝
        """
        print(banner)
    
    def display_help(self):
        help_text = """
Commands:
  convert <text>     - Convert text to RO-LE-MA
  batch              - Batch convert multiple items
  stats              - Show conversion statistics
  export <filename>  - Export history to CSV
  clear              - Clear history
  help               - Show this help
  exit               - Exit program

Examples:
  convert Eiffel Tower        -> EIF-TOW
  convert Coca-Cola Can       -> COC-COL-CAN
  convert Robot Learning Machine -> ROB-LEA-MAC
        """
        print(help_text)
    
    def run(self):
        """Main CLI loop"""
        self.display_banner()
        print("Type 'help' for commands, 'exit' to quit\n")
        
        while True:
            try:
                cmd = input("\nro-le-ma> ").strip()
                
                if not cmd:
                    continue
                
                if cmd == 'exit':
                    print("👋 See you, bro! Keep coding!")
                    break
                
                elif cmd == 'help':
                    self.display_help()
                
                elif cmd == 'stats':
                    stats = self.core.get_stats()
                    print("\n📊 Statistics:")
                    for k, v in stats.items():
                        print(f"  {k.replace('_', ' ').title()}: {v}")
                
                elif cmd == 'clear':
                    self.history = []
                    print("🧹 History cleared")
                
                elif cmd.startswith('export '):
                    filename = cmd[7:].strip()
                    if self.history:
                        self.core.export_csv(self.history, filename)
                    else:
                        print("📭 No history to export")
                
                elif cmd == 'batch':
                    print("\n📝 Enter items (empty line to finish):")
                    items = []
                    while True:
                        item = input("  ").strip()
                        if not item:
                            break
                        items.append(item)
                    
                    if items:
                        results = self.core.batch_convert(items)
                        self.history.extend(results)
                        print("\n✅ Results:")
                        for r in results:
                            print(f"  {r['original']:<30} -> {r['code']}")
                
                elif cmd.startswith('convert '):
                    text = cmd[8:].strip()
                    if text:
                        result = self.core.convert(text)
                        if 'error' in result:
                            print(f"❌ Error: {result['error']}")
                        else:
                            print(f"\n✅ {result['original']}")
                            print(f"   RO-LE-MA: {result['code']}")
                            print(f"   Compact:  {result['compact']}")
                            
                            # Copy to clipboard if available
                            try:
                                pyperclip.copy(result['code'])
                                print("📋 Copied to clipboard!")
                            except:
                                pass
                            
                            self.history.append(result)
                    else:
                        print("❌ Please enter text to convert")
                
                else:
                    print("❌ Unknown command. Type 'help'")
            
            except KeyboardInterrupt:
                print("\n👋 Later, bro!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def quick_test():
    """Run quick tests"""
    core = ROLemaCore()
    test_cases = [
        "Eiffel Tower",
        "Liberty Statute",
        "Coca-Cola Can",
        "Empire State Building",
        "Robot Learning Machine",
        "iPhone 15 Pro Max",
        "McDonald's Big Mac",
        "Star Wars Darth Vader"
    ]
    
    print("\n🔷 Testing RO-LE-MA Converter 🔷\n")
    for test in test_cases:
        result = core.convert(test)
        print(f"{test:<30} -> {result['code']}")
    
    print(f"\n📊 Stats: {core.get_stats()}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line mode
        core = ROLemaCore()
        text = ' '.join(sys.argv[1:])
        result = core.convert(text)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(result['code'])
    else:
        # Interactive mode
        cli = ROLemaCLI()
        cli.run()


if __name__ == "__main__":
    # Show test on startup
    quick_test()
    
    # Ask to continue
    response = input("\n🚀 Start interactive mode? (y/n): ").strip().lower()
    if response == 'y':
        main()
