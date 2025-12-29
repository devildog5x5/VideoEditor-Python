"""
Theme Manager
Manages UI themes for the video editor
"""

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import QSettings
from enum import Enum

class Theme(Enum):
    """Available themes"""
    LIGHT = "light"
    DARK = "dark"
    OCEAN = "ocean"
    FOREST = "forest"
    SUNSET = "sunset"
    MIDNIGHT = "midnight"

class ThemeManager:
    """Manages application themes"""
    
    def __init__(self):
        self.current_theme = Theme.DARK
        self.settings = QSettings("VideoEditor", "Themes")
        self.load_saved_theme()
        self.themes = self._define_themes()
    
    def _define_themes(self):
        """Define all available themes"""
        return {
            Theme.LIGHT: {
                'name': 'Light',
                'window_bg': QColor(245, 245, 245),
                'window_fg': QColor(30, 30, 30),
                'base_bg': QColor(255, 255, 255),
                'base_fg': QColor(0, 0, 0),
                'alternate_bg': QColor(240, 240, 240),
                'alternate_fg': QColor(50, 50, 50),
                'highlight': QColor(0, 120, 215),
                'highlight_text': QColor(255, 255, 255),
                'button_bg': QColor(240, 240, 240),
                'button_fg': QColor(0, 0, 0),
                'button_hover': QColor(220, 220, 220),
                'button_pressed': QColor(200, 200, 200),
                'toolbar_bg': QColor(250, 250, 250),
                'timeline_bg': QColor(50, 50, 50),
                'timeline_fg': QColor(200, 200, 200),
                'timeline_clip': QColor(70, 130, 200),
                'timeline_selected': QColor(100, 150, 255),
                'preview_bg': QColor(0, 0, 0),
                'status_bg': QColor(240, 240, 240),
                'status_fg': QColor(50, 50, 50),
            },
            Theme.DARK: {
                'name': 'Dark',
                'window_bg': QColor(30, 30, 30),
                'window_fg': QColor(240, 240, 240),
                'base_bg': QColor(40, 40, 40),
                'base_fg': QColor(220, 220, 220),
                'alternate_bg': QColor(50, 50, 50),
                'alternate_fg': QColor(200, 200, 200),
                'highlight': QColor(0, 120, 215),
                'highlight_text': QColor(255, 255, 255),
                'button_bg': QColor(60, 60, 60),
                'button_fg': QColor(220, 220, 220),
                'button_hover': QColor(80, 80, 80),
                'button_pressed': QColor(100, 100, 100),
                'toolbar_bg': QColor(35, 35, 35),
                'timeline_bg': QColor(25, 25, 25),
                'timeline_fg': QColor(180, 180, 180),
                'timeline_clip': QColor(60, 120, 200),
                'timeline_selected': QColor(100, 150, 255),
                'preview_bg': QColor(0, 0, 0),
                'status_bg': QColor(40, 40, 40),
                'status_fg': QColor(200, 200, 200),
            },
            Theme.OCEAN: {
                'name': 'Ocean',
                'window_bg': QColor(20, 40, 60),
                'window_fg': QColor(220, 240, 255),
                'base_bg': QColor(30, 55, 80),
                'base_fg': QColor(200, 230, 255),
                'alternate_bg': QColor(40, 70, 100),
                'alternate_fg': QColor(180, 220, 255),
                'highlight': QColor(0, 150, 200),
                'highlight_text': QColor(255, 255, 255),
                'button_bg': QColor(50, 85, 120),
                'button_fg': QColor(200, 230, 255),
                'button_hover': QColor(60, 100, 140),
                'button_pressed': QColor(70, 115, 160),
                'toolbar_bg': QColor(25, 50, 75),
                'timeline_bg': QColor(15, 30, 45),
                'timeline_fg': QColor(150, 200, 230),
                'timeline_clip': QColor(40, 120, 180),
                'timeline_selected': QColor(60, 160, 220),
                'preview_bg': QColor(0, 0, 0),
                'status_bg': QColor(30, 55, 80),
                'status_fg': QColor(180, 220, 255),
            },
            Theme.FOREST: {
                'name': 'Forest',
                'window_bg': QColor(25, 45, 30),
                'window_fg': QColor(220, 240, 220),
                'base_bg': QColor(35, 60, 40),
                'base_fg': QColor(200, 230, 200),
                'alternate_bg': QColor(45, 75, 50),
                'alternate_fg': QColor(180, 220, 180),
                'highlight': QColor(50, 150, 80),
                'highlight_text': QColor(255, 255, 255),
                'button_bg': QColor(55, 90, 60),
                'button_fg': QColor(200, 230, 200),
                'button_hover': QColor(65, 110, 70),
                'button_pressed': QColor(75, 130, 80),
                'toolbar_bg': QColor(30, 55, 35),
                'timeline_bg': QColor(20, 35, 25),
                'timeline_fg': QColor(150, 200, 150),
                'timeline_clip': QColor(60, 140, 90),
                'timeline_selected': QColor(80, 180, 110),
                'preview_bg': QColor(0, 0, 0),
                'status_bg': QColor(35, 60, 40),
                'status_fg': QColor(180, 220, 180),
            },
            Theme.SUNSET: {
                'name': 'Sunset',
                'window_bg': QColor(60, 40, 30),
                'window_fg': QColor(255, 240, 220),
                'base_bg': QColor(80, 55, 40),
                'base_fg': QColor(255, 230, 200),
                'alternate_bg': QColor(100, 70, 50),
                'alternate_fg': QColor(255, 220, 180),
                'highlight': QColor(255, 140, 60),
                'highlight_text': QColor(255, 255, 255),
                'button_bg': QColor(120, 85, 60),
                'button_fg': QColor(255, 230, 200),
                'button_hover': QColor(140, 100, 70),
                'button_pressed': QColor(160, 115, 80),
                'toolbar_bg': QColor(70, 50, 35),
                'timeline_bg': QColor(50, 35, 25),
                'timeline_fg': QColor(255, 200, 150),
                'timeline_clip': QColor(200, 120, 80),
                'timeline_selected': QColor(255, 160, 100),
                'preview_bg': QColor(0, 0, 0),
                'status_bg': QColor(80, 55, 40),
                'status_fg': QColor(255, 220, 180),
            },
            Theme.MIDNIGHT: {
                'name': 'Midnight',
                'window_bg': QColor(15, 15, 25),
                'window_fg': QColor(230, 230, 250),
                'base_bg': QColor(25, 25, 35),
                'base_fg': QColor(210, 210, 240),
                'alternate_bg': QColor(35, 35, 45),
                'alternate_fg': QColor(190, 190, 230),
                'highlight': QColor(120, 100, 200),
                'highlight_text': QColor(255, 255, 255),
                'button_bg': QColor(45, 45, 55),
                'button_fg': QColor(210, 210, 240),
                'button_hover': QColor(55, 55, 65),
                'button_pressed': QColor(65, 65, 75),
                'toolbar_bg': QColor(20, 20, 30),
                'timeline_bg': QColor(10, 10, 20),
                'timeline_fg': QColor(170, 170, 210),
                'timeline_clip': QColor(80, 70, 150),
                'timeline_selected': QColor(140, 120, 220),
                'preview_bg': QColor(0, 0, 0),
                'status_bg': QColor(25, 25, 35),
                'status_fg': QColor(190, 190, 230),
            },
        }
    
    def get_theme(self, theme=None):
        """Get theme colors"""
        if theme is None:
            theme = self.current_theme
        return self.themes.get(theme, self.themes[Theme.DARK])
    
    def apply_theme(self, app, theme=None):
        """Apply theme to application"""
        if theme is None:
            theme = self.current_theme
        else:
            self.current_theme = theme
            self.save_theme()
        
        theme_colors = self.get_theme(theme)
        palette = QPalette()
        
        # Window colors
        palette.setColor(QPalette.ColorRole.Window, theme_colors['window_bg'])
        palette.setColor(QPalette.ColorRole.WindowText, theme_colors['window_fg'])
        
        # Base colors
        palette.setColor(QPalette.ColorRole.Base, theme_colors['base_bg'])
        palette.setColor(QPalette.ColorRole.AlternateBase, theme_colors['alternate_bg'])
        palette.setColor(QPalette.ColorRole.Text, theme_colors['base_fg'])
        
        # Button colors
        palette.setColor(QPalette.ColorRole.Button, theme_colors['button_bg'])
        palette.setColor(QPalette.ColorRole.ButtonText, theme_colors['button_fg'])
        
        # Highlight colors
        palette.setColor(QPalette.ColorRole.Highlight, theme_colors['highlight'])
        palette.setColor(QPalette.ColorRole.HighlightedText, theme_colors['highlight_text'])
        
        # Tooltip colors
        palette.setColor(QPalette.ColorRole.ToolTipBase, theme_colors['base_bg'])
        palette.setColor(QPalette.ColorRole.ToolTipText, theme_colors['base_fg'])
        
        app.setPalette(palette)
        
        # Store theme colors for custom widgets
        app.property('theme_colors', theme_colors)
        
        return theme_colors
    
    def get_stylesheet(self, theme=None):
        """Get stylesheet for custom styling"""
        if theme is None:
            theme = self.current_theme
        theme_colors = self.get_theme(theme)
        
        return f"""
        QMainWindow {{
            background-color: {theme_colors['window_bg'].name()};
            color: {theme_colors['window_fg'].name()};
        }}
        
        QToolBar {{
            background-color: {theme_colors['toolbar_bg'].name()};
            border: none;
            spacing: 5px;
        }}
        
        QToolBar QToolButton {{
            background-color: {theme_colors['button_bg'].name()};
            color: {theme_colors['button_fg'].name()};
            border: 1px solid {theme_colors['alternate_bg'].name()};
            border-radius: 4px;
            padding: 5px 10px;
            margin: 2px;
        }}
        
        QToolBar QToolButton:hover {{
            background-color: {theme_colors['button_hover'].name()};
        }}
        
        QToolBar QToolButton:pressed {{
            background-color: {theme_colors['button_pressed'].name()};
        }}
        
        QPushButton {{
            background-color: {theme_colors['button_bg'].name()};
            color: {theme_colors['button_fg'].name()};
            border: 1px solid {theme_colors['alternate_bg'].name()};
            border-radius: 4px;
            padding: 6px 12px;
            font-weight: 500;
        }}
        
        QPushButton:hover {{
            background-color: {theme_colors['button_hover'].name()};
        }}
        
        QPushButton:pressed {{
            background-color: {theme_colors['button_pressed'].name()};
        }}
        
        QListWidget {{
            background-color: {theme_colors['base_bg'].name()};
            color: {theme_colors['base_fg'].name()};
            border: 1px solid {theme_colors['alternate_bg'].name()};
            border-radius: 4px;
        }}
        
        QListWidget::item {{
            padding: 5px;
            border-bottom: 1px solid {theme_colors['alternate_bg'].name()};
        }}
        
        QListWidget::item:selected {{
            background-color: {theme_colors['highlight'].name()};
            color: {theme_colors['highlight_text'].name()};
        }}
        
        QListWidget::item:hover {{
            background-color: {theme_colors['button_hover'].name()};
        }}
        
        QGroupBox {{
            background-color: {theme_colors['base_bg'].name()};
            color: {theme_colors['base_fg'].name()};
            border: 1px solid {theme_colors['alternate_bg'].name()};
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        
        QSlider::groove:horizontal {{
            background-color: {theme_colors['alternate_bg'].name()};
            height: 6px;
            border-radius: 3px;
        }}
        
        QSlider::handle:horizontal {{
            background-color: {theme_colors['highlight'].name()};
            width: 18px;
            height: 18px;
            margin: -6px 0;
            border-radius: 9px;
        }}
        
        QSlider::handle:horizontal:hover {{
            background-color: {self._lighter_color(theme_colors['highlight']).name()};
        }}
        
        QLabel {{
            color: {theme_colors['base_fg'].name()};
        }}
        
        QStatusBar {{
            background-color: {theme_colors['status_bg'].name()};
            color: {theme_colors['status_fg'].name()};
            border-top: 1px solid {theme_colors['alternate_bg'].name()};
        }}
        """
    
    def get_available_themes(self):
        """Get list of available themes"""
        return list(self.themes.keys())
    
    def get_theme_name(self, theme):
        """Get display name for theme"""
        return self.themes[theme]['name']
    
    def save_theme(self):
        """Save current theme to settings"""
        self.settings.setValue('theme', self.current_theme.value)
    
    def load_saved_theme(self):
        """Load saved theme from settings"""
        saved_theme = self.settings.value('theme', Theme.DARK.value)
        try:
            self.current_theme = Theme(saved_theme)
        except ValueError:
            self.current_theme = Theme.DARK
    
    def _lighter_color(self, color, factor=120):
        """Make a color lighter"""
        r = min(255, color.red() * factor // 100)
        g = min(255, color.green() * factor // 100)
        b = min(255, color.blue() * factor // 100)
        return QColor(r, g, b)

