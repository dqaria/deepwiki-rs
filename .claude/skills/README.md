# Claude Agent Skills for Code Analysis & Documentation

A comprehensive suite of skills for analyzing codebases and generating professional documentation - **without requiring any binary dependencies**.

---

## 🎯 Overview

This skills ecosystem provides:
- **Codebase Analysis** - Understand project structure and dependencies
- **Architecture Documentation** - Generate C4 model documentation
- **Dependency Visualization** - Map code relationships and find issues
- **Multi-Language Support** - Create localized documentation

**Total Size**: ~150KB (vs ~50MB for binary tools)
**Dependencies**: Python 3.7+ (included in most systems)
**Platforms**: Cross-platform (Linux, macOS, Windows)

---

## 📦 Skills Included

### 1. codebase-analyzer
**Purpose**: Analyze source code structure, dependencies, and complexity

**Capabilities**:
- Detects 9+ programming languages
- Extracts imports and exports
- Calculates complexity metrics
- Parses project structure

**Use When**:
- "Analyze this codebase"
- "What does this project do?"
- "Extract dependencies"

[📖 Full Documentation](./codebase-analyzer/SKILL.md)

---

### 2. architecture-documenter
**Purpose**: Generate C4 architecture documentation with Mermaid diagrams

**Capabilities**:
- Creates 4-level C4 documentation
- Generates Mermaid diagrams
- Documents design decisions
- Produces professional tech docs

**Use When**:
- "Generate architecture documentation"
- "Create C4 diagrams"
- "Document the system design"

[📖 Full Documentation](./architecture-documenter/SKILL.md)

---

### 3. code-relationship-mapper
**Purpose**: Visualize dependencies and identify architectural issues

**Capabilities**:
- Creates dependency graphs
- Detects circular dependencies
- Calculates coupling metrics
- Identifies architectural layers

**Use When**:
- "Show me the dependency graph"
- "Find circular dependencies"
- "Visualize module relationships"

[📖 Full Documentation](./code-relationship-mapper/SKILL.md)

---

### 4. multi-language-doc-generator
**Purpose**: Translate documentation to 8 languages

**Capabilities**:
- Supports 8 languages (CN, JP, KR, DE, FR, RU, VN)
- Preserves code blocks and technical terms
- Maintains Markdown structure
- Cultural adaptation

**Use When**:
- "Translate docs to Chinese"
- "Generate Japanese version"
- "Create multi-language documentation"

[📖 Full Documentation](./multi-language-doc-generator/SKILL.md)

---

## 🔄 How Skills Work Together

### Workflow 1: Complete Documentation Pipeline

```
User: "Analyze this project and create full documentation in English and Chinese"

┌─────────────────────────────────────┐
│ 1. codebase-analyzer                │
│    - Detect language (Rust)         │
│    - Extract dependencies           │
│    - Calculate complexity           │
│    - Output: analysis.json          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. architecture-documenter          │
│    - Create C4 Level 1-4            │
│    - Generate Mermaid diagrams      │
│    - Document architecture          │
│    - Output: docs/ (English)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. multi-language-doc-generator     │
│    - Translate to Chinese           │
│    - Preserve code examples         │
│    - Adapt culturally               │
│    - Output: docs/zh/               │
└─────────────────────────────────────┘
```

### Workflow 2: Dependency Analysis

```
User: "Find circular dependencies and create a visual map"

┌─────────────────────────────────────┐
│ 1. codebase-analyzer                │
│    - Extract all imports            │
│    - Build module list              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. code-relationship-mapper         │
│    - Build dependency graph         │
│    - Detect cycles                  │
│    - Calculate metrics              │
│    - Generate Mermaid diagram       │
└─────────────────────────────────────┘
```

### Workflow 3: Quick Overview

```
User: "Give me a quick overview of this project in Japanese"

┌─────────────────────────────────────┐
│ 1. codebase-analyzer (quick mode)   │
│    - Detect language & framework    │
│    - Read README                    │
│    - Scan structure                 │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. multi-language-doc-generator     │
│    - Translate summary              │
│    - Generate Japanese README       │
└─────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone or copy skills to Claude directory
cp -r .claude/skills ~/.claude/

# Make scripts executable
chmod +x ~/.claude/skills/*/scripts/*.py

# Verify Python is available
python3 --version  # Should be 3.7+
```

### Usage

Just ask Claude naturally:

```
"Analyze this Rust project"
→ Activates codebase-analyzer

"Create architecture documentation"
→ Activates architecture-documenter

"Show dependency graph"
→ Activates code-relationship-mapper

"Translate to Chinese"
→ Activates multi-language-doc-generator
```

Claude automatically:
1. Detects which skill(s) to use
2. Chains skills together if needed
3. Generates comprehensive output

---

## 📊 Supported Languages

### Programming Languages (Analysis)

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

### Documentation Languages (Translation)

| Language | Status | Native Name |
|----------|--------|-------------|
| English | ✅ Source | English |
| Chinese | ✅ Full | 简体中文 |
| Japanese | ✅ Full | 日本語 |
| Korean | ✅ Full | 한국어 |
| German | ✅ Full | Deutsch |
| French | ✅ Full | Français |
| Russian | ✅ Full | Русский |
| Vietnamese | ✅ Full | Tiếng Việt |

---

## 💡 Use Cases

### For Developers

**Onboarding to New Codebase**:
```
"Analyze this project and explain the architecture"
→ Get structure, dependencies, and documentation
```

**Refactoring**:
```
"Find circular dependencies and tightly coupled modules"
→ Identify problem areas to refactor
```

**Documentation**:
```
"Generate C4 documentation for this microservice"
→ Create professional architecture docs
```

### For Tech Leads

**Architecture Review**:
```
"Analyze the architecture and identify issues"
→ Get dependency graph, complexity metrics, and recommendations
```

**Team Knowledge Sharing**:
```
"Create documentation in English, Chinese, and Japanese"
→ Support international teams
```

### For Open Source Maintainers

**Multi-Language README**:
```
"Translate README to all supported languages"
→ Reach global audience
```

**Architecture Documentation**:
```
"Generate C4 diagrams and architecture docs"
→ Help contributors understand the project
```

---

## 🎯 Comparison with deepwiki-rs Binary

| Aspect | Skills Suite | deepwiki-rs Binary |
|--------|-------------|-------------------|
| **Size** | ~150KB | ~50MB |
| **Installation** | Copy files | Compile/Download |
| **Dependencies** | Python 3 (built-in) | Rust compiler + libs |
| **Customization** | Edit Markdown | Modify Rust code |
| **Transparency** | Every step visible | Black box |
| **Cost** | Claude session only | Extra LLM API calls |
| **Platform** | Cross-platform | Compile per platform |
| **Maintenance** | Edit text files | Rust expertise needed |
| **Speed** | Real-time analysis | Batch processing (faster) |
| **Flexibility** | Highly composable | Fixed pipeline |

**When to Use Skills Suite**:
- ✅ Want transparency and control
- ✅ Need customization
- ✅ Prefer lightweight tools
- ✅ Interactive exploration

**When to Use Binary**:
- ✅ Batch processing many projects
- ✅ Need maximum speed
- ✅ Want standalone tool
- ✅ Offline usage required

**Best of Both Worlds**:
Use skills for exploration and customization, then use deepwiki-rs binary for automated CI/CD pipelines.

---

## 📁 Directory Structure

```
.claude/skills/
├── README.md                          # This file
│
├── codebase-analyzer/
│   ├── SKILL.md                       # Main skill definition
│   ├── README.md                      # Usage guide
│   ├── EXAMPLES.md                    # Usage examples
│   ├── scripts/
│   │   ├── detect_language.py         # Language detection
│   │   ├── extract_imports.py         # Import extraction
│   │   ├── complexity_metrics.py      # Metrics calculation
│   │   └── parse_structure.py         # Structure parsing
│   └── reference/
│       ├── script-usage.md            # Script documentation
│       └── language-patterns.md       # Language patterns
│
├── architecture-documenter/
│   ├── SKILL.md                       # Main skill definition
│   └── templates/
│       ├── c4-context.md              # C4 Level 1 template
│       ├── c4-container.md            # C4 Level 2 template
│       ├── c4-component.md            # C4 Level 3 template
│       └── mermaid-patterns.md        # Diagram patterns
│
├── code-relationship-mapper/
│   ├── SKILL.md                       # Main skill definition
│   ├── scripts/
│   │   ├── build_dependency_graph.py  # Graph builder
│   │   ├── detect_cycles.py           # Cycle detection
│   │   └── calculate_metrics.py       # Metrics
│   └── templates/
│       └── graph-styles.md            # Styling options
│
└── multi-language-doc-generator/
    ├── SKILL.md                       # Main skill definition
    └── locales/
        ├── glossary.md                # Technical terms
        ├── zh.json                    # Chinese rules
        ├── ja.json                    # Japanese rules
        └── ko.json                    # Korean rules
```

---

## 🧪 Testing the Skills

### Test Each Skill Individually

```bash
# Test codebase-analyzer
cd .claude/skills/codebase-analyzer
python3 scripts/detect_language.py /path/to/project
python3 scripts/extract_imports.py /path/to/file.rs
python3 scripts/parse_structure.py /path/to/project

# Test code-relationship-mapper
cd .claude/skills/code-relationship-mapper
python3 scripts/build_dependency_graph.py /path/to/project
```

### Test in Claude

```
User: "Test the codebase-analyzer skill on this project"

Claude will:
1. Activate the skill
2. Run analysis scripts
3. Generate report
```

---

## 🛠️ Customization

### Add New Language Support

Edit `codebase-analyzer/scripts/detect_language.py`:

```python
# Add new language detection
if (path / 'Cargo.lock').exists():
    detections.append({
        'language': 'Your Language',
        'config_file': 'your-config.toml',
        ...
    })
```

### Customize Templates

Edit `architecture-documenter/templates/*.md` to change output format.

### Add Translation Language

Create `multi-language-doc-generator/locales/new-lang.json`:

```json
{
  "language": "new-lang",
  "name": "Language Name",
  "glossary": {
    "Overview": "Translated Term",
    ...
  }
}
```

---

## 📈 Performance

### Benchmarks

| Project Size | Analysis Time | Token Usage |
|--------------|---------------|-------------|
| Small (<100 files) | 30-60s | ~5K tokens |
| Medium (100-500) | 1-3 min | ~15K tokens |
| Large (500-1000) | 3-5 min | ~30K tokens |
| Very Large (1000+) | 5-10 min | ~50K+ tokens |

### Optimization Tips

1. **Use Quick Mode**: For large projects, analyze key modules first
2. **Cache Results**: Store analysis in conversation context
3. **Parallel Skills**: Run independent skills concurrently
4. **Selective Analysis**: Focus on specific directories

---

## 🤝 Contributing

### Adding New Skills

1. Create directory: `.claude/skills/your-skill/`
2. Write `SKILL.md` with YAML frontmatter
3. Add helper scripts if needed
4. Document usage and examples
5. Test thoroughly

### Improving Existing Skills

1. Fork or edit the skill
2. Update `SKILL.md` documentation
3. Add examples to demonstrate improvements
4. Test with multiple project types

---

## 📚 Resources

- **Claude Skills Documentation**: https://docs.claude.com/en/docs/claude-code/skills
- **C4 Model**: https://c4model.com/
- **Mermaid Diagrams**: https://mermaid.js.org/
- **deepwiki-rs (Binary version)**: https://github.com/lethanhson9901/deepwiki-rs

---

## 🎓 Learning Path

### Beginner
1. Start with `codebase-analyzer` on a small project
2. Read generated analysis
3. Ask Claude to explain findings

### Intermediate
4. Generate architecture docs with `architecture-documenter`
5. Visualize dependencies with `code-relationship-mapper`
6. Understand architectural patterns

### Advanced
7. Customize skills for your tech stack
8. Create multi-language documentation
9. Build your own complementary skills
10. Integrate into CI/CD workflows

---

## ⚡ Quick Examples

### Example 1: New Project Analysis
```
User: "I just joined a new team working on a Rust project. Help me understand it."

Claude:
[Activates codebase-analyzer]
"Let me analyze this Rust project for you..."

[Generates]
- Project overview
- Technology stack
- Module structure
- Key components
- Entry points
- Recommendations for where to start reading
```

### Example 2: Documentation for Open Source
```
User: "Create comprehensive documentation for this open source library in English, Chinese, and Japanese"

Claude:
[Activates codebase-analyzer]
→ Analyzes structure

[Activates architecture-documenter]
→ Generates C4 documentation

[Activates multi-language-doc-generator]
→ Translates to Chinese and Japanese

[Output]
docs/
├── en/ (English)
├── zh/ (Chinese)
└── ja/ (Japanese)
```

### Example 3: Refactoring Guidance
```
User: "I want to refactor this codebase. Show me the problem areas."

Claude:
[Activates codebase-analyzer]
→ Calculates complexity metrics

[Activates code-relationship-mapper]
→ Detects circular dependencies
→ Identifies tightly coupled modules

[Generates]
- High complexity files (candidates for splitting)
- Circular dependencies (must break)
- God objects (high fan-in modules)
- Orphaned code (unused modules)
- Refactoring recommendations
```

---

## 📄 License

These skills are part of the deepwiki-rs project analysis tools.

---

## 🙏 Acknowledgments

- Built on Claude's native analysis capabilities
- Inspired by deepwiki-rs architecture documentation tool
- C4 model by Simon Brown
- Mermaid diagram library

---

**Version**: 1.0.0
**Last Updated**: 2025-01
**Maintainer**: deepwiki-rs contributors

---

## 🆘 Support

For issues or questions:
1. Check individual skill documentation
2. Review examples in EXAMPLES.md
3. Ask Claude for help using the skills
4. Report issues on GitHub

**Happy analyzing! 🚀**
