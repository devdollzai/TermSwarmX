#!/usr/bin/env python3
"""
Sample Plugin for DevDollz: Atelier Edition
Demonstrates the plugin system with a custom code analysis agent
"""

import json
import time
from typing import Dict, Any

def create_message(content: str, meta: Dict[str, Any] = None) -> str:
    """Create a structured message for agent communication"""
    return json.dumps({"content": content, "meta": meta or {}})

def parse_message(msg: str) -> Dict[str, Any]:
    """Parse a structured message from agent communication"""
    return json.loads(msg)

def plugin_agent(input_queue, output_queue):
    """
    Custom plugin agent for code analysis and optimization
    
    This agent provides:
    - Code complexity analysis
    - Performance optimization suggestions
    - Security vulnerability scanning
    - Code style recommendations
    """
    
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                break
                
            task = parse_message(raw_task)
            cmd_type = task['meta'].get('type', '')
            code = task['content']
            
            if cmd_type == "complexity":
                result = analyze_code_complexity(code)
            elif cmd_type == "performance":
                result = analyze_performance(code)
            elif cmd_type == "security":
                result = analyze_security(code)
            elif cmd_type == "style":
                result = analyze_code_style(code)
            else:
                result = comprehensive_analysis(code)
            
            meta = {"status": "success", "timestamp": time.time()}
            output_queue.put(create_message(result, meta))
            
        except Exception as e:
            meta = {"status": "error", "error": str(e)}
            output_queue.put(create_message(f"Plugin agent error: {e}", meta))

def analyze_code_complexity(code: str) -> str:
    """Analyze code complexity and provide insights"""
    lines = code.split('\n')
    complexity_score = 0
    
    # Simple complexity analysis
    for line in lines:
        line = line.strip()
        if line.startswith('if ') or line.startswith('elif '):
            complexity_score += 1
        elif line.startswith('for ') or line.startswith('while '):
            complexity_score += 2
        elif line.startswith('def ') or line.startswith('class '):
            complexity_score += 1
        elif ' and ' in line or ' or ' in line:
            complexity_score += 1
    
    if complexity_score <= 3:
        level = "Low"
        recommendation = "Code is well-structured and maintainable."
    elif complexity_score <= 7:
        level = "Medium"
        recommendation = "Consider breaking down complex functions."
    else:
        level = "High"
        recommendation = "Refactor to reduce complexity. Consider extracting methods."
    
    return f"""Code Complexity Analysis:
Complexity Score: {complexity_score}/10 ({level})
Recommendation: {recommendation}

Breakdown:
- Control structures: {sum(1 for line in lines if line.strip().startswith(('if ', 'elif ', 'for ', 'while ')))}
- Functions/Classes: {sum(1 for line in lines if line.strip().startswith(('def ', 'class ')))}
- Logical operators: {sum(1 for line in lines if ' and ' in line or ' or ' in line)}"""

def analyze_performance(code: str) -> str:
    """Analyze code for performance issues"""
    issues = []
    suggestions = []
    
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Check for common performance issues
        if 'for ' in line and ' in ' in line and 'range(' in line:
            if 'len(' in line:
                issues.append(f"Line {i}: Consider using enumerate() instead of range(len())")
                suggestions.append("Replace with: for i, item in enumerate(collection)")
        
        if 'list(' in line and 'map(' in line:
            issues.append(f"Line {i}: map() with list() creates unnecessary intermediate list")
            suggestions.append("Use generator expression or list comprehension instead")
        
        if 'in ' in line and line.count('in') > 1:
            issues.append(f"Line {i}: Multiple 'in' operations can be optimized")
            suggestions.append("Consider using sets for faster membership testing")
    
    if not issues:
        return "Performance Analysis: No obvious performance issues detected. Code appears well-optimized."
    
    result = "Performance Analysis - Issues Found:\n"
    for issue in issues:
        result += f"⚠️  {issue}\n"
    
    result += "\nOptimization Suggestions:\n"
    for suggestion in suggestions:
        result += f"💡 {suggestion}\n"
    
    return result

def analyze_security(code: str) -> str:
    """Analyze code for security vulnerabilities"""
    vulnerabilities = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Check for common security issues
        if 'eval(' in line:
            vulnerabilities.append(f"Line {i}: eval() usage - potential code injection risk")
        
        if 'exec(' in line:
            vulnerabilities.append(f"Line {i}: exec() usage - potential code injection risk")
        
        if 'input(' in line and 'int(' not in line and 'float(' not in line:
            vulnerabilities.append(f"Line {i}: Raw input() usage - consider input validation")
        
        if 'subprocess.call(' in line or 'os.system(' in line:
            vulnerabilities.append(f"Line {i}: Shell command execution - validate user input")
        
        if 'pickle.loads(' in line:
            vulnerabilities.append(f"Line {i}: pickle.loads() - potential deserialization attack")
    
    if not vulnerabilities:
        return "Security Analysis: No obvious security vulnerabilities detected. Code appears secure."
    
    result = "Security Analysis - Vulnerabilities Found:\n"
    for vuln in vulnerabilities:
        result += f"[!] {vuln}\n"
    
    result += "\nSecurity Recommendations:\n"
    result += "• Avoid eval() and exec() with user input\n"
    result += "• Validate and sanitize all user inputs\n"
    result += "• Use subprocess.run() with shell=False\n"
    result += "• Consider using json.loads() instead of pickle\n"
    
    return result

def analyze_code_style(code: str) -> str:
    """Analyze code style and PEP 8 compliance"""
    style_issues = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        line_original = line
        
        # Check line length
        if len(line) > 79:
            style_issues.append(f"Line {i}: Exceeds 79 characters ({len(line)} chars)")
        
        # Check for mixed tabs and spaces
        if '\t' in line and ' ' in line:
            style_issues.append(f"Line {i}: Mixed tabs and spaces")
        
        # Check for trailing whitespace
        if line != line.rstrip():
            style_issues.append(f"Line {i}: Trailing whitespace")
        
        # Check for proper spacing around operators
        if '=' in line and not line.strip().startswith('#'):
            if ' = ' not in line and '==' not in line and '!=' not in line and '<=' not in line and '>=' not in line:
                style_issues.append(f"Line {i}: Missing spaces around assignment operator")
    
    if not style_issues:
        return "Style Analysis: Code follows PEP 8 style guidelines well. No style issues detected."
    
    result = "Style Analysis - PEP 8 Issues Found:\n"
    for issue in style_issues:
        result += f"[*] {issue}\n"
    
    result += "\nStyle Recommendations:\n"
    result += "• Keep lines under 79 characters\n"
    result += "• Use consistent indentation (spaces, not tabs)\n"
    result += "• Remove trailing whitespace\n"
    result += "• Add spaces around operators\n"
    result += "• Use 4 spaces for indentation\n"
    
    return result

def comprehensive_analysis(code: str) -> str:
    """Perform comprehensive code analysis"""
    result = "Comprehensive Code Analysis\n"
    result += "=" * 50 + "\n\n"
    
    # Run all analyses
    result += analyze_code_complexity(code) + "\n\n"
    result += analyze_performance(code) + "\n\n"
    result += analyze_security(code) + "\n\n"
    result += analyze_code_style(code)
    
    return result

# Plugin metadata
PLUGIN_INFO = {
    "name": "Code Analysis Plugin",
    "version": "1.0.0",
    "author": "DevDollz: Atelier Edition",
    "description": "Advanced code analysis and optimization suggestions",
    "commands": [
        "complexity - Analyze code complexity",
        "performance - Check for performance issues", 
        "security - Scan for security vulnerabilities",
        "style - Review PEP 8 compliance",
        "custom - Comprehensive analysis"
    ]
}

if __name__ == "__main__":
    print("Sample Plugin for DevDollz: Atelier Edition")
    print("This plugin provides advanced code analysis capabilities.")
    print("\nUsage:")
    print("  plugin load sample_plugin.py")
    print("  sample_plugin complexity <code>")
    print("  sample_plugin performance <code>")
    print("  sample_plugin security <code>")
    print("  sample_plugin style <code>")
