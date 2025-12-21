#!/usr/bin/env python3
"""Test multi-language analysis on FlashCode"""

from rag_101.retriever import generate_repo_ast

repo_path = "/tmp/FlashCode"
result = generate_repo_ast(repo_path)

print("=" * 80)
print("MULTI-LANGUAGE REPOSITORY ANALYSIS: FlashCode")
print("=" * 80)
print()

print("📊 OVERALL STATISTICS:")
print(f"   Total Files: {result['stats']['total_files']}")
print(f"   Total Functions: {result['stats']['total_functions']} (all languages)")
print(f"   Total Classes: {result['stats']['total_classes']} (all languages)")
print(f"   Total Imports: {result['stats']['total_imports']} (all languages)")
print()

# Break down by language
lang_stats = {}
for func in result['functions']:
    lang = func.get('language', 'unknown')
    lang_stats[lang] = lang_stats.get(lang, {'functions': 0})
    lang_stats[lang]['functions'] += 1

for cls in result['classes']:
    lang = cls.get('language', 'unknown')
    if lang not in lang_stats:
        lang_stats[lang] = {'functions': 0}
    if 'classes' not in lang_stats[lang]:
        lang_stats[lang]['classes'] = 0
    lang_stats[lang]['classes'] += 1

for imp in result['imports']:
    lang = imp.get('language', 'unknown')
    if lang not in lang_stats:
        lang_stats[lang] = {'functions': 0}
    if 'imports' not in lang_stats:
        lang_stats[lang]['imports'] = 0
    if 'imports' not in lang_stats[lang]:
        lang_stats[lang]['imports'] = 0
    lang_stats[lang]['imports'] += 1

print("📈 BREAKDOWN BY LANGUAGE:")
for lang, stats in sorted(lang_stats.items()):
    funcs = stats.get('functions', 0)
    classes = stats.get('classes', 0)
    imports = stats.get('imports', 0)
    print(f"   {lang.upper()}:")
    print(f"      Functions: {funcs}")
    print(f"      Classes: {classes}")
    print(f"      Imports: {imports}")
print()

print("📁 FILE TYPE DISTRIBUTION:")
file_types = {}
for file_path, file_info in result['files'].items():
    ftype = file_info.get('type', 'unknown')
    file_types[ftype] = file_types.get(ftype, 0) + 1

for ftype, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
    print(f"   {ftype}: {count} files")
print()

print("🔍 SAMPLE SWIFT FUNCTIONS (first 10):")
swift_funcs = [f for f in result['functions'] if f.get('language') == 'swift']
for idx, func in enumerate(swift_funcs[:10], 1):
    print(f"   {idx:2}. {func['name']:30} in {func['file']} (line {func['line']})")
print()

print("📦 SAMPLE SWIFT CLASSES (first 10):")
swift_classes = [c for c in result['classes'] if c.get('language') == 'swift']
for idx, cls in enumerate(swift_classes[:10], 1):
    print(f"   {idx:2}. {cls['name']:30} in {cls['file']} (line {cls['line']})")
print()

print("=" * 80)
print("✅ MULTI-LANGUAGE ANALYSIS COMPLETE")
print("=" * 80)
print()
print("Supported languages: Python, JavaScript, TypeScript, Java, Swift, C/C++")
print(f"This repository uses: {', '.join(lang_stats.keys())}")
