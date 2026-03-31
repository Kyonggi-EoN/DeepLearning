"""
DataExtractor.py

Data structure:
  data_root/
    datas/
      images/Im_*.jpg        <- 모든 이미지 flat
      sound/Sm_*.wav         <- 모든 사운드 flat
    labels/
      images/Im_*.json
      sound/Sm_*.json

라벨은 파일명에서 추출: Im_교통_0001.jpg -> label = "교통"
"""

import os
import glob
import json
from dataclasses import dataclass, field
from typing import List


@dataclass
class BBox:
    x: int
    y: int
    width: int
    height: int


@dataclass
class AudioSegment:
    start: float
    end: float


@dataclass
class DataItem:
    image_path: str
    sound_path: str
    label: str
    bboxes: List[BBox] = field(default_factory=list)
    segments: List[AudioSegment] = field(default_factory=list)


class DataExtractor:
    """
    Usage:
        ext = DataExtractor("./data")
        print(len(ext))
        ext.show(0)
    """

    def __init__(self, data_root: str):
        self.data_root = os.path.abspath(data_root)
        self._items: List[DataItem] = []
        self._load()

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, idx: int) -> DataItem:
        return self._items[idx]

    def __iter__(self):
        yield from self._items

    def show(self, idx: int) -> None:
        item = self._items[idx]
        print(f"[{idx}]  label   : {item.label}")
        print(f"       image   : {os.path.basename(item.image_path)}")
        print(f"       sound   : {os.path.basename(item.sound_path)}")
        print(f"       bboxes  : {item.bboxes}")
        print(f"       segments: {item.segments}")

    # ------------------------------------------------------------------

    def _load(self) -> None:
        # {label: [(data_path, label_path)]}
        image_map = self._scan("images", "jpg")
        sound_map = self._scan("sound",  "wav")

        for label, images in image_map.items():
            if label not in sound_map:
                continue
            sounds = sound_map[label]

            for i, (img_path, img_label_path) in enumerate(images):
                snd_path, snd_label_path = sounds[i % len(sounds)]

                self._items.append(DataItem(
                    image_path=img_path,
                    sound_path=snd_path,
                    label=label,
                    bboxes=self._load_image_label(img_label_path),
                    segments=self._load_sound_label(snd_label_path),
                ))

    def _scan(self, modality: str, ext: str) -> dict:
        """Returns {label: [(data_path, label_path), ...]}"""
        data_dir  = os.path.join(self.data_root, "datas",  modality)
        label_dir = os.path.join(self.data_root, "labels", modality)

        result = {}
        for data_path in glob.glob(os.path.join(data_dir, f"*.{ext}")):
            stem  = os.path.splitext(os.path.basename(data_path))[0]
            label = stem.split("_")[1]          # Im_교통_0001 -> 교통

            label_path = os.path.join(label_dir, stem + ".json")
            if not os.path.exists(label_path):
                continue

            result.setdefault(label, []).append((data_path, label_path))

        return result

    @staticmethod
    def _load_image_label(json_path: str) -> List[BBox]:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [
            BBox(x=ann["x"], y=ann["y"], width=ann["width"], height=ann["height"])
            for ann in data.get("annotations", [])
        ]

    @staticmethod
    def _load_sound_label(json_path: str) -> List[AudioSegment]:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [
            AudioSegment(start=ann["start"], end=ann["end"])
            for ann in data.get("annotations", [])
        ]
