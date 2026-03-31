"""
AudioImageDataset.py
- torch.utils.data.Dataset wrapping DataExtractor
- label: depth1 기준 정수 클래스 (예: {"교통":0, "농기계":1, ...})

Each sample: (image_tensor, audio_tensor, label_id)
  - image_tensor : (3, 224, 224)  float32
  - audio_tensor : (C, T)         float32  (5초 고정)
  - label_id     : int

Requirements:
    pip install torch torchaudio torchvision Pillow

Usage:
    from DataExtractor import DataExtractor
    from AudioImageDataset import AudioImageDataset

    ext     = DataExtractor("./DeepLearning/data/image-sound_matching")
    dataset = AudioImageDataset(ext)
    loader  = DataLoader(dataset, batch_size=8, shuffle=True)

    for images, audios, labels in loader:
        ...
"""

import torch
import torchaudio
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms as T

from DataExtractor import DataExtractor, DataItem


_IMG_TRANSFORM = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]),
])


class AudioImageDataset(Dataset):
    """
    Args:
        extractor      : DataExtractor 인스턴스
        target_sr      : 오디오 리샘플링 목표 샘플레이트 (기본 22050)
        audio_duration : 오디오 고정 길이(초). None이면 원본 길이 유지 (배치 불가)
        img_transform  : 이미지 변환. None이면 기본값 사용
    """

    def __init__(
        self,
        extractor: DataExtractor,
        target_sr: int = 22050,
        audio_duration: float = 5.0,
        img_transform=None,
    ):
        self.extractor = extractor
        self.target_sr = target_sr
        self.audio_duration = audio_duration
        self.img_transform = img_transform or _IMG_TRANSFORM

        # depth1 -> int label map (정렬하여 결정론적으로 생성)
        labels = sorted({item.label for item in extractor})
        self.label_map: dict[str, int] = {name: i for i, name in enumerate(labels)}

    def __len__(self) -> int:
        return len(self.extractor)

    def __getitem__(self, idx: int):
        item: DataItem = self.extractor[idx]

        image = self._load_image(item)
        audio = self._load_audio(item)
        label = self.label_map[item.label]

        return image, audio, label

    # ------------------------------------------------------------------

    def _load_image(self, item: DataItem) -> torch.Tensor:
        img = Image.open(item.image_path).convert("RGB")
        return self.img_transform(img)

    def _load_audio(self, item: DataItem) -> torch.Tensor:
        waveform, sr = torchaudio.load(item.sound_path)

        if sr != self.target_sr:
            waveform = torchaudio.functional.resample(waveform, sr, self.target_sr)

        # 첫 번째 어노테이션 구간만 사용
        if item.segments:
            seg = item.segments[0]
            start = int(seg.start * self.target_sr)
            end   = int(seg.end   * self.target_sr)
            waveform = waveform[:, start:end]

        # 고정 길이로 패딩 / 트리밍
        if self.audio_duration is not None:
            target_len = int(self.audio_duration * self.target_sr)
            if waveform.shape[1] < target_len:
                waveform = torch.nn.functional.pad(waveform, (0, target_len - waveform.shape[1]))
            else:
                waveform = waveform[:, :target_len]

        return waveform
