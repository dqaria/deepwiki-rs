#!/usr/bin/env python3
"""
Extract imports, dependencies, and exports from source files.
Supports: Python, Rust, JavaScript, TypeScript, Java, Go
"""

import json
import re
import sys
from pathlib import Path


def extract_python_imports(content):
    """Extract Python import statements."""
    imports = []
    exports = []

    # Match: import foo, from foo import bar
    import_pattern = r'^(?:from\s+(\S+)\s+)?import\s+(.+?)(?:\s+as\s+\S+)?$'
    for match in re.finditer(import_pattern, content, re.MULTILINE):
        module = match.group(1) if match.group(1) else match.group(2).split(',')[0].strip()
        base_module = module.split('.')[0]
        if base_module:
            imports.append(base_module)

    # Find exports (functions/classes that might be exported)
    # Look for: def function_name, class ClassName
    export_pattern = r'^(?:def|class)\s+(\w+)'
    for match in re.finditer(export_pattern, content, re.MULTILINE):
        exports.append(match.group(1))

    return {
        'imports': list(set(imports)),
        'exports': exports[:20]  # Limit to first 20
    }


def extract_rust_imports(content):
    """Extract Rust use statements and pub items."""
    imports = []
    exports = []

    # Match: use foo::bar;
    use_pattern = r'use\s+([^;]+);'
    for match in re.finditer(use_pattern, content, re.MULTILINE):
        parts = match.group(1).split('::')
        # Filter out std/core/alloc/crate/self/super
        if parts[0] not in ['std', 'core', 'alloc', 'crate', 'self', 'super']:
            imports.append(parts[0])

    # Find public items: pub fn, pub struct, pub enum, pub trait
    export_pattern = r'pub\s+(?:fn|struct|enum|trait|const|static)\s+(\w+)'
    for match in re.finditer(export_pattern, content, re.MULTILINE):
        exports.append(match.group(1))

    return {
        'imports': list(set(imports)),
        'exports': exports[:20]
    }


def extract_js_imports(content):
    """Extract JavaScript/TypeScript imports and exports."""
    imports = []
    exports = []

    # ES6 imports: import { foo } from 'bar'
    import_pattern = r"import\s+(?:{[^}]+}|\*\s+as\s+\w+|\w+)\s+from\s+['\"]([^'\"]+)['\"]"
    for match in re.finditer(import_pattern, content):
        module = match.group(1)
        # External packages don't start with . or /
        if not module.startswith(('.', '/')):
            base_module = module.split('/')[0]
            imports.append(base_module)

    # CommonJS: require('bar')
    require_pattern = r"require\(['\"]([^'\"]+)['\"]\)"
    for match in re.finditer(require_pattern, content):
        module = match.group(1)
        if not module.startswith(('.', '/')):
            base_module = module.split('/')[0]
            imports.append(base_module)

    # Exports: export function, export class, export const
    export_pattern = r'export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)'
    for match in re.finditer(export_pattern, content):
        exports.append(match.group(1))

    # Named exports: export { foo, bar }
    named_export_pattern = r'export\s+{([^}]+)}'
    for match in re.finditer(named_export_pattern, content):
        names = [n.strip().split(' as ')[0] for n in match.group(1).split(',')]
        exports.extend(names)

    return {
        'imports': list(set(imports)),
        'exports': list(set(exports))[:20]
    }


def extract_java_imports(content):
    """Extract Java import statements and public classes."""
    imports = []
    exports = []

    # Match: import foo.bar.Baz;
    import_pattern = r'import\s+(?:static\s+)?([^;]+);'
    for match in re.finditer(import_pattern, content, re.MULTILINE):
        parts = match.group(1).split('.')
        # Get package name (everything except last part which is class)
        if len(parts) > 1:
            package = parts[0]
            # Filter out java.* and javax.*
            if package not in ['java', 'javax']:
                imports.append(package)

    # Find public classes, interfaces, enums
    export_pattern = r'public\s+(?:class|interface|enum)\s+(\w+)'
    for match in re.finditer(export_pattern, content, re.MULTILINE):
        exports.append(match.group(1))

    return {
        'imports': list(set(imports)),
        'exports': exports
    }


def extract_go_imports(content):
    """Extract Go import statements and exported identifiers."""
    imports = []
    exports = []

    # Single import: import "foo/bar"
    single_import = r'import\s+"([^"]+)"'
    for match in re.finditer(single_import, content):
        package = match.group(1).split('/')[0]
        imports.append(package)

    # Multiple imports: import ( "foo" "bar" )
    multi_import = r'import\s+\((.*?)\)'
    for match in re.finditer(multi_import, content, re.DOTALL):
        for line in match.group(1).split('\n'):
            pkg_match = re.search(r'"([^"]+)"', line)
            if pkg_match:
                package = pkg_match.group(1).split('/')[0]
                imports.append(package)

    # Exported identifiers start with capital letter
    # func ExportedFunc, type ExportedType, const ExportedConst
    export_pattern = r'(?:func|type|const|var)\s+([A-Z]\w*)'
    for match in re.finditer(export_pattern, content, re.MULTILINE):
        exports.append(match.group(1))

    return {
        'imports': list(set(imports)),
        'exports': list(set(exports))[:20]
    }


def extract_imports(file_path):
    """Main entry point to extract imports and exports."""
    path = Path(file_path)

    if not path.exists():
        return {'error': f'File does not exist: {file_path}'}

    if not path.is_file():
        return {'error': f'Path is not a file: {file_path}'}

    # Read file content
    try:
        content = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return {'error': f'Could not read file: {str(e)}'}

    # Language-specific extractors
    extractors = {
        '.py': extract_python_imports,
        '.rs': extract_rust_imports,
        '.js': extract_js_imports,
        '.jsx': extract_js_imports,
        '.ts': extract_js_imports,
        '.tsx': extract_js_imports,
        '.java': extract_java_imports,
        '.kt': extract_java_imports,  # Kotlin similar to Java
        '.go': extract_go_imports,
    }

    extractor = extractors.get(path.suffix.lower())
    if not extractor:
        return {
            'error': f'Unsupported file type: {path.suffix}',
            'supported_types': list(extractors.keys())
        }

    # Extract imports and exports
    result = extractor(content)

    # Add metadata
    result.update({
        'file': str(path),
        'file_name': path.name,
        'language': path.suffix[1:],
        'size_bytes': path.stat().st_size,
        'line_count': content.count('\n') + 1,
        'import_count': len(result['imports']),
        'export_count': len(result['exports'])
    })

    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Usage: extract_imports.py <file_path>',
            'example': 'python extract_imports.py src/main.rs',
            'supported_languages': ['Python', 'Rust', 'JavaScript', 'TypeScript', 'Java', 'Kotlin', 'Go']
        }, indent=2))
        sys.exit(1)

    file_path = sys.argv[1]
    result = extract_imports(file_path)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
