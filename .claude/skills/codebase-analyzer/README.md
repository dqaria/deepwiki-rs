# Codebase Analyzer Skill

A Claude AI skill for analyzing codebases without external dependencies.

## What is This?

This is a **Claude Agent Skill** that enables Claude to systematically analyze software projects and understand:
- Project structure and organization
- Programming languages and frameworks
- Dependencies and relationships
- Code complexity and quality
- Architecture patterns

## Key Features

✅ **Zero Binary Dependencies** - Pure Python scripts + Claude's native tools
✅ **Multi-Language Support** - Rust, Python, JavaScript, TypeScript, Java, Go, and more
✅ **Lightweight** - < 100KB total (vs ~50MB for compiled tools)
✅ **Transparent** - All analysis steps visible to user
✅ **Customizable** - Easy to modify prompts and scripts

## Quick Start

### Installation

1. **Copy to Claude skills directory**:
   ```bash
   cp -r codebase-analyzer ~/.claude/skills/
   ```

2. **Make scripts executable** (optional):
   ```bash
   chmod +x ~/.claude/skills/codebase-analyzer/scripts/*.py
   ```

3. **Enable in Claude Code**:
   - Ensure `"Skill"` is in your `allowed_tools` configuration

### Usage

Just ask Claude to analyze a codebase:

```
User: "Analyze this Rust project"
User: "What does this codebase do?"
User: "Explain the architecture of this project"
```

Claude will automatically activate this skill and provide structured analysis.

## What Gets Analyzed

### Project Level
- Primary programming language(s)
- Frameworks and build tools
- Project configuration
- Directory structure

### Code Level
- Import/dependency statements
- Exported functions and classes
- Code complexity metrics
- Interface definitions

### Architecture Level
- Module relationships
- Design patterns
- Entry points
- Data flow

## File Structure

```
codebase-analyzer/
├── SKILL.md                 # Main skill definition (loaded by Claude)
├── README.md               # This file
├── scripts/                # Helper utilities
│   ├── detect_language.py      # Language/framework detection
│   ├── extract_imports.py      # Dependency extraction
│   ├── complexity_metrics.py   # Code quality metrics
│   └── parse_structure.py      # Directory tree parsing
└── reference/              # Documentation (loaded on-demand)
    ├── script-usage.md         # Detailed script documentation
    └── language-patterns.md    # Language-specific patterns
```

## How It Works

### Progressive Analysis

1. **Discovery** (Quick)
   - Detect project type via config files
   - Scan directory structure
   - Identify key modules

2. **Analysis** (Medium)
   - Extract imports from key files
   - Calculate complexity metrics
   - Map dependencies

3. **Synthesis** (Detailed)
   - Understand architecture
   - Identify patterns
   - Generate documentation

### Skill Activation

Claude automatically activates this skill when you ask questions like:
- "Analyze this codebase"
- "What is the structure of this project?"
- "How does this code work?"
- "Extract dependencies from this repo"

## Supported Languages

| Language | Detection | Imports | Exports | Metrics |
|----------|-----------|---------|---------|---------|
| Rust | ✅ | ✅ | ✅ | ✅ |
| Python | ✅ | ✅ | ✅ | ✅ |
| JavaScript | ✅ | ✅ | ✅ | ✅ |
| TypeScript | ✅ | ✅ | ✅ | ✅ |
| Java | ✅ | ✅ | ✅ | ✅ |
| Kotlin | ✅ | ✅ | ✅ | ✅ |
| Go | ✅ | ✅ | ✅ | ✅ |
| Ruby | ✅ | ⚠️ | ⚠️ | ⚠️ |
| PHP | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

✅ Full support | ⚠️ Partial support | ❌ Not supported

## Examples

### Example 1: Analyze Rust Project

```
User: "Analyze the current Rust project"

Claude: I'll analyze this Rust project using the codebase-analyzer skill.

[Runs detect_language.py]
Detected: Rust project with Cargo

[Scans src/ directory]
Found 45 Rust source files

[Analyzes main.rs and lib.rs]
Entry point: src/main.rs
Library exports: User, Transaction, Config

[Extracts dependencies from Cargo.toml]
Dependencies: tokio, serde, actix-web

[Generates summary]
This is a web API project built with Actix-web...
```

### Example 2: Get Project Statistics

```
User: "How many lines of code in this project?"

Claude: [Uses parse_structure.py --stats]

Statistics:
- Total files: 142
- Rust files: 89
- Total lines: ~12,500
- Largest file: src/generator/workflow.rs (456 lines)
```

## Customization

### Modify Analysis Workflow

Edit `SKILL.md` to change how Claude approaches analysis:

```markdown
## Analysis Workflow

### Phase 1: Quick Scan
[Your custom instructions]

### Phase 2: Deep Dive
[Your custom instructions]
```

### Add Language Support

Add patterns to `reference/language-patterns.md` and update scripts.

### Adjust Filtering

Edit `scripts/parse_structure.py` to change excluded directories:

```python
EXCLUDED_DIRS = {
    '.git', 'node_modules', 'target',
    # Add your exclusions
}
```

## Performance

### Benchmarks

| Project Size | Analysis Time | Token Usage |
|--------------|---------------|-------------|
| Small (< 100 files) | 30-60s | ~5K tokens |
| Medium (100-500) | 1-3 min | ~15K tokens |
| Large (500-1000) | 3-5 min | ~30K tokens |

*Times are estimates and depend on Claude model and API response time*

### Optimization Tips

1. **Start broad**: Get overview before deep dive
2. **Use caching**: Store results in conversation context
3. **Selective analysis**: Focus on key modules, not all files
4. **Progressive depth**: Increase detail only when needed

## Integration with Other Skills

This skill works well with:

- **architecture-documenter**: Generate C4 documentation from analysis
- **dependency-visualizer**: Create interactive dependency graphs
- **code-reviewer**: Identify code quality issues
- **test-generator**: Suggest test cases based on structure

## Troubleshooting

### Skill not activating?

**Check**:
1. Skill is in `~/.claude/skills/`
2. `SKILL.md` has correct YAML frontmatter
3. `"Skill"` is in allowed_tools
4. Your request matches the "When to Use" patterns

### Scripts failing?

**Ensure**:
1. Python 3.7+ is installed
2. Scripts are executable (`chmod +x scripts/*.py`)
3. Running from project root or using full paths

### Analysis incomplete?

**Try**:
1. Ask more specific questions
2. Request analysis of specific modules
3. Increase context by reading more files

## Contributing

To improve this skill:

1. Add more language support in scripts
2. Enhance pattern matching in `language-patterns.md`
3. Add examples to `SKILL.md`
4. Improve error handling

## License

This skill is part of the deepwiki-rs project analysis tools.

## Related Projects

- **deepwiki-rs**: Full-featured documentation generator (Rust)
- **architecture-documenter**: C4 documentation skill
- **dependency-visualizer**: Graph visualization skill

---

**Version**: 1.0.0
**Last Updated**: 2025-01
**Requires**: Claude Code, Python 3.7+
