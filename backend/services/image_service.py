"""
Image model service.

Reproduces, unchanged, the original Streamlit application's:
  - DSEE module
  - ImageModel (EfficientNet-B3 + DSEE + classifier)
  - Google Drive model download
  - Image preprocessing transform
  - image_prediction() function

Loaded once at application startup (see app.py) and reused for every request.
"""

import os

import gdown
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models

device = torch.device("cpu")

# ── Image preprocessing — unchanged from the original app.py ──
transform = transforms.Compose(
    [
        transforms.Resize((300, 300)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        ),
    ]
)

# Module-level holder for the loaded model, populated by load_image_model().
_image_model = None


class DSEE(nn.Module):
    """Directional Spatial Edge Enhancement block — unchanged architecture."""

    def __init__(self, in_channels):
        super().__init__()

        self.h = nn.Conv2d(in_channels, in_channels, (1, 3), padding=(0, 1))
        self.v = nn.Conv2d(in_channels, in_channels, (3, 1), padding=(1, 0))
        self.d1 = nn.Conv2d(in_channels, in_channels, 3, padding=1)
        self.d2 = nn.Conv2d(in_channels, in_channels, 3, padding=1)
        self.r = nn.Conv2d(in_channels, in_channels, 3, padding=1)

        self.fusion = nn.Conv2d(in_channels * 5, in_channels, 1)
        self.bn = nn.BatchNorm2d(in_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        h = self.h(x)
        v = self.v(x)
        d1 = self.d1(x)
        d2 = self.d2(x)
        r = self.r(x)

        out = torch.cat([h, v, d1, d2, r], dim=1)
        out = self.fusion(out)
        out = self.bn(out)
        out = self.relu(out)

        return out + x


class ImageModel(nn.Module):
    """EfficientNet-B3 backbone + DSEE + classifier — unchanged architecture."""

    def __init__(self):
        super().__init__()

        self.backbone = models.efficientnet_b3(weights=None)
        self.features = self.backbone.features

        self.dsee = DSEE(1536)
        self.pool = nn.AdaptiveAvgPool2d(1)

        self.classifier = nn.Sequential(
            nn.Linear(1536, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(128, 3),
        )

    def forward(self, x):
        f = self.features(x)
        e = self.dsee(f)

        fused = f + 0.5 * e

        pooled = self.pool(fused)
        pooled = pooled.view(pooled.size(0), -1)

        return self.classifier(pooled)


def download_model(model_path: str, file_id: str) -> None:
    """
    Downloads image_model.pth from Google Drive if it does not already
    exist locally. The Google Drive file ID never reaches the frontend —
    this function only ever runs on the backend.
    """
    if not os.path.exists(model_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, model_path, quiet=False)


def load_image_model(model_path: str, file_id: str) -> ImageModel:
    """
    Ensures the model file exists (downloading it if necessary), builds
    the ImageModel, loads its weights, sets it to eval mode, and caches
    it at module level so it is only ever loaded once.
    """
    global _image_model

    download_model(model_path, file_id)

    model = ImageModel()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    _image_model = model
    return model


def image_prediction(image) -> np.ndarray:
    """
    Runs inference on a PIL Image (already converted to RGB) and returns
    the softmax class probabilities in the original class order:
    ["Healthy", "Early Deficiency", "Critical Deficiency"].
    """
    if _image_model is None:
        raise RuntimeError("Image model has not been loaded yet.")

    img_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = _image_model(img_tensor)
        probs = torch.softmax(outputs, dim=1).numpy()[0]
    return probs
