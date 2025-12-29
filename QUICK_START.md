# Quick Start Guide

## Installation

### Step 1: Install Python
- Download Python 3.8+ from https://www.python.org
- Make sure to check "Add Python to PATH" during installation

### Step 2: Install Dependencies

**Windows:**
```bash
install.bat
```

**macOS/Linux:**
```bash
pip install -r requirements.txt
```

### Step 3: Install FFmpeg

**Windows:**
- Download from https://ffmpeg.org/download.html
- Extract and add to PATH, or place `ffmpeg.exe` in project folder

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

## Running the Application

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
python main.py
```

## Basic Usage

1. **Import Video**
   - Click "Import Video" button
   - Select video files (MP4, AVI, MOV, etc.)

2. **Add to Timeline**
   - Drag video from Media Library to timeline
   - Or double-click video in library

3. **Edit**
   - Select clip on timeline
   - Adjust properties (brightness, contrast, etc.)
   - Cut clips: Press 'S' at playhead position
   - Delete: Select clip and press Delete

4. **Preview**
   - Press Space to play/pause
   - Scrub timeline to jump to any point

5. **Export**
   - Click "Export Video" button
   - Choose output location and format
   - Wait for rendering

## Keyboard Shortcuts

- `Space` - Play/Pause
- `S` - Split clip at playhead
- `Delete` - Delete selected clip
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+S` - Save project
- `Ctrl+O` - Open project
- `Ctrl+E` - Export video

## Troubleshooting

**"FFmpeg not found"**
- Install FFmpeg (see Installation Step 3)
- Or place ffmpeg.exe in project folder

**Import errors**
- Check Python version: `python --version` (need 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

**Slow performance**
- Use smaller video files for testing
- Close other applications
- Reduce preview quality

## Need Help?

Check the full README.md for detailed documentation.

