#!/usr/bin/env python3
"""
Build dependency graph from source code.
Analyzes import/use/require statements to create a directed graph.
"""

import json
import sys
import re
from pathlib import Path
from collections import defaultdict


def extract_imports_rust(content):
    """Extract Rust use statements."""
    imports = []
    pattern = r'use\s+(?:crate::)?([^;{]+)'
    for match in re.finditer(pattern, content):
        import_path = match.group(1).strip()
        # Parse module path
        parts = import_path.split('::')
        if parts[0] not in ['std', 'core', 'alloc']:
            imports.append(parts[0])
    return list(set(imports))


def extract_imports_python(content):
    """Extract Python imports."""
    imports = []
    # from foo import bar
    pattern1 = r'from\s+(\S+)\s+import'
    for match in re.finditer(pattern1, content):
        module = match.group(1).split('.')[0]
        imports.append(module)

    # import foo
    pattern2 = r'^import\s+(\S+)'
    for match in re.finditer(pattern2, content, re.MULTILINE):
        module = match.group(1).split('.')[0]
        imports.append(module)

    return list(set(imports))


def extract_imports_js(content):
    """Extract JavaScript/TypeScript imports."""
    imports = []
    # import ... from 'module'
    pattern = r"import\s+.+\s+from\s+['\"]([^'\"]+)['\"]"
    for match in re.finditer(pattern, content):
        module = match.group(1)
        # Only internal imports (start with . or /)
        if module.startswith('.') or module.startswith('/'):
            # Resolve to module name
            parts = module.split('/')
            module_name = parts[-1].replace('.js', '').replace('.ts', '')
            imports.append(module_name)

    return list(set(imports))


def get_module_name(file_path, root_path):
    """Get module name from file path."""
    rel_path = file_path.relative_to(root_path)
    # Remove extension
    module = str(rel_path.with_suffix(''))
    # Convert path separators to module separators
    module = module.replace('/', '::').replace('\\', '::')
    return module


def build_graph(project_path, include_tests=False, max_depth=None):
    """Build dependency graph for project."""
    root = Path(project_path).resolve()

    if not root.exists():
        return {'error': f'Path does not exist: {project_path}'}

    # Detect language
    if (root / 'Cargo.toml').exists():
        language = 'rust'
        source_dir = root / 'src'
        extensions = ['.rs']
        extractor = extract_imports_rust
    elif (root / 'package.json').exists():
        language = 'javascript'
        source_dir = root / 'src' if (root / 'src').exists() else root
        extensions = ['.js', '.ts', '.jsx', '.tsx']
        extractor = extract_imports_js
    elif (root / 'pyproject.toml').exists() or (root / 'setup.py').exists():
        language = 'python'
        source_dir = root / 'src' if (root / 'src').exists() else root
        extensions = ['.py']
        extractor = extract_imports_python
    else:
        return {'error': 'Could not detect project language'}

    # Find all source files
    source_files = []
    for ext in extensions:
        source_files.extend(source_dir.rglob(f'*{ext}'))

    # Filter out tests if requested
    if not include_tests:
        source_files = [
            f for f in source_files
            if not ('test' in str(f) or 'spec' in str(f))
        ]

    # Build graph
    nodes = []
    edges = []
    module_to_file = {}

    for file_path in source_files:
        module_name = get_module_name(file_path, source_dir)
        module_to_file[module_name] = str(file_path.relative_to(root))

        # Determine node type
        if file_path.name in ['main.rs', 'main.py', 'index.js', 'index.ts']:
            node_type = 'entry'
        elif 'test' in str(file_path) or 'spec' in str(file_path):
            node_type = 'test'
        else:
            node_type = 'module'

        nodes.append({
            'id': module_name,
            'file': str(file_path.relative_to(root)),
            'type': node_type
        })

        # Extract imports
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            imports = extractor(content)

            for imp in imports:
                # Try to match import to actual module
                # Simple heuristic: look for module with matching name
                matching_modules = [
                    m for m in module_to_file.keys()
                    if imp in m
                ]

                for target in matching_modules:
                    edges.append({
                        'from': module_name,
                        'to': target,
                        'type': 'import'
                    })
        except Exception as e:
            # Skip files that can't be read
            pass

    # Build result
    result = {
        'language': language,
        'project_path': str(root),
        'nodes': nodes,
        'edges': edges,
        'statistics': {
            'total_modules': len(nodes),
            'total_dependencies': len(edges),
            'entry_points': len([n for n in nodes if n['type'] == 'entry']),
            'test_modules': len([n for n in nodes if n['type'] == 'test'])
        }
    }

    return result


def detect_cycles(graph):
    """Detect circular dependencies using DFS."""
    edges = graph.get('edges', [])

    # Build adjacency list
    adj = defaultdict(list)
    for edge in edges:
        adj[edge['from']].append(edge['to'])

    visited = set()
    rec_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path[:])
            elif neighbor in rec_stack:
                # Found cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)

        rec_stack.remove(node)

    for node in [n['id'] for n in graph.get('nodes', [])]:
        if node not in visited:
            dfs(node, [])

    return cycles


def calculate_metrics(graph):
    """Calculate graph metrics."""
    nodes = {n['id']: n for n in graph.get('nodes', [])}
    edges = graph.get('edges', [])

    # Calculate fan-in and fan-out
    fan_in = defaultdict(int)
    fan_out = defaultdict(int)

    for edge in edges:
        fan_out[edge['from']] += 1
        fan_in[edge['to']] += 1

    # Add metrics to nodes
    for node_id, node in nodes.items():
        node['fan_in'] = fan_in.get(node_id, 0)
        node['fan_out'] = fan_out.get(node_id, 0)
        node['coupling'] = fan_in.get(node_id, 0) + fan_out.get(node_id, 0)

    return list(nodes.values())


def generate_mermaid(graph):
    """Generate Mermaid diagram from graph."""
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])

    lines = ['graph TD']

    # Add nodes
    for node in nodes[:50]:  # Limit to 50 nodes for readability
        node_id = node['id'].replace('::', '_').replace('/', '_')
        label = node['id'].split('::')[-1]  # Just the last part

        if node['type'] == 'entry':
            lines.append(f'    {node_id}[{label}]:::entry')
        else:
            lines.append(f'    {node_id}[{label}]')

    # Add edges
    for edge in edges[:100]:  # Limit edges
        from_id = edge['from'].replace('::', '_').replace('/', '_')
        to_id = edge['to'].replace('::', '_').replace('/', '_')
        lines.append(f'    {from_id} --> {to_id}')

    # Add styling
    lines.append('')
    lines.append('    classDef entry fill:#e1f5ff,stroke:#01579b')

    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Usage: build_dependency_graph.py <project_path> [options]',
            'options': {
                '--include-tests': 'Include test files',
                '--output': 'Output file path',
                '--format': 'Output format: json|mermaid'
            }
        }, indent=2))
        sys.exit(1)

    project_path = sys.argv[1]
    include_tests = '--include-tests' in sys.argv
    output_file = None
    output_format = 'json'

    # Parse options
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    if '--format' in sys.argv:
        idx = sys.argv.index('--format')
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]

    # Build graph
    graph = build_graph(project_path, include_tests=include_tests)

    if 'error' in graph:
        print(json.dumps(graph, indent=2))
        sys.exit(1)

    # Detect cycles
    cycles = detect_cycles(graph)
    if cycles:
        graph['circular_dependencies'] = [' → '.join(c) for c in cycles]

    # Calculate metrics
    graph['nodes'] = calculate_metrics(graph)

    # Output
    if output_format == 'mermaid':
        output = generate_mermaid(graph)
    else:
        output = json.dumps(graph, indent=2)

    if output_file:
        Path(output_file).write_text(output)
        print(f'Output written to {output_file}')
    else:
        print(output)


if __name__ == '__main__':
    main()
