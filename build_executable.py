"""
Build Executable Script
Creates a standalone executable from the Python video editor
"""

import PyInstaller.__main__
import os
import sys
import shutil

def build_executable():
    """Build the executable using PyInstaller"""
    
    print("Building Video Editor executable...")
    print("=" * 50)
    
    spec_file = os.path.join(os.path.dirname(__file__), 'VideoEditor.spec')
    
    # Use spec file if it exists, otherwise use command-line options
    if os.path.exists(spec_file):
        print(f"Using spec file: {spec_file}")
        options = [spec_file, '--clean', '--noconfirm']
    else:
        # Fallback to command-line options
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        options = [
            'main.py',
            '--name=VideoEditor',
            '--onefile',
            '--windowed',
            '--icon=' + icon_path,
            '--hidden-import=moviepy',
            '--hidden-import=cv2',
            '--hidden-import=numpy',
            '--hidden-import=PIL',
            '--hidden-import=scipy',
            '--hidden-import=imageio',
            '--hidden-import=imageio_ffmpeg',
            '--hidden-import=PyQt6',
            '--hidden-import=PyQt6.QtCore',
            '--hidden-import=PyQt6.QtGui',
            '--hidden-import=PyQt6.QtWidgets',
            '--hidden-import=PyQt6.sip',
            '--collect-all=PyQt6',
            '--collect-all=moviepy',
            '--collect-all=cv2',
            '--collect-all=imageio',
            '--noconfirm',
            '--clean',
        ]
    
    try:
        PyInstaller.__main__.run(options)
        print("\n[SUCCESS] Executable built successfully!")
        exe_path = os.path.abspath('dist/VideoEditor.exe')
        if os.path.exists(exe_path):
            print(f"Location: {exe_path}")
        else:
            # Check for onedir build
            onedir_path = os.path.abspath('dist/VideoEditor/VideoEditor.exe')
            if os.path.exists(onedir_path):
                print(f"Location (onedir): {onedir_path}")
            else:
                print("Warning: Executable location not found")
        return True
    except Exception as e:
        print(f"\n[ERROR] Error building executable: {e}")
        return False

if __name__ == "__main__":
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        os.system("pip install pyinstaller")
    
    success = build_executable()
    sys.exit(0 if success else 1)

