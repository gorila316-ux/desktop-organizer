import sys
import shutil
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")

DESKTOP_PATH = Path.home() / "Desktop"

CATEGORY_MAP = {
    "이미지": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp", ".tiff"},
    "문서": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".hwp"},
    "동영상": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"},
    "음악": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "압축파일": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "실행파일": {".exe", ".msi", ".bat", ".cmd", ".ps1", ".sh"},
    "코드": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".h", ".json", ".xml", ".yaml", ".yml"},
    "CAD": {".dwg", ".dxf", ".nwc", ".nwd", ".nwf", ".rvt", ".rfa", ".ifc", ".bak", ".sdf", ".dgn"},
}

SKIP_FILES = {"desktop.ini", "thumbs.db"}

EXT_TO_CATEGORY = {}
for category, extensions in CATEGORY_MAP.items():
    for ext in extensions:
        EXT_TO_CATEGORY[ext] = category


def scan_desktop():
    grouped = defaultdict(list)

    for entry in DESKTOP_PATH.iterdir():
        if not entry.is_file():
            continue
        if entry.name.lower() in SKIP_FILES:
            continue
        if entry.suffix == ".lnk" or entry.suffix == ".url":
            continue

        ext = entry.suffix.lower()
        category = EXT_TO_CATEGORY.get(ext, "기타")
        grouped[category].append(entry)

    return grouped


def preview(grouped):
    total = sum(len(files) for files in grouped.values())
    print(f"\n바탕화면: {DESKTOP_PATH}")
    print(f"이동 대상: {total}개 파일")
    print("=" * 55)

    for category in sorted(grouped):
        files = grouped[category]
        dest = DESKTOP_PATH / category
        print(f"\n[{category}] -> {dest}")
        print("-" * 55)
        for f in sorted(files, key=lambda x: x.name):
            print(f"  {f.name}")

    print()


def move_files(grouped):
    moved = 0
    skipped = 0

    for category, files in grouped.items():
        dest_dir = DESKTOP_PATH / category
        dest_dir.mkdir(exist_ok=True)

        for f in files:
            dest = dest_dir / f.name
            if dest.exists():
                print(f"  [건너뜀] 이미 존재: {category}/{f.name}")
                skipped += 1
                continue

            shutil.move(str(f), str(dest))
            print(f"  [이동] {f.name} -> {category}/")
            moved += 1

    print(f"\n완료: {moved}개 이동, {skipped}개 건너뜀")


def main():
    if not DESKTOP_PATH.exists():
        print(f"바탕화면 경로를 찾을 수 없습니다: {DESKTOP_PATH}")
        return

    grouped = scan_desktop()

    if not grouped:
        print("이동할 파일이 없습니다.")
        return

    preview(grouped)

    answer = input("위 파일들을 이동하시겠습니까? (y/n): ").strip().lower()
    if answer == "y":
        print()
        move_files(grouped)
    else:
        print("취소되었습니다.")


if __name__ == "__main__":
    main()
