#!/usr/bin/env python3
"""
Frontend Display Diagnostic Test
Tests if uploaded file analysis results actually display on the browser
"""
import time
import json
from datetime import datetime

print(f"\n{'='*60}")
print(f"Frontend Display Diagnostic Test - {datetime.now().strftime('%H:%M:%S')}")
print(f"{'='*60}\n")

# Step 1: Check if resultsSection element exists in HTML
print("Step 1: Checking HTML for resultsSection element...")
try:
    with open(r'c:\Users\rakes\Downloads\blood report ai\templates\index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    if 'id="resultsSection"' in html_content:
        print("✅ resultsSection element FOUND in HTML")
        
        # Find the line
        lines = html_content.split('\n')
        for i, line in enumerate(lines):
            if 'id="resultsSection"' in line:
                print(f"   Location: Line {i+1}")
                print(f"   HTML: {line.strip()}")
                break
    else:
        print("❌ resultsSection element NOT FOUND in HTML - This is critical!")
except Exception as e:
    print(f"❌ Error reading HTML: {e}")

# Step 2: Check CSS for results-section styling
print("\nStep 2: Checking CSS for .results-section styling...")
try:
    with open(r'c:\Users\rakes\Downloads\blood report ai\templates\index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    if '.results-section {' in html_content:
        print("✅ .results-section CSS class FOUND")
        
        # Find the lines
        lines = html_content.split('\n')
        in_class = False
        for i, line in enumerate(lines):
            if '.results-section {' in line:
                in_class = True
                start_line = i+1
            if in_class:
                print(f"   {line}")
                if line.strip() == '}':
                    in_class = False
                    break
    else:
        print("❌ .results-section CSS class NOT FOUND")
        
    # Check for .results-section.show
    if '.results-section.show {' in html_content:
        print("\n✅ .results-section.show CSS class FOUND")
        lines = html_content.split('\n')
        in_class = False
        for i, line in enumerate(lines):
            if '.results-section.show {' in line:
                in_class = True
                start_line = i+1
            if in_class:
                print(f"   {line}")
                if line.strip() == '}':
                    in_class = False
                    break
    else:
        print("❌ .results-section.show CSS class NOT FOUND - This is critical!")
        
except Exception as e:
    print(f"❌ Error checking CSS: {e}")

# Step 3: Check JavaScript showResults function
print("\nStep 3: Checking JavaScript showResults function...")
try:
    with open(r'c:\Users\rakes\Downloads\blood report ai\templates\index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    if 'function showResults(data)' in html_content:
        print("✅ showResults function FOUND")
        
        # Check what it does
        if 'resultsSection.innerHTML = html;' in html_content:
            print("✅ Sets resultsSection.innerHTML")
        else:
            print("❌ Does NOT set resultsSection.innerHTML")
            
        if "resultsSection.classList.add('show')" in html_content:
            print("✅ Adds 'show' class to resultsSection")
        else:
            print("❌ Does NOT add 'show' class")
            
        if "showView('analysis')" in html_content:
            print("✅ Calls showView('analysis')")
        else:
            print("⚠️  Does NOT explicitly call showView")
    else:
        print("❌ showResults function NOT FOUND")
        
except Exception as e:
    print(f"❌ Error checking showResults: {e}")

# Step 4: Check uploadFile function
print("\nStep 4: Checking uploadFile function...")
try:
    with open(r'c:\Users\rakes\Downloads\blood report ai\templates\index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    if 'async function uploadFile(file)' in html_content:
        print("✅ uploadFile function FOUND")
        
        if 'const response = await fetch' in html_content:
            print("✅ Uses fetch to upload")
        
        if 'if (response.ok)' in html_content:
            print("✅ Has response.ok check")
        
        # Check the critical part
        if 'showResults(data)' in html_content:
            print("✅ Calls showResults(data) on success")
        else:
            print("❌ Does NOT call showResults")
            
    else:
        print("❌ uploadFile function NOT FOUND")
        
except Exception as e:
    print(f"❌ Error checking uploadFile: {e}")

# Step 5: Check showView function
print("\nStep 5: Checking showView function...")
try:
    with open(r'c:\Users\rakes\Downloads\blood report ai\templates\index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    if 'function showView(view)' in html_content:
        print("✅ showView function FOUND")
        
        if "analysis.style.display = 'block'" in html_content:
            print("✅ Shows analysis section when view='analysis'")
        
        if "dashboard.classList.add('active')" in html_content:
            print("✅ Shows dashboard when view='dashboard'")
            
    else:
        print("❌ showView function NOT FOUND")
        
except Exception as e:
    print(f"❌ Error checking showView: {e}")

# Step 6: Analyze CSS opacity issue
print("\n" + "="*60)
print("ANALYSIS: Potential CSS Opacity Issue")
print("="*60)

try:
    with open(r'c:\Users\rakes\Downloads\blood report ai\templates\index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract the CSS animation and opacity
    import re
    
    results_section_match = re.search(r'\.results-section\s*\{([^}]+)\}', html_content)
    if results_section_match:
        css_content = results_section_match.group(1)
        print("\n.results-section CSS:")
        print(css_content)
        
        if 'opacity: 0' in css_content:
            print("\n⚠️  WARNING: Initial opacity is 0 (invisible)")
            print("   This is intentional - element should be shown via .show class")
        
        if 'animation:' in css_content:
            animation_match = re.search(r'animation:\s*([^;]+);', css_content)
            if animation_match:
                print(f"\n⚠️  WARNING: Animation is: {animation_match.group(1)}")
                print("   This animation might delay visibility on fast uploads")
    
    # Check if there's a timing issue
    print("\n" + "="*60)
    print("POTENTIAL ISSUES:")
    print("="*60)
    
    print("\n1. ANIMATION DELAY ISSUE:")
    print("   - If .results-section has animation with delay")
    print("   - And it runs AFTER .show class is added")
    print("   - The animation might override opacity:1 temporarily")
    
    print("\n2. CSS SPECIFICITY:")
    print("   - .results-section.show should have higher specificity")
    print("   - than .results-section")
    print("   - Check if opacity:1 in .show rule is being applied")
    
    print("\n3. JAVASCRIPT TIMING:")
    print("   - Make sure showResults() is actually being called")
    print("   - Add console.log to verify execution")
    
    print("\n4. VISIBILITY MODE:")
    print("   - Check if opacity:0 vs display:none is the issue")
    print("   - Element exists but is invisible (opacity:0)")
    
except Exception as e:
    print(f"❌ Error in analysis: {e}")

# Step 7: Recommendation
print("\n" + "="*60)
print("RECOMMENDED FIX:")
print("="*60)

print("""
To ensure results display immediately:

1. MODIFY CSS for .results-section:
   Change from:
   -----------
   .results-section {
       opacity: 0;
       animation: fadeIn 1s ease-out 0.5s both;
   }
   .results-section.show {
       opacity: 1;
   }
   
   To:
   -----------
   .results-section {
       opacity: 0;
   }
   .results-section.show {
       opacity: 1 !important;
       animation: none !important;
   }
   
   This ensures that when .show class is added:
   - opacity becomes 1 immediately (no animation delay)
   - Any animation is cancelled
   - The element is 100% visible

2. OR: Use display property instead:
   Change from using opacity to display
   
   .results-section {
       display: none;
   }
   .results-section.show {
       display: block;
   }

3. ADD CONSOLE.LOG to verify execution:
   In showResults():
   -----------------
   console.log("showResults called with data:", data);
   console.log("resultsSection.classList:", resultsSection.classList);
   
   This will help debug if the function is even being called.
""")

print("="*60)
print("Test Complete")
print("="*60 + "\n")
