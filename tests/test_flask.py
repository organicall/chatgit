#!/usr/bin/env python3
"""Test Flask repository analysis"""

import os
import sys
from rag_101.retriever import generate_repo_ast

# Test on Flask
repo_path = "/tmp/flask-test"
print(f"Analyzing repository: Flask (Python web framework)\n")

result = generate_repo_ast(repo_path)

print("=" * 70)
print("FLASK REPOSITORY STATISTICS")
print("=" * 70)
print(f"Total Files: {result['stats']['total_files']}")
print(f"Total Functions: {result['stats']['total_functions']}")
print(f"Total Classes: {result['stats']['total_classes']}")
print(f"Total Imports: {result['stats']['total_imports']}")
print()

# Count Python files
python_files = [f for f in result['files'].keys() if f.endswith('.py')]
print(f"Python Files: {len(python_files)}")
print(f"Other Files: {result['stats']['total_files'] - len(python_files)}")

print("\n" + "=" * 70)
print("SAMPLE PYTHON FILES (first 10)")
print("=" * 70)
for idx, file_path in enumerate(sorted(python_files)[:10], 1):
    file_info = result['files'][file_path]
    if 'error' not in file_info:
        num_funcs = len(file_info.get('functions', []))
        num_classes = len(file_info.get('classes', []))
        print(f"{idx:2}. {file_path}")
        print(f"    Functions: {num_funcs}, Classes: {num_classes}")

print("\n" + "=" * 70)
print("TOP 20 MOST FUNCTION-RICH FILES")
print("=" * 70)

# Sort files by function count
file_func_counts = []
for file_path, file_info in result['files'].items():
    if file_path.endswith('.py') and 'error' not in file_info:
        num_funcs = len(file_info.get('functions', []))
        if num_funcs > 0:
            file_func_counts.append((file_path, num_funcs, file_info))

file_func_counts.sort(key=lambda x: x[1], reverse=True)

for idx, (file_path, num_funcs, file_info) in enumerate(file_func_counts[:20], 1):
    num_classes = len(file_info.get('classes', []))
    print(f"{idx:2}. {file_path}")
    print(f"    {num_funcs} functions, {num_classes} classes")

print("\n" + "=" * 70)
print("VERIFICATION")
print("=" * 70)
print(f"✓ Total files counted: {result['stats']['total_files']}")
print(f"✓ Total functions found: {result['stats']['total_functions']}")
print(f"✓ Total classes found: {result['stats']['total_classes']}")
print(f"✓ Total imports found: {result['stats']['total_imports']}")
