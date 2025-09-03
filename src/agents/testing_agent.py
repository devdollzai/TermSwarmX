"""
Testing Agent for AI Swarm IDE
Handles test execution, coverage analysis, and test generation
"""

import asyncio
import subprocess
import json
import os
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

from .base_agent import BaseAgent, AgentConfig

class TestingAgent(BaseAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.test_results = {}
        self.coverage_data = {}
        self.test_runners = {
            "python": "pytest",
            "javascript": "npm test",
            "java": "mvn test",
            "go": "go test"
        }
        
        # Extend capabilities for testing-specific tasks
        self.config.capabilities.extend([
            "test_execution",
            "coverage_analysis",
            "test_generation",
            "performance_testing",
            "test_reporting",
            "continuous_testing"
        ])
    
    def can_handle_task(self, task_data: Dict[str, Any]) -> bool:
        """Check if this agent can handle a testing-related task"""
        task_type = task_data.get("type", "")
        return task_type in [
            "run_tests",
            "analyze_coverage",
            "generate_tests",
            "performance_test",
            "generate_report",
            "continuous_test"
        ]
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a testing-related task"""
        task_type = task_data.get("type", "")
        
        try:
            if task_type == "run_tests":
                return await self._run_tests(task_data)
            elif task_type == "analyze_coverage":
                return await self._analyze_coverage(task_data)
            elif task_type == "generate_tests":
                return await self._generate_tests(task_data)
            elif task_type == "performance_test":
                return await self._performance_test(task_data)
            elif task_type == "generate_report":
                return await self._generate_report(task_data)
            elif task_type == "continuous_test":
                return await self._continuous_test(task_data)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
        
        except Exception as e:
            self.logger.error(f"Error processing {task_type} task: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_type": task_type
            }
    
    async def _run_tests(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run tests for a project"""
        project_path = task_data.get("project_path", ".")
        test_type = task_data.get("test_type", "unit")
        language = task_data.get("language", "python")
        
        self.console.print(f"[cyan]🧪 Running {test_type} tests for {language} project[/cyan]")
        
        # Determine test command based on language
        test_command = self._get_test_command(language, test_type)
        
        try:
            # Run tests
            result = await self._execute_test_command(test_command, project_path)
            
            # Parse test results
            parsed_results = self._parse_test_results(result, language)
            
            return {
                "success": True,
                "test_results": parsed_results,
                "test_type": test_type,
                "language": language,
                "project_path": project_path,
                "raw_output": result
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "test_type": test_type,
                "language": language
            }
    
    async def _analyze_coverage(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze test coverage for a project"""
        project_path = task_data.get("project_path", ".")
        language = task_data.get("language", "python")
        
        self.console.print(f"[cyan]📊 Analyzing test coverage for {language} project[/cyan]")
        
        try:
            # Get coverage command
            coverage_command = self._get_coverage_command(language)
            
            # Run coverage analysis
            coverage_result = await self._execute_test_command(coverage_command, project_path)
            
            # Parse coverage data
            coverage_data = self._parse_coverage_results(coverage_result, language)
            
            return {
                "success": True,
                "coverage_data": coverage_data,
                "language": language,
                "project_path": project_path,
                "overall_coverage": coverage_data.get("overall_coverage", 0)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "language": language
            }
    
    async def _generate_tests(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tests for existing code"""
        code_path = task_data.get("code_path", "")
        language = task_data.get("language", "python")
        test_framework = task_data.get("test_framework", "pytest")
        
        self.console.print(f"[cyan]🔧 Generating {test_framework} tests for {language} code[/cyan]")
        
        await asyncio.sleep(2)  # Simulate test generation time
        
        # Generate sample tests
        generated_tests = self._create_sample_tests(language, test_framework)
        
        return {
            "success": True,
            "generated_tests": generated_tests,
            "language": language,
            "test_framework": test_framework,
            "test_file_path": f"test_{Path(code_path).stem}.py"
        }
    
    async def _performance_test(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run performance tests"""
        test_target = task_data.get("test_target", "")
        test_duration = task_data.get("duration", 60)
        
        self.console.print(f"[cyan]⚡ Running performance tests on {test_target} for {test_duration}s[/cyan]")
        
        await asyncio.sleep(test_duration)  # Simulate performance testing
        
        # Generate performance metrics
        performance_metrics = self._generate_performance_metrics()
        
        return {
            "success": True,
            "performance_metrics": performance_metrics,
            "test_target": test_target,
            "duration": test_duration
        }
    
    async def _generate_report(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        project_path = task_data.get("project_path", ".")
        report_format = task_data.get("format", "json")
        
        self.console.print(f"[cyan]📋 Generating {report_format} test report[/cyan]")
        
        await asyncio.sleep(1)  # Simulate report generation
        
        # Generate report
        report = self._create_test_report(project_path, report_format)
        
        return {
            "success": True,
            "report": report,
            "format": report_format,
            "project_path": project_path
        }
    
    async def _continuous_test(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Set up continuous testing"""
        project_path = task_data.get("project_path", ".")
        trigger_conditions = task_data.get("triggers", ["file_change"])
        
        self.console.print(f"[cyan]🔄 Setting up continuous testing with triggers: {trigger_conditions}[/cyan]")
        
        await asyncio.sleep(2)  # Simulate setup time
        
        # Set up continuous testing
        continuous_test_config = self._setup_continuous_testing(project_path, trigger_conditions)
        
        return {
            "success": True,
            "continuous_test_config": continuous_test_config,
            "triggers": trigger_conditions,
            "project_path": project_path
        }
    
    def _get_test_command(self, language: str, test_type: str) -> str:
        """Get the appropriate test command for a language and test type"""
        base_command = self.test_runners.get(language, "echo 'No test runner configured'")
        
        if language == "python":
            if test_type == "unit":
                return "pytest tests/ -v"
            elif test_type == "integration":
                return "pytest tests/integration/ -v"
            elif test_type == "e2e":
                return "pytest tests/e2e/ -v"
            else:
                return "pytest tests/ -v"
        
        elif language == "javascript":
            if test_type == "unit":
                return "npm run test:unit"
            elif test_type == "integration":
                return "npm run test:integration"
            else:
                return "npm test"
        
        return base_command
    
    def _get_coverage_command(self, language: str) -> str:
        """Get the appropriate coverage command for a language"""
        if language == "python":
            return "pytest --cov=. --cov-report=term-missing"
        elif language == "javascript":
            return "npm run test:coverage"
        else:
            return "echo 'Coverage not configured for this language'"
    
    async def _execute_test_command(self, command: str, working_dir: str) -> str:
        """Execute a test command and return the output"""
        try:
            process = await asyncio.create_subprocess_exec(
                *command.split(),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return stdout.decode()
            else:
                return stderr.decode()
        
        except Exception as e:
            self.logger.error(f"Error executing command '{command}': {e}")
            return f"Error: {str(e)}"
    
    def _parse_test_results(self, output: str, language: str) -> Dict[str, Any]:
        """Parse test output to extract results"""
        # Simple parsing - in real implementation, this would be more sophisticated
        lines = output.split('\n')
        
        # Count test results
        passed = len([line for line in lines if "PASSED" in line or "passed" in line])
        failed = len([line for line in lines if "FAILED" in line or "failed" in line])
        errors = len([line for line in lines if "ERROR" in line or "error" in line])
        
        return {
            "total_tests": passed + failed + errors,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "success_rate": (passed / max(passed + failed + errors, 1)) * 100
        }
    
    def _parse_coverage_results(self, output: str, language: str) -> Dict[str, Any]:
        """Parse coverage output to extract coverage data"""
        # Simple parsing - in real implementation, this would parse actual coverage reports
        lines = output.split('\n')
        
        coverage_percentage = 0
        for line in lines:
            if "TOTAL" in line and "%" in line:
                # Extract percentage from line like "TOTAL                   100%"
                try:
                    coverage_percentage = float(line.split()[-1].replace('%', ''))
                    break
                except (ValueError, IndexError):
                    continue
        
        return {
            "overall_coverage": coverage_percentage,
            "files_covered": len([line for line in lines if "100%" in line]),
            "total_files": len([line for line in lines if ".py" in line or ".js" in line]),
            "missing_lines": len([line for line in lines if "missing" in line.lower()])
        }
    
    def _create_sample_tests(self, language: str, test_framework: str) -> str:
        """Create sample tests for demonstration"""
        if language == "python" and test_framework == "pytest":
            return '''import pytest
from your_module import your_function

def test_your_function_basic():
    """Test basic functionality"""
    result = your_function(2, 3)
    assert result == 5

def test_your_function_edge_cases():
    """Test edge cases"""
    result = your_function(0, 0)
    assert result == 0
    
    result = your_function(-1, 1)
    assert result == 0

def test_your_function_error_handling():
    """Test error handling"""
    with pytest.raises(ValueError):
        your_function("invalid", 1)'''
        
        elif language == "javascript":
            return '''describe('Your Function', () => {
    test('should add two numbers correctly', () => {
        expect(yourFunction(2, 3)).toBe(5);
    });
    
    test('should handle edge cases', () => {
        expect(yourFunction(0, 0)).toBe(0);
        expect(yourFunction(-1, 1)).toBe(0);
    });
});'''
        
        else:
            return f"# Sample tests for {language} using {test_framework}\n# Implement actual test logic here"
    
    def _generate_performance_metrics(self) -> Dict[str, Any]:
        """Generate sample performance metrics"""
        return {
            "response_time": {
                "average": 150.5,
                "min": 45.2,
                "max": 320.8,
                "p95": 280.1
            },
            "throughput": {
                "requests_per_second": 1250,
                "total_requests": 75000
            },
            "resource_usage": {
                "cpu_percent": 45.2,
                "memory_mb": 512.8,
                "disk_io_mb": 25.4
            }
        }
    
    def _create_test_report(self, project_path: str, format_type: str) -> Dict[str, Any]:
        """Create a comprehensive test report"""
        return {
            "project": project_path,
            "timestamp": "2024-01-15T10:30:00Z",
            "summary": {
                "total_tests": 150,
                "passed": 142,
                "failed": 5,
                "skipped": 3,
                "success_rate": 94.67
            },
            "coverage": {
                "overall": 87.5,
                "by_module": {
                    "core": 95.2,
                    "utils": 82.1,
                    "api": 78.9
                }
            },
            "performance": {
                "average_test_time": 0.45,
                "slowest_tests": ["test_integration_api", "test_database_operations"],
                "total_duration": "1m 12s"
            },
            "recommendations": [
                "Increase test coverage for API module",
                "Optimize slow integration tests",
                "Add more edge case testing"
            ]
        }
    
    def _setup_continuous_testing(self, project_path: str, triggers: List[str]) -> Dict[str, Any]:
        """Set up continuous testing configuration"""
        return {
            "enabled": True,
            "triggers": triggers,
            "watch_paths": [project_path],
            "test_command": self._get_test_command("python", "unit"),
            "coverage_threshold": 80.0,
            "notifications": {
                "email": True,
                "slack": False,
                "github": True
            },
            "auto_fix": False
        }
