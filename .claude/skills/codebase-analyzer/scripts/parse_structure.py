#!/usr/bin/env python3
"""
Parse and visualize project directory structure.
Creates a tree view of the project with smart filtering.
"""

import json
import sys
from pathlib import Path


# Common directories to exclude
EXCLUDED_DIRS = {
    '.git', '.svn', '.hg',
    'node_modules', '__pycache__', '.pytest_cache',
    'target', 'build', 'dist', '.next', '.nuxt',
    'venv', 'env', '.venv', '.env',
    '.idea', '.vscode', '.vs',
    'coverage', '.coverage', 'htmlcov'
}

# Common files to exclude
EXCLUDED_FILES = {
    '.DS_Store', 'Thumbs.db', '.gitignore', '.gitkeep',
    'package-lock.json', 'yarn.lock', 'Cargo.lock',
    '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dll', '*.dylib'
}


def should_exclude(path, depth, max_depth=4):
    """Determine if a path should be excluded from the tree."""
    # Depth limit
    if depth > max_depth:
        return True

    # Excluded directories
    if path.is_dir() and path.name in EXCLUDED_DIRS:
        return True

    # Excluded files
    if path.is_file() and path.name in EXCLUDED_FILES:
        return True

    # Hidden files (starting with .)
    if path.name.startswith('.') and path.name not in {'.github', '.gitlab', '.env.example'}:
        return True

    return False


def build_tree(root_path, max_depth=4, max_files_per_dir=50):
    """Build a tree structure of the project."""
    root = Path(root_path).resolve()

    if not root.exists():
        return {'error': f'Path does not exist: {root_path}'}

    tree = {
        'name': root.name,
        'path': str(root),
        'type': 'directory' if root.is_dir() else 'file',
        'children': []
    }

    if root.is_file():
        tree['size'] = root.stat().st_size
        return tree

    def walk_directory(path, depth=0):
        """Recursively walk directory."""
        if depth > max_depth:
            return None

        children = []
        try:
            items = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))

            # Limit files per directory
            file_count = 0
            for item in items:
                if should_exclude(item, depth, max_depth):
                    continue

                if item.is_file():
                    file_count += 1
                    if file_count > max_files_per_dir:
                        children.append({
                            'name': f'... ({len(items) - len(children)} more files)',
                            'type': 'truncated'
                        })
                        break

                child = {
                    'name': item.name,
                    'path': str(item.relative_to(root)),
                    'type': 'directory' if item.is_dir() else 'file'
                }

                if item.is_file():
                    child['size'] = item.stat().st_size
                    child['extension'] = item.suffix

                if item.is_dir():
                    subchildren = walk_directory(item, depth + 1)
                    if subchildren:
                        child['children'] = subchildren

                children.append(child)

        except PermissionError:
            return [{'name': '(Permission denied)', 'type': 'error'}]

        return children

    tree['children'] = walk_directory(root)
    return tree


def tree_to_string(tree, prefix='', is_last=True, show_size=False):
    """Convert tree structure to ASCII art string."""
    if isinstance(tree, dict) and 'error' in tree:
        return tree['error']

    lines = []

    # Root node
    if prefix == '':
        name = tree['name']
        if show_size and 'size' in tree:
            name += f" ({format_size(tree['size'])})"
        lines.append(name + '/')
        prefix = ''
    else:
        # Branch characters
        connector = '└── ' if is_last else '├── '
        name = tree['name']

        if tree['type'] == 'directory':
            name += '/'
        elif show_size and 'size' in tree:
            name += f" ({format_size(tree['size'])})"

        lines.append(prefix + connector + name)

    # Children
    if 'children' in tree and tree['children']:
        extension = '    ' if is_last else '│   '
        child_prefix = prefix + extension

        children = tree['children']
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            if isinstance(child, dict):
                child_lines = tree_to_string(child, child_prefix, is_last_child, show_size)
                lines.append(child_lines)

    return '\n'.join(lines)


def format_size(size_bytes):
    """Format byte size to human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}TB"


def analyze_structure(root_path, max_depth=4):
    """Analyze project structure and return statistics."""
    root = Path(root_path).resolve()

    stats = {
        'total_files': 0,
        'total_dirs': 0,
        'files_by_extension': {},
        'largest_files': [],
        'deepest_path': '',
        'max_depth': 0
    }

    def walk(path, depth=0):
        if depth > max_depth or should_exclude(path, depth, max_depth):
            return

        stats['max_depth'] = max(stats['max_depth'], depth)

        if path.is_file():
            stats['total_files'] += 1
            ext = path.suffix or '(no extension)'
            stats['files_by_extension'][ext] = stats['files_by_extension'].get(ext, 0) + 1

            size = path.stat().st_size
            stats['largest_files'].append({
                'path': str(path.relative_to(root)),
                'size': size,
                'size_formatted': format_size(size)
            })

        elif path.is_dir():
            stats['total_dirs'] += 1
            try:
                for item in path.iterdir():
                    walk(item, depth + 1)
            except PermissionError:
                pass

    walk(root)

    # Sort largest files and keep top 10
    stats['largest_files'].sort(key=lambda x: x['size'], reverse=True)
    stats['largest_files'] = stats['largest_files'][:10]

    return stats


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Usage: parse_structure.py <project_path> [--json|--stats|--tree]',
            'examples': [
                'python parse_structure.py /path/to/project',
                'python parse_structure.py /path/to/project --tree',
                'python parse_structure.py /path/to/project --json',
                'python parse_structure.py /path/to/project --stats'
            ]
        }, indent=2))
        sys.exit(1)

    project_path = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else '--tree'

    if output_format == '--json':
        # Output full JSON tree
        tree = build_tree(project_path)
        print(json.dumps(tree, indent=2))

    elif output_format == '--stats':
        # Output statistics
        stats = analyze_structure(project_path)
        print(json.dumps(stats, indent=2))

    else:  # --tree (default)
        # Output ASCII tree
        tree = build_tree(project_path)
        print(tree_to_string(tree, show_size=True))


if __name__ == '__main__':
    main()
