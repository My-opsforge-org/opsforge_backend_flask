#!/usr/bin/env python3
"""
Test runner script for Go_Tripping Flask Backend
Usage: python run_tests.py [options]
"""

import sys
import subprocess
import argparse
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*50}\n")
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run tests for Go_Tripping Flask Backend')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage report')
    parser.add_argument('--html', action='store_true', help='Generate HTML coverage report')
    parser.add_argument('--parallel', action='store_true', help='Run tests in parallel')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--file', help='Run specific test file')
    parser.add_argument('--class', dest='test_class', help='Run specific test class')
    parser.add_argument('--method', help='Run specific test method')
    parser.add_argument('--marker', help='Run tests with specific marker')
    parser.add_argument('--install-deps', action='store_true', help='Install test dependencies')
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        print("Installing test dependencies...")
        if not run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_test.txt'], 
                          "Installing test dependencies"):
            sys.exit(1)
    
    # Build pytest command
    pytest_cmd = ['pytest']
    
    if args.verbose:
        pytest_cmd.append('-v')
    
    if args.parallel:
        pytest_cmd.extend(['-n', 'auto'])
    
    if args.coverage:
        pytest_cmd.extend(['--cov=app', '--cov=auth', '--cov=community', '--cov=explore'])
        if args.html:
            pytest_cmd.append('--cov-report=html')
        else:
            pytest_cmd.append('--cov-report=term-missing')
    
    if args.unit:
        pytest_cmd.append('tests/unit/')
    elif args.integration:
        pytest_cmd.append('tests/integration/')
    elif args.file:
        pytest_cmd.append(args.file)
    elif args.marker:
        pytest_cmd.extend(['-m', args.marker])
    else:
        pytest_cmd.append('tests/')
    
    if args.test_class:
        pytest_cmd.append(f'::{args.test_class}')
    
    if args.method:
        pytest_cmd.append(f'::{args.method}')
    
    # Run tests
    success = run_command(pytest_cmd, "Running tests")
    
    if success:
        print("\n🎉 All tests passed!")
        if args.coverage and args.html:
            print("\n📊 Coverage report generated in htmlcov/ directory")
            print("Open htmlcov/index.html in your browser to view the report")
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)

if __name__ == '__main__':
    main() 