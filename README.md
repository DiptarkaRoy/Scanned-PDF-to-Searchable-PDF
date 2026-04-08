# Scanned PDF to Searchable PDF Converter

A high-performance, parallelized OCR tool optimized for macOS (Apple Silicon) and Windows. This tool converts scanned image-based PDFs into searchable, selectable text PDFs using Tesseract OCR.

## 🚀 Features
- **Multiprocessing**: Utilizes all available CPU cores (Optimized for 8 workers on M3).
- **Progress Tracking**: Real-time progress bar using `tqdm`.
- **Cross-Platform**: Automatic path detection for macOS and Windows.
- **Queue Management**: Built-in lock file to prevent overlapping jobs.

## 🛠️ Prerequisites

Before running the tool, you must install the following system dependencies:

### macOS (Recommended)
```bash
# Install Homebrew if you haven't already
/bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"

# Install Poppler and Tesseract
brew install poppler tesseract
```

## 📦 Setup & Installation

### Using uv
- Install uv: ```brew install uv```
- Setup the Project:
    Run this inside the project folder to create the environment and install dependencies instantly.
        ```uv sync```

### Using standard pip
- **Create and Activate environment:**
    ```python3 -m venv .venv```
    ```source .venv/bin/activate```
- **Install the tool in editable mode:**
    ```pip install -e .```

## How to Run

### The Global Command
Run from anywhere in your terminal (while the environment is active): ```pdf-convert-to-readable "/path/to/your/file.pdf"```
### Using uv run (No activation required): ```uv run pdf-convert-to-readable "/path/to/your/file.pdf"```
### The Direct Python Way: ```python main.py "/path/to/your/file.pdf"```

## Troubleshooting

- **PDFInfoNotInstalledError:** 
    **Error:** Unable to get page count. Is poppler installed and in PATH?
    **Fix:** brew install poppler
- **TesseractNotFoundError:**
    **Error:** tesseract is not installed or it's not in your PATH
    **Fix:**
    - Install Tesseract: brew install tesseract
    - Verify path with which tesseract (usually /opt/homebrew/bin/tesseract).
    - Ensure main.py matches this path.
- **Permission Denied:**
    **Error:** zsh: permission denied: pdf-convert-to-readable
    **Fix:** chmod +x main.py
- **Memory/Thermal Throttling:**
    **Issue:** MacBook Air M3 gets warm on very large files.
    **Fix:** Reduce WORKERS = 4 in main.py to lower CPU load.

## ⚙️ Configuration
The tool is pre-configured for MacBook Air M3 (24GB RAM):
- **Workers:** 8 parallel processes.
- **DPI:** 200 (Optimal balance).
- **Tesseract Path:** /opt/homebrew/bin/tesseract.