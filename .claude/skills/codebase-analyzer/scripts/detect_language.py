#!/usr/bin/env python3
"""
Detect project language and framework by analyzing configuration files.
"""

import json
import sys
from pathlib import Path


def detect_project(project_path):
    """Detect project type based on configuration files."""
    path = Path(project_path).resolve()

    if not path.exists():
        return {'error': f'Path does not exist: {project_path}'}

    detections = []

    # Rust
    cargo_toml = path / 'Cargo.toml'
    if cargo_toml.exists():
        detections.append({
            'language': 'Rust',
            'config_file': 'Cargo.toml',
            'source_dirs': ['src'],
            'test_dirs': ['tests'],
            'extensions': ['.rs'],
            'entry_points': ['src/main.rs', 'src/lib.rs'],
            'package_manager': 'Cargo'
        })

    # Python
    pyproject_toml = path / 'pyproject.toml'
    setup_py = path / 'setup.py'
    requirements_txt = path / 'requirements.txt'

    if pyproject_toml.exists() or setup_py.exists() or requirements_txt.exists():
        config_file = 'pyproject.toml' if pyproject_toml.exists() else 'setup.py'
        detections.append({
            'language': 'Python',
            'config_file': config_file,
            'source_dirs': ['src', '.'],
            'test_dirs': ['tests', 'test'],
            'extensions': ['.py'],
            'entry_points': ['__main__.py', 'main.py', 'app.py'],
            'package_manager': 'pip' if requirements_txt.exists() else 'poetry/setuptools'
        })

    # Node.js / JavaScript / TypeScript
    package_json = path / 'package.json'
    if package_json.exists():
        try:
            pkg_data = json.loads(package_json.read_text(encoding='utf-8'))
            dependencies = pkg_data.get('dependencies', {})
            dev_dependencies = pkg_data.get('devDependencies', {})
            all_deps = {**dependencies, **dev_dependencies}

            # Detect framework
            framework = None
            if 'react' in all_deps:
                framework = 'React'
            elif 'vue' in all_deps:
                framework = 'Vue'
            elif 'svelte' in all_deps:
                framework = 'Svelte'
            elif 'next' in all_deps:
                framework = 'Next.js'
            elif '@angular/core' in all_deps:
                framework = 'Angular'
            elif 'express' in all_deps:
                framework = 'Express'

            # Check for TypeScript
            is_typescript = 'typescript' in all_deps or (path / 'tsconfig.json').exists()
            language = 'TypeScript' if is_typescript else 'JavaScript'

            detections.append({
                'language': language,
                'framework': framework,
                'config_file': 'package.json',
                'source_dirs': ['src', 'lib'],
                'test_dirs': ['test', 'tests', '__tests__'],
                'extensions': ['.js', '.ts', '.jsx', '.tsx'] if is_typescript else ['.js', '.jsx'],
                'entry_points': ['index.js', 'index.ts', 'src/index.js', 'src/index.ts'],
                'package_manager': 'npm' if (path / 'package-lock.json').exists() else 'yarn' if (path / 'yarn.lock').exists() else 'pnpm'
            })
        except json.JSONDecodeError:
            detections.append({
                'language': 'JavaScript',
                'config_file': 'package.json',
                'error': 'Could not parse package.json'
            })

    # Java (Maven)
    pom_xml = path / 'pom.xml'
    if pom_xml.exists():
        detections.append({
            'language': 'Java',
            'build_tool': 'Maven',
            'config_file': 'pom.xml',
            'source_dirs': ['src/main/java'],
            'test_dirs': ['src/test/java'],
            'extensions': ['.java'],
            'entry_points': ['src/main/java/Main.java'],
            'package_manager': 'Maven'
        })

    # Java/Kotlin (Gradle)
    build_gradle = path / 'build.gradle'
    build_gradle_kts = path / 'build.gradle.kts'

    if build_gradle.exists() or build_gradle_kts.exists():
        config_file = 'build.gradle.kts' if build_gradle_kts.exists() else 'build.gradle'
        is_kotlin = build_gradle_kts.exists() or (path / 'src/main/kotlin').exists()

        detections.append({
            'language': 'Kotlin' if is_kotlin else 'Java',
            'build_tool': 'Gradle',
            'config_file': config_file,
            'source_dirs': ['src/main/kotlin', 'src/main/java'] if is_kotlin else ['src/main/java'],
            'test_dirs': ['src/test/kotlin', 'src/test/java'] if is_kotlin else ['src/test/java'],
            'extensions': ['.kt', '.java'] if is_kotlin else ['.java'],
            'entry_points': ['src/main/kotlin/Main.kt'] if is_kotlin else ['src/main/java/Main.java'],
            'package_manager': 'Gradle'
        })

    # Go
    go_mod = path / 'go.mod'
    if go_mod.exists():
        detections.append({
            'language': 'Go',
            'config_file': 'go.mod',
            'source_dirs': ['.'],
            'test_dirs': ['.'],  # Go tests are in *_test.go files
            'extensions': ['.go'],
            'entry_points': ['main.go', 'cmd/main.go'],
            'package_manager': 'go modules'
        })

    # Ruby
    gemfile = path / 'Gemfile'
    if gemfile.exists():
        detections.append({
            'language': 'Ruby',
            'config_file': 'Gemfile',
            'source_dirs': ['lib', 'app'],
            'test_dirs': ['spec', 'test'],
            'extensions': ['.rb'],
            'entry_points': ['bin/main', 'app.rb'],
            'package_manager': 'Bundler'
        })

    # If no detection, try to infer from directory structure
    if not detections:
        source_files = {}
        for ext in ['.py', '.js', '.rs', '.java', '.go', '.rb', '.ts']:
            files = list(path.glob(f'**/*{ext}'))
            if files:
                source_files[ext] = len(files)

        if source_files:
            most_common = max(source_files, key=source_files.get)
            lang_map = {
                '.py': 'Python',
                '.js': 'JavaScript',
                '.ts': 'TypeScript',
                '.rs': 'Rust',
                '.java': 'Java',
                '.go': 'Go',
                '.rb': 'Ruby'
            }
            detections.append({
                'language': lang_map.get(most_common, 'Unknown'),
                'detection_method': 'file_extension_inference',
                'file_count': source_files[most_common],
                'warning': 'No configuration file found, inferred from file extensions'
            })

    # Build result
    result = {
        'project_path': str(path),
        'project_name': path.name,
        'detected_languages': detections,
    }

    if detections:
        result['primary_language'] = detections[0]['language']
        result['primary_config'] = detections[0].get('config_file', 'N/A')
    else:
        result['primary_language'] = 'Unknown'
        result['warning'] = 'Could not detect project type'

    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Usage: detect_language.py <project_path>',
            'example': 'python detect_language.py /path/to/project'
        }, indent=2))
        sys.exit(1)

    project_path = sys.argv[1]
    result = detect_project(project_path)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
