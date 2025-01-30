# Gujarati TTS Training

This repository contains code for training a Text-to-Speech (TTS) model for the Gujarati language using the [optispeech](https://github.com/thewh1teagle/optispeech) framework.

## Dataset

The model is trained on a 5-hour subset of the [Gujarati Interspeech Dataset](https://huggingface.co/datasets/Cossale/gujarati-interspeech) containing:
- 2817 audio files
- Total duration: 4:59:54 (HH:MM:SS)
- Single male speaker
- Decent quality recordings

Dataset structure:
```
train/
├── metadata.csv
└── wavs/
    └── 2817 wav files
```

## Project Structure

```
.
├── configs/                   # Configuration files
│   ├── data/guj.yaml          # Dataset statistics
│   └── experiment/gujju.yaml  # Training hyperparameters  
├── data/
│   └── guj_dataset/           # Preprocessed training data
│       ├── train.txt
│       ├── val.txt 
│       └── wavs/
├── notebooks/
│   ├── prepare.ipynb          # Dataset preparation 
│   ├── train.ipynb            # Training script
│   └── export.ipynb           # Model export and testing
└── scripts/
    └── process_dataset.py     # Data preprocessing
```

## Pre-trained Models

Pre-trained checkpoints and ONNX models are available in the [GitHub releases](https://github.com/Aunali321/optispeech-train/releases/tag/v0.1.0):
- `last.ckpt.7z`: Training checkpoint
- `last.onnx`: Exported ONNX model

## Setup

1. Install system dependencies:
```bash
apt update && apt install tmux nano clang p7zip-full p7zip-rar aria2 gh -y
gh auth login
```

## Reproducing Checkpoint
1. Process dataset:
```bash
python process_datasets.py --hours 5  # Loads from parquet and formats to LJSpeech format
```
2. Run notebooks in sequence:
- prepare.ipynb: Prepares dataset splits, generates stats
- train.ipynb: Trains model with provided configs
- export.ipynb: Exports to ONNX and tests inference

## Notebooks

- **prepare.ipynb**: Downloads dataset, splits train/val, generates statistics
- **train.ipynb**: Main training script with checkpointing and monitoring
- **export.ipynb**: Exports trained model to ONNX format and tests inference

## Training Performance

- ~1 minute 30 seconds per epoch on NVIDIA RTX 4090
- Batch size: 14
- Workers: 12
- At 999 epochs (~402K steps) the model starts getting decent results (last.ckpt)

## Thanks ❤️
Special thanks to [gravityml](https://github.com/gravityml) for sponsoring compute resources.