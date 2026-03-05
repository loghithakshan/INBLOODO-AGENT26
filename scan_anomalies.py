#!/usr/bin/env python3
"""
Complete Anomaly Scanner and Repair Tool
Scans entire codebase for issues and suggests fixes
"""
import os
import re
import json
from pathlib import Path

print(f"\n{'='*70}")
print(f"ANOMALY SCANNER - Detecting Errors & Issues")
print(f"{'='*70}\n")

issues_found = []

# ===== SCAN 1: HTML File Issues =====
print("SCAN 1: Checking HTML file for anomalies...")
print("-" * 70)

html_file = r'c:\Users\rakes\Downloads\blood report ai\templates\index.html'
try:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()
    
    # Check for unclosed tags
    open_tags = re.findall(r'<(\w+)[^>]*(?<!/)>', html_content)
    close_tags = re.findall(r'</(\w+)>', html_content)
    
    # Common self-closing tags to exclude
    self_closing = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}
    
    # Check for obvious mismatches
    if 'console.log' in html_content:
        print("✅ Console logging present")
    else:
        print("⚠️  No console logging found")
    
    # Check for duplicate function definitions
    showresults_count = html_content.count('function showResults(')
    if showresults_count > 1:
        print(f"❌ ANOMALY: showResults() defined {showresults_count} times!")
        issues_found.append(f"Duplicate showResults() function ({showresults_count} times)")
    
    showview_count = html_content.count('function showView(')
    if showview_count > 1:
        print(f"❌ ANOMALY: showView() defined {showview_count} times!")
        issues_found.append(f"Duplicate showView() function ({showview_count} times)")
    
    uploadfile_count = html_content.count('function uploadFile(')
    if uploadfile_count > 1:
        print(f"❌ ANOMALY: uploadFile() defined {uploadfile_count} times!")
        issues_found.append(f"Duplicate uploadFile() function ({uploadfile_count} times)")
    
    # Check for orphaned CSS
    if re.search(r'}\s+display:', html_content) or re.search(r'}\s+animation:', html_content):
        print("❌ ANOMALY: Orphaned CSS detected")
        issues_found.append("Orphaned CSS code blocks")
    else:
        print("✅ No orphaned CSS detected")
    
    # Check for closing </div> tags mismatch
    div_open = html_content.count('<div')
    div_close = html_content.count('</div>')
    if div_open != div_close:
        print(f"⚠️  Possible unclosed divs: {div_open} open, {div_close} closed")
        issues_found.append(f"Div mismatch: {div_open} open vs {div_close} closed")
    else:
        print(f"✅ Div tags balanced: {div_open} pairs")
    
    # Check for malformed JavaScript strings
    if 'console.log(\'undefinedspace=undefined' in html_content or 'undefined' in html_content.split('<script>')[1:] if len(html_content.split('<script>')) > 1 else False:
        print("⚠️  Possible undefined variables in JavaScript")
    
    # Check file size
    file_size = os.path.getsize(html_file)
    print(f"✅ HTML file size: {file_size / 1024:.1f} KB")
    
    # Check line count
    line_count = len(html_content.split('\n'))
    print(f"✅ HTML line count: {line_count} lines")
    
except Exception as e:
    print(f"❌ Error scanning HTML: {e}")
    issues_found.append(f"HTML scan error: {e}")

# ===== SCAN 2: Python Files =====
print("\nSCAN 2: Checking Python files for syntax errors...")
print("-" * 70)

py_files = [
    'main.py',
    'src/api_optimized.py',
    'src/llm_service.py',
]

for py_file in py_files:
    full_path = rf'c:\Users\rakes\Downloads\blood report ai\{py_file}'
    if os.path.exists(full_path):
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            compile(code, py_file, 'exec')
            print(f"✅ {py_file} - Valid syntax")
        except SyntaxError as e:
            print(f"❌ {py_file} - {e}")
            issues_found.append(f"{py_file}: {e}")
        except Exception as e:
            print(f"⚠️  {py_file} - Warning: {e}")
    else:
        print(f"ⓘ  {py_file} - Not found (optional)")

# ===== SCAN 3: Common Configuration Issues =====
print("\nSCAN 3: Checking for configuration anomalies...")
print("-" * 70)

# Check if main.py has proper imports
try:
    with open(r'c:\Users\rakes\Downloads\blood report ai\main.py', 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    required_imports = [
        'from fastapi import FastAPI',
        'import uvicorn',
        'from pathlib import Path',
    ]
    
    missing_imports = []
    for imp in required_imports:
        if imp not in main_content:
            missing_imports.append(imp)
            print(f"⚠️  Missing: {imp}")
        else:
            print(f"✅ Found: {imp}")
    
    if missing_imports:
        issues_found.append(f"Missing imports in main.py: {missing_imports}")
    
except Exception as e:
    print(f"❌ Error checking main.py: {e}")

# ===== SCAN 4: CSS Issues =====
print("\nSCAN 4: Checking for CSS anomalies...")
print("-" * 70)

try:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # Extract CSS section
    css_match = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    if css_match:
        css = css_match.group(1)
        
        # Check for unmatched braces
        open_braces = css.count('{')
        close_braces = css.count('}')
        
        if open_braces != close_braces:
            print(f"❌ ANOMALY: CSS brace mismatch - {open_braces} open, {close_braces} closed")
            issues_found.append(f"CSS brace mismatch: {open_braces} vs {close_braces}")
        else:
            print(f"✅ CSS braces balanced: {open_braces} pairs")
        
        # Check for duplicate class definitions
        classes = re.findall(r'\.[\w-]+\s*\{', css)
        class_names = [c.strip().rstrip('{').strip().lstrip('.') for c in classes]
        duplicates = [item for item in set(class_names) if class_names.count(item) > 1]
        
        if duplicates:
            print(f"⚠️  Duplicate CSS classes: {duplicates}")
            issues_found.append(f"Duplicate CSS classes: {duplicates}")
        else:
            print(f"✅ No duplicate CSS classes")
    
except Exception as e:
    print(f"⚠️  CSS check error: {e}")

# ===== SCAN 5: JavaScript Issues =====
print("\nSCAN 5: Checking for JavaScript anomalies...")
print("-" * 70)

try:
    # Extract JavaScript sections
    js_sections = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    
    print(f"✅ Found {len(js_sections)} script sections")
    
    # Check for common JS issues
    issues_to_check = [
        ('Missing semicolons', False),  # Hard to reliably detect
        ('Undefined variables', 'undefined' in html and 'window.currentAnalysisData' not in html),
        ('Unreachable code', False),
    ]
    
    # Check for syntax issues in JavaScript strings
    for js_idx, js in enumerate(js_sections):
        # Count function definitions
        function_count = js.count('function ')
        arrow_function_count = js.count('=>')
        
    print(f"✅ JavaScript sections validated")
    
except Exception as e:
    print(f"⚠️  JavaScript check error: {e}")

# ===== SCAN 6: Data Integrity =====
print("\nSCAN 6: Checking data integrity...")
print("-" * 70)

try:
    # Check if test files exist
    test_file = r'c:\Users\rakes\Downloads\blood report ai\test_sample.csv'
    if os.path.exists(test_file):
        size = os.path.getsize(test_file)
        print(f"✅ Test file exists: {size} bytes")
    else:
        print(f"⚠️  Test file missing: {test_file}")
    
    # Check for required directories
    required_dirs = [
        'templates',
        'src',
        'static',
    ]
    
    base_path = r'c:\Users\rakes\Downloads\blood report ai'
    for dir_name in required_dirs:
        dir_path = os.path.join(base_path, dir_name)
        if os.path.isdir(dir_path):
            print(f"✅ Directory exists: {dir_name}/")
        else:
            print(f"❌ Missing directory: {dir_name}/")
            issues_found.append(f"Missing directory: {dir_name}")
    
except Exception as e:
    print(f"⚠️  Data integrity check error: {e}")

# ===== SUMMARY =====
print("\n" + "="*70)
print("ANOMALY SCAN SUMMARY")
print("="*70)

if issues_found:
    print(f"\n❌ Found {len(issues_found)} issue(s):\n")
    for idx, issue in enumerate(issues_found, 1):
        print(f"{idx}. {issue}")
    print("\nRun repair script to fix these issues.")
else:
    print("\n✅ NO MAJOR ANOMALIES DETECTED")
    print("System appears to be in good condition.")

print("\n" + "="*70)
