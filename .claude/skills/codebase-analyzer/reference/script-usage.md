# Helper Script Usage Guide

This document provides detailed usage information for all helper scripts in the codebase-analyzer skill.

## Overview

All scripts are located in the `scripts/` directory and can be run with Python 3.7+.

```bash
cd .claude/skills/codebase-analyzer
python scripts/<script_name>.py <arguments>
```

---

## 1. detect_language.py

**Purpose**: Automatically detect project language and framework.

### Usage

```bash
python scripts/detect_language.py <project_path>
```

### Examples

```bash
# Detect current directory
python scripts/detect_language.py .

# Detect specific project
python scripts/detect_language.py /path/to/my-project
```

### Output

```json
{
  "project_path": "/path/to/project",
  "project_name": "my-awesome-app",
  "detected_languages": [
    {
      "language": "Rust",
      "config_file": "Cargo.toml",
      "source_dirs": ["src"],
      "test_dirs": ["tests"],
      "extensions": [".rs"],
      "entry_points": ["src/main.rs", "src/lib.rs"],
      "package_manager": "Cargo"
    }
  ],
  "primary_language": "Rust",
  "primary_config": "Cargo.toml"
}
```

### Detection Logic

The script checks for these configuration files in order:

1. **Rust**: `Cargo.toml`
2. **Python**: `pyproject.toml`, `setup.py`, `requirements.txt`
3. **Node.js**: `package.json`
4. **Java**: `pom.xml`, `build.gradle`, `build.gradle.kts`
5. **Go**: `go.mod`
6. **Ruby**: `Gemfile`

If no config file is found, it falls back to analyzing file extensions.

---

## 2. extract_imports.py

**Purpose**: Extract import/dependency statements and exported items from source files.

### Usage

```bash
python scripts/extract_imports.py <file_path>
```

### Examples

```bash
# Python file
python scripts/extract_imports.py src/main.py

# Rust file
python scripts/extract_imports.py src/lib.rs

# JavaScript file
python scripts/extract_imports.py src/index.js
```

### Output

```json
{
  "file": "src/main.rs",
  "file_name": "main.rs",
  "language": "rs",
  "size_bytes": 4567,
  "line_count": 123,
  "imports": [
    "tokio",
    "serde",
    "actix_web"
  ],
  "exports": [
    "main",
    "configure_app",
    "AppState"
  ],
  "import_count": 3,
  "export_count": 3
}
```

### Supported Languages

- **Python** (`.py`): `import`, `from...import`
- **Rust** (`.rs`): `use`, `pub fn/struct/enum/trait`
- **JavaScript/TypeScript** (`.js`, `.ts`, `.jsx`, `.tsx`): ES6 imports, CommonJS `require()`
- **Java/Kotlin** (`.java`, `.kt`): `import`, public classes/interfaces
- **Go** (`.go`): `import`, exported identifiers (capital letter)

### What Gets Extracted

**Imports**: Only external packages (excludes relative imports like `./utils`)

**Exports**:
- Python: Functions and classes
- Rust: `pub` items
- JS/TS: `export` statements
- Java: `public` classes/interfaces
- Go: Capital-letter identifiers

---

## 3. complexity_metrics.py

**Purpose**: Calculate code complexity metrics for quality assessment.

### Usage

```bash
python scripts/complexity_metrics.py <file_path>
```

### Examples

```bash
python scripts/complexity_metrics.py src/core/business_logic.rs
```

### Output

```json
{
  "file": "src/core/business_logic.rs",
  "file_name": "business_logic.rs",
  "language": "rs",
  "size_bytes": 12345,
  "lines": {
    "total": 345,
    "code": 289,
    "blank": 34,
    "comments": 22
  },
  "functions": 12,
  "structs": 5,
  "enums": 2,
  "traits": 1,
  "complexity_estimate": 24,
  "complexity_rating": "Medium",
  "max_nesting": 4
}
```

### Metrics Explained

**Lines**:
- `total`: All lines including blank and comments
- `code`: Actual code lines
- `blank`: Empty lines
- `comments`: Comment-only lines

**Language-Specific Counts**:
- Python: `functions`, `classes`
- Rust: `functions`, `structs`, `enums`, `traits`
- JS/TS: `functions`, `arrow_functions`, `classes`
- Java: `methods`, `classes`, `interfaces`
- Go: `functions`, `types`

**Complexity Estimate**:
Count of control flow keywords (`if`, `for`, `while`, `match`, etc.)
- Low: < 10
- Medium: 10-30
- High: > 30

**Max Nesting**:
Deepest level of brace/indentation nesting (potential maintainability issue if > 5)

---

## 4. parse_structure.py

**Purpose**: Visualize project directory structure with smart filtering.

### Usage

```bash
python scripts/parse_structure.py <project_path> [--tree|--json|--stats]
```

### Output Formats

#### Tree View (default)

```bash
python scripts/parse_structure.py /path/to/project
# or
python scripts/parse_structure.py /path/to/project --tree
```

Output:
```
my-project/
├── src/
│   ├── main.rs (4.5KB)
│   ├── lib.rs (2.3KB)
│   └── utils/
│       ├── helpers.rs (1.2KB)
│       └── config.rs (800B)
├── tests/
│   └── integration_test.rs (3.4KB)
├── Cargo.toml (456B)
└── README.md (2.1KB)
```

#### JSON Structure

```bash
python scripts/parse_structure.py /path/to/project --json
```

Output:
```json
{
  "name": "my-project",
  "path": "/path/to/project",
  "type": "directory",
  "children": [
    {
      "name": "src",
      "path": "src",
      "type": "directory",
      "children": [
        {
          "name": "main.rs",
          "path": "src/main.rs",
          "type": "file",
          "size": 4567,
          "extension": ".rs"
        }
      ]
    }
  ]
}
```

#### Statistics

```bash
python scripts/parse_structure.py /path/to/project --stats
```

Output:
```json
{
  "total_files": 142,
  "total_dirs": 28,
  "files_by_extension": {
    ".rs": 89,
    ".toml": 2,
    ".md": 5,
    ".json": 3
  },
  "largest_files": [
    {
      "path": "src/generator/workflow.rs",
      "size": 45678,
      "size_formatted": "44.6KB"
    }
  ],
  "max_depth": 5
}
```

### Filtering Rules

**Automatically Excluded**:
- Build artifacts: `target/`, `build/`, `dist/`
- Dependencies: `node_modules/`, `__pycache__/`
- Version control: `.git/`, `.svn/`
- IDE files: `.idea/`, `.vscode/`
- Virtual environments: `venv/`, `.venv/`

**Limits**:
- Max depth: 4 levels by default
- Max files per directory: 50 (shows "... (N more files)" if exceeded)

---

## Best Practices

### 1. Pipeline Scripts Together

```bash
# Detect language, then analyze main file
LANG=$(python scripts/detect_language.py . | jq -r '.primary_language')
echo "Detected: $LANG"

# Find entry point
ENTRY=$(python scripts/detect_language.py . | jq -r '.detected_languages[0].entry_points[0]')

# Analyze entry point
python scripts/extract_imports.py "$ENTRY"
python scripts/complexity_metrics.py "$ENTRY"
```

### 2. Use with Claude's Tools

Within a Claude session:
```
1. Run detect_language.py to identify project type
2. Use Glob to find all source files
3. Run extract_imports.py on key files
4. Use Read to examine interesting modules
5. Run complexity_metrics.py to identify complex files
6. Generate analysis report
```

### 3. Error Handling

All scripts return JSON with `"error"` key on failure:
```json
{
  "error": "File does not exist: /invalid/path",
  "suggestion": "Check file path and try again"
}
```

Always check for the `error` key in output.

### 4. Performance Tips

- For large projects (1000+ files), start with `parse_structure.py --stats` to get overview
- Use `extract_imports.py` only on key files, not all files
- Run `complexity_metrics.py` on files flagged as complex first

---

## Integration Examples

### Example 1: Full Project Analysis

```python
import json
import subprocess

def analyze_project(path):
    # Detect language
    detect = subprocess.run(
        ['python', 'scripts/detect_language.py', path],
        capture_output=True, text=True
    )
    info = json.loads(detect.stdout)

    # Get structure
    structure = subprocess.run(
        ['python', 'scripts/parse_structure.py', path, '--stats'],
        capture_output=True, text=True
    )
    stats = json.loads(structure.stdout)

    return {
        'language': info['primary_language'],
        'file_count': stats['total_files'],
        'extensions': stats['files_by_extension']
    }
```

### Example 2: Find Complex Files

```bash
# Find all Rust files and check complexity
for file in $(find src -name "*.rs"); do
    COMPLEXITY=$(python scripts/complexity_metrics.py "$file" | jq -r '.complexity_rating')
    if [ "$COMPLEXITY" = "High" ]; then
        echo "High complexity: $file"
    fi
done
```

---

## Troubleshooting

### Issue: Script not found
**Solution**: Ensure you're in the skill directory or use full path:
```bash
python /full/path/to/.claude/skills/codebase-analyzer/scripts/detect_language.py .
```

### Issue: Permission denied
**Solution**: Make scripts executable:
```bash
chmod +x scripts/*.py
```

### Issue: Invalid JSON output
**Cause**: Script encountered an error
**Solution**: Check the `error` key in output:
```bash
python scripts/detect_language.py . | jq '.error'
```

### Issue: Python not found
**Solution**: Ensure Python 3.7+ is installed:
```bash
python3 --version
# If python3 works, use that instead of python
```
