#!/usr/bin/env python3
"""
Professional Video Editor - Main Entry Point
A comprehensive video editing application
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from video_editor import VideoEditor

def main():
    """Main application entry point"""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Video Editor")
    app.setOrganizationName("VideoEditor")
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Create and show main window
    editor = VideoEditor()
    editor.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

