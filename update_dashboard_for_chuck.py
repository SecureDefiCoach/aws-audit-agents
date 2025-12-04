#!/usr/bin/env python3
"""
Quick script to update dashboard for Chuck styling
"""

# Read the dashboard HTML
with open('src/web/templates/dashboard.html', 'r') as f:
    content = f.read()

# Add CSS for company-rep-card after agent-card:hover
css_to_add = """
        
        .company-rep-card {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
        }
        
        .company-rep-card:hover {
            background: #f1f3f5;
        }"""

# Find the agent-card:hover section and add after it
import re
pattern = r'(\.agent-card:hover\s*\{[^}]+\})'
replacement = r'\1' + css_to_add
content = re.sub(pattern, replacement, content)

# Update the displayAgents function to sort Chuck first and add class
# Find the function
pattern = r'(function displayAgents\(agents\) \{[^}]+grid\.innerHTML = )agents\.map\(agent => `'
replacement = r'''\1(() => {
                // Sort agents: Chuck first, then others
                const sortedAgents = [...agents].sort((a, b) => {
                    if (a.name.toLowerCase() === 'chuck') return -1;
                    if (b.name.toLowerCase() === 'chuck') return 1;
                    return 0;
                });
                return sortedAgents;
            })().map(agent => {
                const isChuck = agent.name.toLowerCase() === 'chuck';
                const cardClass = isChuck ? 'agent-card company-rep-card' : 'agent-card';
                return `
                <div class="${cardClass}" onclick="showAgentDetails('${agent.name}')">'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Also need to fix the closing of the map
content = content.replace(
    '</div>\n            `).join(\'\');',
    '</div>\n                `;\n            }).join(\'\');'
)

# Write back
with open('src/web/templates/dashboard.html', 'w') as f:
    f.write(content)

print("✓ Dashboard updated for Chuck styling")
print("  - Added company-rep-card CSS class (lighter shade)")
print("  - Chuck's card will appear first")
print("  - Chuck's card has lighter background")
