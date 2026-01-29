import os
import sys
from collections import defaultdict
from pathlib import Path
# Ensure UTF-8 encoding for standard input and output
sys.stdout.reconfigure(encoding="utf-8")
# Ensure UTF-8 encoding for standard input and output
DESKTOP_PATH = Path.home() / "Desktop"
# Define file categories and their associated extensions
CATEGORY_MAP = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp", ".tiff"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".hwp"},
    "videos": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "executables": {".exe", ".msi", ".bat", ".cmd", ".ps1", ".sh"},
    "code": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".h", ".json", ".xml", ".yaml", ".yml"},
    "shortcuts": {".lnk", ".url"},
    "cad": {".dwg", ".dxf", ".nwc", ".nwd", ".nwf", ".rvt", ".rfa", ".ifc", ".bak", ".sdf", ".dgn"},
}

EXT_TO_CATEGORY = {}
for category, extensions in CATEGORY_MAP.items():
    for ext in extensions:
        EXT_TO_CATEGORY[ext] = category


def format_size(size_bytes):
    """파일 크기를 보기 좋은 단위로 변환"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def categorize_files():
    if not DESKTOP_PATH.exists():
        print(f"Desktop path not found: {DESKTOP_PATH}")
        return

    grouped = defaultdict(list)

    for entry in DESKTOP_PATH.iterdir():
        if not entry.is_file():
            continue
        ext = entry.suffix.lower()
        category = EXT_TO_CATEGORY.get(ext, "etc")
        grouped[category].append(entry)

    if not grouped:
        print("No files found on the desktop.")
        return

    total = sum(len(files) for files in grouped.values())
    total_size = sum(f.stat().st_size for files in grouped.values() for f in files)
    print(f"Desktop: {DESKTOP_PATH}")
    print(f"Total files: {total} ({format_size(total_size)})")
    print("=" * 50)

    for category in sorted(grouped):
        files = sorted(grouped[category], key=lambda x: x.name)
        print(f"\n[{category.upper()}] ({len(files)} files)")
        print("-" * 50)
        for f in files:
            size = format_size(f.stat().st_size)
            print(f"  {f.name:<35} {size:>10}")

    print()


if __name__ == "__main__":
    categorize_files()
