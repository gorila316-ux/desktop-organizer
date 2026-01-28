import os
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DESKTOP_PATH = Path.home() / "Desktop"

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
        grouped[category].append(entry.name)

    if not grouped:
        print("No files found on the desktop.")
        return

    total = sum(len(files) for files in grouped.values())
    print(f"Desktop: {DESKTOP_PATH}")
    print(f"Total files: {total}")
    print("=" * 50)

    for category in sorted(grouped):
        files = sorted(grouped[category])
        print(f"\n[{category.upper()}] ({len(files)} files)")
        print("-" * 40)
        for name in files:
            print(f"  {name}")

    print()


if __name__ == "__main__":
    categorize_files()
