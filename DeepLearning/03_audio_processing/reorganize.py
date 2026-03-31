"""
reorganize.py
data/ 아래 모든 파일을 긁어서 아래 구조로 정리합니다.

  data/datas/images/  <- jpg, png
  data/datas/sound/   <- wav
  data/labels/images/ <- Im_*.json
  data/labels/sound/  <- Sm_*.json
"""

import os
import glob
import shutil

DATA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

DEST = {
    "images_data":  os.path.join(DATA_ROOT, "datas",  "images"),
    "sound_data":   os.path.join(DATA_ROOT, "datas",  "sound"),
    "images_label": os.path.join(DATA_ROOT, "labels", "images"),
    "sound_label":  os.path.join(DATA_ROOT, "labels", "sound"),
}

for path in DEST.values():
    os.makedirs(path, exist_ok=True)


def move(src: str, dst_dir: str) -> None:
    dst = os.path.join(dst_dir, os.path.basename(src))
    if src != dst:
        shutil.move(src, dst)


moved = {"images": 0, "sound": 0, "labels/images": 0, "labels/sound": 0}

for f in glob.glob(os.path.join(DATA_ROOT, "**", "*"), recursive=True):
    if not os.path.isfile(f):
        continue

    # 이미 목적지에 있으면 skip
    if any(f.startswith(d + os.sep) for d in DEST.values()):
        continue

    name = os.path.basename(f)
    ext  = os.path.splitext(name)[1].lower()

    if ext in (".jpg", ".png"):
        move(f, DEST["images_data"])
        moved["images"] += 1
    elif ext == ".wav":
        move(f, DEST["sound_data"])
        moved["sound"] += 1
    elif ext == ".json":
        if name.startswith("Im_"):
            move(f, DEST["images_label"])
            moved["labels/images"] += 1
        elif name.startswith("Sm_"):
            move(f, DEST["sound_label"])
            moved["labels/sound"] += 1

# 빈 폴더 정리
for root, dirs, files in os.walk(DATA_ROOT, topdown=False):
    if root in DEST.values():
        continue
    if not os.listdir(root):
        os.rmdir(root)

print("정리 완료:")
for k, n in moved.items():
    print(f"  {k}: {n}개")
