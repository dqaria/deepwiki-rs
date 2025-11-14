# Language-Specific Patterns Reference

Quick reference for identifying and parsing code patterns across different programming languages.

---

## Rust

### Import Patterns
```rust
use std::collections::HashMap;
use tokio::runtime::Runtime;
use crate::utils::helper;
use super::parent_module;
```

**Regex**: `use\s+([^;]+);`

**Filtering**:
- Exclude: `std`, `core`, `alloc`, `crate`, `self`, `super`
- Keep only external crates

### Export Patterns
```rust
pub fn public_function() {}
pub struct PublicStruct {}
pub enum PublicEnum {}
pub trait PublicTrait {}
pub const PUBLIC_CONST: i32 = 42;
```

**Regex**: `pub\s+(?:fn|struct|enum|trait|const|static)\s+(\w+)`

### Entry Points
- Binary: `src/main.rs` with `fn main()`
- Library: `src/lib.rs`

### Config Files
- `Cargo.toml`: Dependencies, metadata
- `rust-toolchain.toml`: Rust version

---

## Python

### Import Patterns
```python
import os
import sys
from pathlib import Path
from typing import List, Dict
```

**Regex**:
- `import\s+(\w+)`
- `from\s+(\S+)\s+import`

### Export Patterns
```python
def public_function():
    pass

class PublicClass:
    pass

__all__ = ['public_function', 'PublicClass']
```

**Regex**:
- Functions: `^def\s+(\w+)\s*\(`
- Classes: `^class\s+(\w+)`
- Explicit exports: `__all__\s*=\s*\[(.*?)\]`

### Entry Points
- `__main__.py`
- `main.py`
- `app.py`
- `manage.py` (Django)

### Config Files
- `pyproject.toml`: Modern Python projects
- `setup.py`: Traditional packaging
- `requirements.txt`: Dependencies
- `Pipfile`: Pipenv
- `poetry.lock`: Poetry

---

## JavaScript / TypeScript

### Import Patterns
```javascript
// ES6
import React from 'react';
import { useState, useEffect } from 'react';
import * as utils from './utils';

// CommonJS
const express = require('express');
const { Router } = require('express');
```

**Regex**:
- ES6: `import\s+.*\s+from\s+['\"]([^'\"]+)['\"]`
- CommonJS: `require\(['\"]([^'\"]+)['\"]\)`

**Filtering**:
- Keep only packages (no `./ ` or `../` prefixes)
- Strip scopes: `@org/package` → keep both

### Export Patterns
```javascript
// Named exports
export function myFunction() {}
export class MyClass {}
export const MY_CONST = 42;

// Default export
export default MyComponent;

// Re-exports
export { foo, bar } from './module';
```

**Regex**:
- `export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)`
- `export\s+{([^}]+)}`

### Entry Points
- `index.js`, `index.ts`
- `main.js`, `main.ts`
- `app.js`, `app.ts`
- `src/index.{js,ts}`
- `package.json`: Check `main` and `module` fields

### Config Files
- `package.json`: Dependencies, scripts, metadata
- `tsconfig.json`: TypeScript configuration
- `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`: Lock files

### Framework Detection

**React**: `"react"` in dependencies
```javascript
import React from 'react';
import { Component } from 'react';
```

**Vue**: `"vue"` in dependencies
```javascript
import Vue from 'vue';
import { createApp } from 'vue';
```

**Angular**: `"@angular/core"` in dependencies
```typescript
import { Component } from '@angular/core';
```

**Express**: `"express"` in dependencies
```javascript
const express = require('express');
const app = express();
```

---

## Java

### Import Patterns
```java
import java.util.List;
import java.util.*;
import static java.lang.Math.PI;
import org.springframework.boot.SpringApplication;
```

**Regex**: `import\s+(?:static\s+)?([^;]+);`

**Filtering**:
- Exclude: `java.*`, `javax.*`
- Keep third-party packages (first segment of package name)

### Export Patterns
```java
public class PublicClass {}
public interface PublicInterface {}
public enum PublicEnum {}
```

**Regex**: `public\s+(?:class|interface|enum)\s+(\w+)`

### Entry Points
- `src/main/java/**/Main.java`
- Class with `public static void main(String[] args)`

### Config Files
- `pom.xml`: Maven projects
- `build.gradle` / `build.gradle.kts`: Gradle projects
- `settings.gradle`: Gradle settings

---

## Kotlin

### Import Patterns
```kotlin
import kotlin.collections.List
import org.springframework.boot.*
import com.example.utils.Helper
```

**Regex**: Same as Java

### Export Patterns
```kotlin
class PublicClass
data class DataClass
interface PublicInterface
object Singleton
```

**Regex**: `(?:class|data class|interface|object)\s+(\w+)`

### Entry Points
- `src/main/kotlin/**/Main.kt`
- Function: `fun main(args: Array<String>)`

### Config Files
- Same as Java (Kotlin often uses Gradle)

---

## Go

### Import Patterns
```go
import "fmt"
import "net/http"

import (
    "encoding/json"
    "github.com/gorilla/mux"
    "myproject/utils"
)
```

**Regex**:
- Single: `import\s+"([^"]+)"`
- Multi: `import\s+\((.*?)\)` (multiline)

### Export Patterns
```go
// Exported (capitalized)
func ExportedFunction() {}
type ExportedType struct {}
const ExportedConst = 42
var ExportedVar int
```

**Regex**: `(?:func|type|const|var)\s+([A-Z]\w*)`

**Note**: In Go, capitalization determines export visibility

### Entry Points
- `main.go`
- `cmd/appname/main.go`
- Package: `package main` with `func main()`

### Config Files
- `go.mod`: Module definition and dependencies
- `go.sum`: Checksums for dependencies

---

## Ruby

### Import Patterns
```ruby
require 'rails'
require 'active_record'
require_relative 'my_module'
```

**Regex**: `require\s+['\"]([^'\"]+)['\"]`

### Export Patterns
```ruby
class MyClass
end

module MyModule
end
```

**Regex**:
- `class\s+(\w+)`
- `module\s+(\w+)`

### Entry Points
- `bin/main`
- `app.rb`
- `config.ru` (Rack apps)

### Config Files
- `Gemfile`: Dependency specification
- `Gemfile.lock`: Lock file

---

## PHP

### Import Patterns
```php
use Symfony\Component\HttpFoundation\Request;
use App\Models\User;
require 'vendor/autoload.php';
```

**Regex**:
- `use\s+([^;]+);`
- `require(?:_once)?\s+['\"]([^'\"]+)['\"]`

### Export Patterns
```php
class MyClass {}
interface MyInterface {}
trait MyTrait {}
```

**Regex**: `(?:class|interface|trait)\s+(\w+)`

### Entry Points
- `index.php`
- `public/index.php`

### Config Files
- `composer.json`: Dependencies and autoloading
- `composer.lock`: Lock file

---

## C/C++

### Import Patterns
```c
#include <stdio.h>
#include "myheader.h"
```

**Regex**: `#include\s+[<"]([^>"]+)[>"]`

### Export Patterns
Look for header files (`.h`, `.hpp`) with function declarations

### Entry Points
- File containing `int main()`

### Config Files
- `CMakeLists.txt`: CMake build configuration
- `Makefile`: Make build rules
- `meson.build`: Meson build system

---

## Swift

### Import Patterns
```swift
import Foundation
import UIKit
```

**Regex**: `import\s+(\w+)`

### Export Patterns
```swift
public class MyClass {}
public func myFunction() {}
```

**Regex**: `public\s+(?:class|struct|func|var)\s+(\w+)`

### Entry Points
- `main.swift`
- `@main` attribute

### Config Files
- `Package.swift`: Swift Package Manager

---

## Scala

### Import Patterns
```scala
import scala.collection.mutable.HashMap
import java.util.{Date, Locale}
```

**Regex**: `import\s+([^;\n]+)`

### Export Patterns
```scala
class MyClass
object Singleton
trait MyTrait
```

**Regex**: `(?:class|object|trait)\s+(\w+)`

### Config Files
- `build.sbt`: SBT build definition

---

## Common Detection Strategies

### 1. Config File Priority

```
Highest Priority → Lowest Priority

Rust:    Cargo.toml > .rs files
Python:  pyproject.toml > setup.py > requirements.txt > .py files
Node.js: package.json > .js/.ts files
Java:    pom.xml > build.gradle > .java files
Go:      go.mod > .go files
```

### 2. Entry Point Discovery

1. Check config file for `main` field
2. Look for conventional names (`main.*`, `index.*`, `app.*`)
3. Search for main function pattern
4. Use most-imported file as fallback

### 3. Framework Detection

**Web Frameworks**:
- Django: `django` in dependencies + `manage.py`
- Flask: `flask` in dependencies
- Express: `express` in dependencies
- Spring Boot: `spring-boot-starter` in dependencies
- Rails: `rails` in Gemfile

**Frontend Frameworks**:
- React: `react` in dependencies
- Vue: `vue` in dependencies
- Angular: `@angular/core` in dependencies
- Svelte: `svelte` in dependencies

### 4. Test Detection

**Directory Patterns**:
- `test/`, `tests/`, `__tests__/`
- `spec/`
- `src/test/` (Java/Kotlin)

**File Patterns**:
- `*_test.*` (Go, Python)
- `*.test.*` (JS/TS)
- `*.spec.*` (JS/TS, Ruby)
- `Test*.java` (Java)

---

## Regular Expression Patterns Cheat Sheet

### Escape Characters in Different Languages

| Language | String Escape | Regex Escape |
|----------|---------------|--------------|
| Python   | `\` | `\\` |
| Rust     | `\` | `\\` |
| JavaScript | `\` | `\\` or `/` |
| Java     | `\` | `\\` |

### Common Patterns

**Identifier**: `\w+` or `[a-zA-Z_]\w*`
**Qualified Name**: `[\w.]+` or `\w+(?:\.\w+)*`
**Whitespace**: `\s+`
**Optional Whitespace**: `\s*`
**Any Characters**: `.*?` (non-greedy)
**Until Semicolon**: `[^;]+`
**Until Newline**: `[^\n]+`

---

## Usage Tips

1. **Start broad**: Use config file detection first
2. **Validate**: Cross-reference multiple signals
3. **Handle edge cases**: Mixed-language projects (e.g., Python + Rust)
4. **Cache results**: Don't re-parse the same file
5. **Error tolerance**: Skip unparseable files gracefully
