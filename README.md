```bash
apt update && apt install tmux nano clang -y
tmux
git clone https://github.com/thewh1teagle/israwave
cd israwave
wget https://huggingface.co/datasets/Cossale/Guj_dataset/resolve/main/guj_dataset.tar?download=true
mv guj_dataset.tar?download=true guj_dataset.tar
tar -xvf guj_dataset.tar
```

```bash
python process_dataset_new.py --hours 5
```

Dataset Statistics:
Total number of audio files: 2817
Total duration: 4.00 hours (17994.17 seconds)
Total duration: 4:59:54 (HH:MM:SS)

Created directory structure:
train/
├── metadata.csv
└── wavs/
    └── 2817 wav files

```bash
HF_HUB_ENABLE_HF_TRANSFER=1 python process_dataset.py
```

Dataset Statistics:
Total number of audio files: 22807
Total duration: 39.00 hours (143998.67 seconds)
Total duration: 39:59:58 (HH:MM:SS)

Created directory structure:
train/
├── metadata.csv
└── wav/
    └── 22807 wav files