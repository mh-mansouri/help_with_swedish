from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
SKILL_DIR = ROOT / "swedish-youtube-mentor"
BUNDLE = ROOT / "hjälp_om_svenska.skill"


def build_bundle() -> None:
    if BUNDLE.exists():
        BUNDLE.unlink()

    with zipfile.ZipFile(BUNDLE, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(SKILL_DIR.rglob("*")):
            if path.is_file():
                arcname = path.relative_to(ROOT)
                zf.write(path, arcname.as_posix())


if __name__ == "__main__":
    build_bundle()
    print(f"Built {BUNDLE.name}")
