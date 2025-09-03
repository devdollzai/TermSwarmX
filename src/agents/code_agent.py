"""
Code Agent for AI Swarm IDE
Handles code generation, refactoring, analysis, and debugging tasks
"""

import asyncio
import re
from typing import Dict, List, Optional, Any
from pathlib import Path

from .base_agent import BaseAgent, AgentConfig

class CodeAgent(BaseAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.code_context = {}
        self.file_cache = {}
        
        # Extend capabilities for code-specific tasks
        self.config.capabilities.extend([
            "code_generation",
            "code_refactoring", 
            "code_analysis",
            "debugging",
            "documentation",
            "testing"
        ])
    
    def can_handle_task(self, task_data: Dict[str, Any]) -> bool:
        """Check if this agent can handle a code-related task"""
        task_type = task_data.get("type", "")
        return task_type in [
            "generate_code",
            "refactor_code",
            "analyze_code",
            "debug_code",
            "document_code",
            "test_code"
        ]
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a code-related task"""
        task_type = task_data.get("type", "")
        
        try:
            if task_type == "generate_code":
                return await self._generate_code(task_data)
            elif task_type == "refactor_code":
                return await self._refactor_code(task_data)
            elif task_type == "analyze_code":
                return await self._analyze_code(task_data)
            elif task_type == "debug_code":
                return await self._debug_code(task_data)
            elif task_type == "document_code":
                return await self._document_code(task_data)
            elif task_type == "test_code":
                return await self._test_code(task_data)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
        
        except Exception as e:
            self.logger.error(f"Error processing {task_type} task: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_type": task_type
            }
    
    async def _generate_code(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code based on requirements"""
        requirements = task_data.get("requirements", "")
        language = task_data.get("language", "python")
        context = task_data.get("context", "")
        
        self.console.print(f"[cyan]🔧 Generating {language} code for: {requirements}[/cyan]")
        
        # Simulate code generation (in real implementation, this would call an LLM)
        await asyncio.sleep(2)  # Simulate processing time
        
        # Generate sample code based on requirements
        generated_code = self._create_sample_code(requirements, language, context)
        
        return {
            "success": True,
            "generated_code": generated_code,
            "language": language,
            "requirements": requirements,
            "metadata": {
                "lines_of_code": len(generated_code.split('\n')),
                "complexity": "medium"
            }
        }
    
    async def _refactor_code(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Refactor existing code"""
        code = task_data.get("code", "")
        refactoring_type = task_data.get("refactoring_type", "general")
        
        self.console.print(f"[cyan]🔄 Refactoring code with {refactoring_type} approach[/cyan]")
        
        await asyncio.sleep(1.5)  # Simulate processing time
        
        # Apply refactoring (simplified)
        refactored_code = self._apply_refactoring(code, refactoring_type)
        
        return {
            "success": True,
            "original_code": code,
            "refactored_code": refactored_code,
            "refactoring_type": refactoring_type,
            "improvements": [
                "Improved readability",
                "Reduced complexity",
                "Better naming conventions"
            ]
        }
    
    async def _analyze_code(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code quality and provide insights"""
        code = task_data.get("code", "")
        
        self.console.print(f"[cyan]🔍 Analyzing code quality[/cyan]")
        
        await asyncio.sleep(1)  # Simulate processing time
        
        # Perform code analysis
        analysis = self._analyze_code_quality(code)
        
        return {
            "success": True,
            "analysis": analysis,
            "recommendations": analysis.get("recommendations", []),
            "metrics": analysis.get("metrics", {})
        }
    
    async def _debug_code(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Debug code and identify issues"""
        code = task_data.get("code", "")
        error_message = task_data.get("error_message", "")
        
        self.console.print(f"[cyan]🐛 Debugging code with error: {error_message}[/cyan]")
        
        await asyncio.sleep(2)  # Simulate processing time
        
        # Debug the code
        debug_result = self._debug_code_issues(code, error_message)
        
        return {
            "success": True,
            "debug_result": debug_result,
            "issues_found": len(debug_result.get("issues", [])),
            "suggested_fixes": debug_result.get("suggested_fixes", [])
        }
    
    async def _document_code(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate documentation for code"""
        code = task_data.get("code", "")
        doc_type = task_data.get("doc_type", "docstring")
        
        self.console.print(f"[cyan]📚 Generating {doc_type} documentation[/cyan]")
        
        await asyncio.sleep(1.5)  # Simulate processing time
        
        # Generate documentation
        documentation = self._generate_documentation(code, doc_type)
        
        return {
            "success": True,
            "documentation": documentation,
            "doc_type": doc_type,
            "coverage": "95%"
        }
    
    async def _test_code(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tests for code"""
        code = task_data.get("code", "")
        test_framework = task_data.get("test_framework", "pytest")
        
        self.console.print(f"[cyan]🧪 Generating {test_framework} tests[/cyan]")
        
        await asyncio.sleep(2)  # Simulate processing time
        
        # Generate tests
        tests = self._generate_tests(code, test_framework)
        
        return {
            "success": True,
            "tests": tests,
            "test_framework": test_framework,
            "test_coverage": "85%",
            "test_count": len(tests.split('\n'))
        }
    
    def _create_sample_code(self, requirements: str, language: str, context: str) -> str:
        """Create sample code based on requirements"""
        if "function" in requirements.lower():
            return f'''def {requirements.lower().replace(" ", "_")}(param1, param2):
    """
    {requirements}
    
    Args:
        param1: First parameter
        param2: Second parameter
    
    Returns:
        Result of the operation
    """
    result = param1 + param2
    return result

# Example usage
if __name__ == "__main__":
    result = {requirements.lower().replace(" ", "_")}(10, 20)
    print(f"Result: {{result}}")'''
        
        elif "class" in requirements.lower():
            return f'''class {requirements.replace(" ", "")}:
    """
    {requirements}
    """
    
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name

# Example usage
obj = {requirements.replace(" ", "")}("Example")
print(obj.get_name())'''
        
        else:
            return f'''# {requirements}
# This is a sample implementation

def main():
    print("Hello, World!")
    print("This code was generated by the AI Swarm IDE Code Agent")

if __name__ == "__main__":
    main()'''
    
    def _apply_refactoring(self, code: str, refactoring_type: str) -> str:
        """Apply refactoring to code"""
        if refactoring_type == "extract_method":
            # Extract method refactoring
            return code.replace("def main():", "def main():\n    process_data()\n\ndef process_data():")
        elif refactoring_type == "rename_variable":
            # Rename variable refactoring
            return code.replace("x = 10", "counter = 10")
        else:
            # General refactoring
            return code.replace("print(", "logger.info(")
    
    def _analyze_code_quality(self, code: str) -> Dict[str, Any]:
        """Analyze code quality"""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        metrics = {
            "total_lines": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "comment_ratio": len([line for line in lines if line.strip().startswith('#')]) / max(len(lines), 1),
            "function_count": len([line for line in lines if line.strip().startswith('def ')]),
            "class_count": len([line for line in lines if line.strip().startswith('class ')])
        }
        
        recommendations = []
        if metrics["comment_ratio"] < 0.1:
            recommendations.append("Consider adding more comments for better readability")
        if metrics["function_count"] == 0:
            recommendations.append("Consider breaking down code into smaller functions")
        
        return {
            "metrics": metrics,
            "recommendations": recommendations,
            "overall_score": min(100, max(0, 100 - len(recommendations) * 20))
        }
    
    def _debug_code_issues(self, code: str, error_message: str) -> Dict[str, Any]:
        """Debug code and identify issues"""
        issues = []
        suggested_fixes = []
        
        # Simple pattern matching for common issues
        if "NameError" in error_message:
            issues.append("Undefined variable or function")
            suggested_fixes.append("Check variable names and ensure all functions are defined")
        
        if "IndentationError" in error_message:
            issues.append("Incorrect indentation")
            suggested_fixes.append("Check indentation levels and ensure consistency")
        
        if "SyntaxError" in error_message:
            issues.append("Syntax error in code")
            suggested_fixes.append("Review code syntax and check for missing brackets, quotes, etc.")
        
        return {
            "issues": issues,
            "suggested_fixes": suggested_fixes,
            "error_type": error_message.split(":")[0] if ":" in error_message else "Unknown"
        }
    
    def _generate_documentation(self, code: str, doc_type: str) -> str:
        """Generate documentation for code"""
        if doc_type == "docstring":
            return '''"""
This module provides functionality for data processing.

Classes:
    DataProcessor: Main class for processing data
    
Functions:
    process_data: Process input data and return results
    validate_input: Validate input parameters
"""'''
        else:
            return "# Code Documentation\n# This code implements the required functionality\n# Use the provided functions and classes as documented"
    
    def _generate_tests(self, code: str, test_framework: str) -> str:
        """Generate tests for code"""
        if test_framework == "pytest":
            return '''import pytest
from your_module import your_function

def test_your_function():
    """Test the your_function"""
    result = your_function(2, 3)
    assert result == 5

def test_your_function_edge_cases():
    """Test edge cases"""
    result = your_function(0, 0)
    assert result == 0'''
        else:
            return '''import unittest

class TestYourFunction(unittest.TestCase):
    def test_your_function(self):
        result = your_function(2, 3)
        self.assertEqual(result, 5)

if __name__ == '__main__':
    unittest.main()'''
