from pathlib import Path
import argparse
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
SKILL_DIR = ROOT / "swedish_mentor"
BUNDLE = ROOT / "swedish_mentor.skill"


def build_bundle(bundle_path: Path = BUNDLE) -> Path:
    if bundle_path.exists():
        bundle_path.unlink()

    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(SKILL_DIR.rglob("*")):
            if path.is_file():
                arcname = path.relative_to(ROOT)
                zf.write(path, arcname.as_posix())

    return bundle_path


def check_bundle() -> bool:
    required_files = [
        SKILL_DIR / "SKILL.md",
        SKILL_DIR / "references" / "channels-by-level.md",
        SKILL_DIR / "references" / "podcasts-by-level.md",
        SKILL_DIR / "references" / "speaking-clips.md",
    ]

    missing = [path for path in required_files if not path.exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f" - {path}")
        return False

    if not BUNDLE.exists():
        print(f"Bundle not found: {BUNDLE}")
        return False

    print("Bundle and required skill files look present.")
    return True


def install_bundle(skills_dir: Path) -> Path:
    skills_dir.mkdir(parents=True, exist_ok=True)
    target = skills_dir / BUNDLE.name
    shutil.copy2(BUNDLE, target)
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build, check, or install the skill bundle")
    parser.add_argument("--check", action="store_true", help="Validate that the bundle and skill files are present")
    parser.add_argument("--install", action="store_true", help="Copy the packaged skill bundle to a skills directory")
    parser.add_argument("--skills-dir", type=Path, default=None, help="Destination directory for --install")
    args = parser.parse_args()

    if args.check:
        sys.exit(0 if check_bundle() else 1)

    if args.install:
        if not BUNDLE.exists():
            build_bundle()
        destination = install_bundle(args.skills_dir or Path.home() / ".claude" / "skills")
        print(f"Installed {BUNDLE.name} to {destination}")
        sys.exit(0)

    bundle_path = build_bundle()
    print(f"Built {bundle_path.name}")
