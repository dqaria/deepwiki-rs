#!/usr/bin/env python3
"""
Calculate code complexity metrics for source files.
Provides: LOC, nesting depth, cyclomatic complexity estimate, function count
"""

import json
import re
import sys
from pathlib import Path


def analyze_python(content):
    """Analyze Python code metrics."""
    lines = content.split('\n')

    # Count function and class definitions
    functions = len(re.findall(r'^\s*def\s+\w+', content, re.MULTILINE))
    classes = len(re.findall(r'^\s*class\s+\w+', content, re.MULTILINE))

    # Estimate complexity by counting control flow statements
    complexity_keywords = ['if', 'elif', 'for', 'while', 'except', 'and', 'or']
    complexity = sum(content.count(f' {kw} ') + content.count(f'\n{kw} ') for kw in complexity_keywords)

    # Calculate max nesting (approximate via indentation)
    max_indent = 0
    for line in lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            max_indent = max(max_indent, indent // 4)  # Assuming 4-space indent

    return {
        'functions': functions,
        'classes': classes,
        'complexity_estimate': complexity,
        'max_nesting': max_indent
    }


def analyze_rust(content):
    """Analyze Rust code metrics."""
    # Count functions, structs, enums, traits
    functions = len(re.findall(r'\bfn\s+\w+', content))
    structs = len(re.findall(r'\bstruct\s+\w+', content))
    enums = len(re.findall(r'\benum\s+\w+', content))
    traits = len(re.findall(r'\btrait\s+\w+', content))

    # Complexity: control flow keywords
    complexity_keywords = ['if', 'match', 'for', 'while', 'loop']
    complexity = sum(content.count(f' {kw} ') + content.count(f'\n{kw} ') for kw in complexity_keywords)

    # Nesting (count brace depth)
    max_depth = 0
    current_depth = 0
    for char in content:
        if char == '{':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == '}':
            current_depth -= 1

    return {
        'functions': functions,
        'structs': structs,
        'enums': enums,
        'traits': traits,
        'complexity_estimate': complexity,
        'max_nesting': max_depth
    }


def analyze_javascript(content):
    """Analyze JavaScript/TypeScript code metrics."""
    # Count functions (various styles)
    functions = len(re.findall(r'\bfunction\s+\w+', content))
    arrow_functions = len(re.findall(r'=>', content))
    classes = len(re.findall(r'\bclass\s+\w+', content))

    # Complexity
    complexity_keywords = ['if', 'else if', 'for', 'while', 'switch', '&&', '||', '?']
    complexity = sum(content.count(kw) for kw in complexity_keywords)

    # Nesting (brace depth)
    max_depth = 0
    current_depth = 0
    for char in content:
        if char == '{':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == '}':
            current_depth -= 1

    return {
        'functions': functions + arrow_functions,
        'arrow_functions': arrow_functions,
        'classes': classes,
        'complexity_estimate': complexity,
        'max_nesting': max_depth
    }


def analyze_java(content):
    """Analyze Java code metrics."""
    # Count methods and classes
    methods = len(re.findall(r'\b(?:public|private|protected)\s+(?:static\s+)?\w+\s+\w+\s*\(', content))
    classes = len(re.findall(r'\bclass\s+\w+', content))
    interfaces = len(re.findall(r'\binterface\s+\w+', content))

    # Complexity
    complexity_keywords = ['if', 'else if', 'for', 'while', 'switch', '&&', '||', '?']
    complexity = sum(content.count(kw) for kw in complexity_keywords)

    # Nesting
    max_depth = 0
    current_depth = 0
    for char in content:
        if char == '{':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == '}':
            current_depth -= 1

    return {
        'methods': methods,
        'classes': classes,
        'interfaces': interfaces,
        'complexity_estimate': complexity,
        'max_nesting': max_depth
    }


def analyze_go(content):
    """Analyze Go code metrics."""
    # Count functions and types
    functions = len(re.findall(r'\bfunc\s+(?:\(\w+\s+\*?\w+\)\s+)?\w+', content))
    types = len(re.findall(r'\btype\s+\w+', content))

    # Complexity
    complexity_keywords = ['if', 'for', 'switch', 'select']
    complexity = sum(content.count(f' {kw} ') + content.count(f'\n{kw} ') for kw in complexity_keywords)

    # Nesting
    max_depth = 0
    current_depth = 0
    for char in content:
        if char == '{':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == '}':
            current_depth -= 1

    return {
        'functions': functions,
        'types': types,
        'complexity_estimate': complexity,
        'max_nesting': max_depth
    }


def calculate_metrics(file_path):
    """Calculate metrics for a source file."""
    path = Path(file_path)

    if not path.exists():
        return {'error': f'File does not exist: {file_path}'}

    if not path.is_file():
        return {'error': f'Path is not a file: {file_path}'}

    # Read content
    try:
        content = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return {'error': f'Could not read file: {str(e)}'}

    lines = content.split('\n')

    # Basic metrics
    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if not line.strip())
    comment_lines = sum(1 for line in lines if line.strip().startswith(('#', '//', '/*', '*')))
    code_lines = total_lines - blank_lines - comment_lines

    # Language-specific analysis
    analyzers = {
        '.py': analyze_python,
        '.rs': analyze_rust,
        '.js': analyze_javascript,
        '.jsx': analyze_javascript,
        '.ts': analyze_javascript,
        '.tsx': analyze_javascript,
        '.java': analyze_java,
        '.kt': analyze_java,
        '.go': analyze_go,
    }

    analyzer = analyzers.get(path.suffix.lower())
    language_metrics = analyzer(content) if analyzer else {}

    # Compile result
    result = {
        'file': str(path),
        'file_name': path.name,
        'language': path.suffix[1:],
        'size_bytes': path.stat().st_size,
        'lines': {
            'total': total_lines,
            'code': code_lines,
            'blank': blank_lines,
            'comments': comment_lines
        },
        **language_metrics
    }

    # Add complexity rating
    if 'complexity_estimate' in result:
        complexity = result['complexity_estimate']
        if complexity < 10:
            rating = 'Low'
        elif complexity < 30:
            rating = 'Medium'
        else:
            rating = 'High'
        result['complexity_rating'] = rating

    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Usage: complexity_metrics.py <file_path>',
            'example': 'python complexity_metrics.py src/main.rs'
        }, indent=2))
        sys.exit(1)

    file_path = sys.argv[1]
    result = calculate_metrics(file_path)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
