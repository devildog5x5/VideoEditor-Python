"""
Theme Selector Widget
Allows users to select and change themes
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QPushButton, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from themes import ThemeManager, Theme

class ThemeSelector(QWidget):
    """Theme selector widget"""
    
    theme_changed = pyqtSignal(object)
    
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        # Theme selector group
        group = QGroupBox("Theme")
        group_layout = QVBoxLayout(group)
        
        # Combo box for theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)
        
        # Add all themes
        for theme in Theme:
            self.theme_combo.addItem(
                self.theme_manager.get_theme_name(theme),
                theme
            )
        
        # Set current theme
        current_index = list(Theme).index(self.theme_manager.current_theme)
        self.theme_combo.setCurrentIndex(current_index)
        
        group_layout.addWidget(self.theme_combo)
        layout.addWidget(group)
        
        # Theme preview (optional - can show color swatches)
        preview_layout = QHBoxLayout()
        preview_layout.addWidget(QLabel("Preview:"))
        
        self.preview_label = QLabel()
        self.preview_label.setMinimumHeight(30)
        self.preview_label.setStyleSheet(
            f"background-color: {self.theme_manager.get_theme()['highlight'].name()};"
            f"border-radius: 4px;"
        )
        preview_layout.addWidget(self.preview_label)
        preview_layout.addStretch()
        
        group_layout.addLayout(preview_layout)
    
    def on_theme_changed(self, index):
        """Handle theme selection change"""
        theme = self.theme_combo.currentData()
        if theme:
            self.theme_manager.current_theme = theme
            self.theme_changed.emit(theme)
            
            # Update preview
            theme_colors = self.theme_manager.get_theme(theme)
            self.preview_label.setStyleSheet(
                f"background-color: {theme_colors['highlight'].name()};"
                f"border-radius: 4px;"
            )

