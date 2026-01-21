# AGENTS.md - Agent Guidelines for Network Security Learning Repository

This document provides guidelines for agentic coding assistants working in this repository.

## Project Overview

A 90-day network security learning curriculum with daily markdown files and supporting Python scripts for WeChat publishing and content management.

---

## Build / Lint / Test Commands

### Linting
```bash
# Run linter (preferred)
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Specific file
ruff check scripts/batch_update_days.py
```

### Running Scripts
```bash
# Generate HTML preview for WeChat
python scripts/generate_preview.py

# Batch update Day file structures
python scripts/batch_update_days.py

# Test WeChat publishing (requires .env with credentials)
python test_publish.py

# Individual day scripts
python scripts/day018_parse_log.py
python scripts/day020_probe_http.py <host> <port>
```

### Testing
No formal test suite exists. Run scripts directly to verify functionality.

---

## Code Style Guidelines

### Imports
- Standard library imports first, then third-party, then local
- Use `from __future__ import annotations` at top for modern type hints
- Prefer Python standard library over external dependencies where possible
- Use `pathlib.Path` for file operations

```python
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
```

### Formatting
- Use UTF-8 encoding for all file operations
- Max line length: 120 chars (not strictly enforced)
- Type hints required for function signatures in new code

```python
def parse_log(path: Path) -> list[dict[str, str]]:
    ...
```

### Naming Conventions
- Functions: `snake_case`
- Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Classes: `PascalCase`
- File names: `snake_case.py`

```python
ROOT = Path(__file__).resolve().parents[1]
def convert_markdown_to_html(file_path: str) -> str: ...
```

### Error Handling
- Use specific exceptions where possible
- Provide helpful error messages
- Return exit codes from main functions

```python
try:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print(f"ERROR: file not found: {filepath}")
    return 1
except Exception as exc:
    print("ERROR:", exc)
    return 1
```

### Type Hints
- Use modern syntax: `list[str]` instead of `List[str]`
- Return types on all functions
- Parameters typed when clear

### File Encoding
Always specify UTF-8 encoding:

```python
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

path.read_text(encoding="utf-8")
path.write_text(content, encoding="utf-8")
```

### Docstrings
Use triple-quoted strings at module/function level for new code:

```python
"""Parse demo log and extract structured data.

Args:
    path: Path to the log file.

Returns:
    List of dictionaries with Time, Level, and Msg fields.
"""
```

### Markdown Files
- Daily files: `daily/DayXXX.md` (3-digit zero-padded)
- UTF-8 encoded
- Chinese content
- Include these sections: 学习目标, 学习内容, 实践任务, 巩固练习, 评估标准, 学习成果达成情况

---

## Environment

- Python 3.9+ required
- Virtual environment at `.venv/`
- Dependencies: ruff, PIL (Pillow), wordcloud, markdown2, requests
- Configuration: `.env` for WeChat credentials (DO NOT commit)

---

## Project Structure

```
Network Security/
├── daily/              # Daily learning cards (Day001.md ~ Day090.md)
├── scripts/            # Python utility scripts
│   ├── batch_update_days.py      # Standardize Day file structures
│   ├── generate_daily_content.py # Generate all 90-day content
│   ├── generate_preview.py       # Convert MD to HTML preview
│   ├── day018_parse_log.py      # Day018: Log parsing demo
│   └── day020_probe_http.py     # Day020: HTTP probe tool
├── plan/               # Learning roadmap and schedules
│   └── 3-month-roadmap.md       # Weekly breakdown
├── docs/               # Additional documentation
├── test_publish.py     # WeChat publishing test script
├── .env                # WeChat credentials (DO NOT commit)
├── .gitignore          # Git ignore patterns
└── AGENTS.md           # This file
```

---

## Git Workflow

### Daily Commit Pattern
```bash
# After completing daily learning
git add daily/
git add images/  # if screenshots added
git commit -m "DayXXX: 完成学习与记录"

# Optional: push every few days
git push
```

### Branching Strategy
- Main branch: `main` - primary development
- Feature branches: Use descriptive names like `update-day022-content`

### Commit Message Format
```
DayXXX: brief description (Chinese preferred)

- key point 1
- key point 2
```

---

## Troubleshooting

### Common Issues

**Issue**: WeChat publishing fails with credential error
**Solution**: Check `.env` file exists with valid `WECHAT_APP_ID` and `WECHAT_APP_SECRET`

**Issue**: Preview HTML shows garbled Chinese characters
**Solution**: Ensure UTF-8 encoding when reading/writing files

**Issue**: Ruff linting errors on existing code
**Solution**: Run `ruff check --fix .` to auto-fix, or review rules in `pyproject.toml` if exists

**Issue**: Script cannot find markdown file
**Solution**: Verify working directory is project root, or use absolute paths with `pathlib.Path`

### Environment Setup
```bash
# Create virtual environment (if not exists)
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install ruff pillow wordcloud markdown2 requests
```

---

## Extended Commands

### Batch Operations
```bash
# Count total day files
ls daily/*.md | wc -l

# Find missing day files
for i in {001..090}; do [ ! -f "daily/Day$i.md" ] && echo "Missing: Day$i.md"; done

# Search for specific topic across all days
grep -r "CVE" daily/
```

### WeChat Publishing Workflow
```bash
# 1. Create/update markdown
# 2. Generate preview
python scripts/generate_preview.py

# 3. Check preview.html in browser
start preview.html  # Windows

# 4. Publish to WeChat (if credentials configured)
python test_publish.py
```

---

## Important Notes

1. **Security Focus**: All code is for educational/authorized testing only
2. **Chinese Content**: Most markdown files contain Chinese text
3. **WeChat Publishing**: `test_publish.py` handles markdown-to-HTML conversion for WeChat
4. **No Tests**: Run scripts directly to verify functionality
5. **Batch Updates**: `batch_update_days.py` standardizes Day file structures
6. **Images**: Store screenshots in `daily/images/` or root-level `images/` directory
7. **Dates**: Use format `YYYY-MM-DD` in markdown headers
8. **Week Numbers**: Marked as "第X周" (Week X) in daily files
