"""
Media Library
Displays imported media files
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                             QLabel, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
import os

class MediaLibrary(QWidget):
    """Media library widget"""
    
    media_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.media_files = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Media Library")
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)
        
        # Media list
        self.media_list = QListWidget()
        self.media_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.media_list)
        
        # Add media button
        add_btn = QPushButton("+ Add Media")
        add_btn.clicked.connect(self.on_add_media)
        layout.addWidget(add_btn)
    
    def add_media(self, filepath):
        """Add media file to library"""
        if filepath not in self.media_files:
            self.media_files.append(filepath)
            
            item = QListWidgetItem(os.path.basename(filepath))
            item.setData(Qt.ItemDataRole.UserRole, filepath)
            item.setToolTip(filepath)
            self.media_list.addItem(item)
    
    def on_item_double_clicked(self, item):
        """Handle double click on media item"""
        filepath = item.data(Qt.ItemDataRole.UserRole)
        if filepath:
            self.media_selected.emit(filepath)
    
    def on_add_media(self):
        """Handle add media button click"""
        # This will be handled by the main window's import function
        pass

