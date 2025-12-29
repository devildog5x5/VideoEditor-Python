"""
Timeline Widget
Displays and manages the video editing timeline
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
                             QLabel, QPushButton, QSlider)
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
import math

class TimelineWidget(QWidget):
    """Timeline widget for displaying and editing video clips"""
    
    clip_selected = pyqtSignal(object)
    position_changed = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        self.clips = []
        self.selected_clip = None
        self.playhead_position = 0
        self.zoom_level = 1.0
        self.pixels_per_second = 50  # Base zoom level
        self.scroll_position = 0
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        # Timeline controls
        controls_layout = QHBoxLayout()
        
        # Zoom controls
        zoom_in_btn = QPushButton("+")
        zoom_in_btn.clicked.connect(self.zoom_in)
        controls_layout.addWidget(zoom_in_btn)
        
        zoom_out_btn = QPushButton("-")
        zoom_out_btn.clicked.connect(self.zoom_out)
        controls_layout.addWidget(zoom_out_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Timeline area (will be drawn in paintEvent)
        self.setMinimumHeight(150)
        self.setMaximumHeight(200)
        
    def add_clip(self, clip):
        """Add a clip to the timeline"""
        self.clips.append(clip)
        clip.end_time = clip.start_time + clip.duration
        self.update()
    
    def remove_clip(self, clip):
        """Remove a clip from timeline"""
        if clip in self.clips:
            self.clips.remove(clip)
            if self.selected_clip == clip:
                self.selected_clip = None
            self.update()
    
    def update_clip(self, clip):
        """Update clip display"""
        self.update()
    
    def clear(self):
        """Clear all clips"""
        self.clips = []
        self.selected_clip = None
        self.playhead_position = 0
        self.update()
    
    def set_position(self, position):
        """Set playhead position"""
        self.playhead_position = position
        self.update()
    
    def get_total_duration(self):
        """Get total duration of all clips"""
        if not self.clips:
            return 0
        return max(clip.end_time for clip in self.clips)
    
    def get_timeline_data(self):
        """Get timeline data for saving"""
        return {
            'clips': [clip.to_dict() for clip in self.clips],
            'zoom_level': self.zoom_level,
            'scroll_position': self.scroll_position
        }
    
    def zoom_in(self):
        """Zoom in on timeline"""
        self.zoom_level = min(self.zoom_level * 1.5, 10.0)
        self.pixels_per_second = 50 * self.zoom_level
        self.update()
    
    def zoom_out(self):
        """Zoom out on timeline"""
        self.zoom_level = max(self.zoom_level / 1.5, 0.1)
        self.pixels_per_second = 50 * self.zoom_level
        self.update()
    
    def paintEvent(self, event):
        """Paint the timeline"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get theme colors
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        theme_colors = None
        if app:
            theme_colors = app.property('theme_colors')
        
        if theme_colors:
            bg_color = theme_colors.get('timeline_bg', QColor(40, 40, 40))
            fg_color = theme_colors.get('timeline_fg', QColor(200, 200, 200))
        else:
            bg_color = QColor(40, 40, 40)
            fg_color = QColor(200, 200, 200)
        
        # Draw background
        painter.fillRect(self.rect(), bg_color)
        
        # Draw time markers
        self.draw_time_markers(painter, fg_color)
        
        # Draw clips
        for clip in self.clips:
            self.draw_clip(painter, clip)
        
        # Draw playhead
        self.draw_playhead(painter)
        
    def draw_time_markers(self, painter, fg_color):
        """Draw time markers on timeline"""
        marker_color = fg_color
        marker_color.setAlpha(150)
        painter.setPen(QPen(marker_color, 1))
        
        duration = self.get_total_duration()
        if duration == 0:
            duration = 60  # Default 1 minute
        
        # Draw major markers every 10 seconds
        for i in range(0, int(duration) + 10, 10):
            x = i * self.pixels_per_second - self.scroll_position
            if x >= 0 and x <= self.width():
                painter.drawLine(int(x), 0, int(x), self.height())
                painter.setPen(QPen(fg_color, 1))
                painter.drawText(int(x) + 5, 15, f"{i}s")
                painter.setPen(QPen(marker_color, 1))
        
        # Draw minor markers every second
        minor_color = fg_color
        minor_color.setAlpha(100)
        painter.setPen(QPen(minor_color, 1))
        for i in range(0, int(duration) + 1):
            x = i * self.pixels_per_second - self.scroll_position
            if x >= 0 and x <= self.width():
                painter.drawLine(int(x), 0, int(x), 20)
    
    def draw_clip(self, painter, clip):
        """Draw a clip on timeline"""
        x = clip.start_time * self.pixels_per_second - self.scroll_position
        width = clip.duration * self.pixels_per_second
        
        if x + width < 0 or x > self.width():
            return  # Clip not visible
        
        # Clip rectangle
        clip_rect = QRect(int(x), 30, int(width), self.height() - 40)
        
        # Get theme colors from application
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        theme_colors = None
        if app:
            theme_colors = app.property('theme_colors')
        
        if theme_colors:
            # Use theme colors
            if clip == self.selected_clip:
                color = theme_colors.get('timeline_selected', QColor(100, 150, 255))
            else:
                color = theme_colors.get('timeline_clip', QColor(60, 120, 200))
            text_color = theme_colors.get('timeline_fg', QColor(255, 255, 255))
        else:
            # Fallback colors
            if clip == self.selected_clip:
                color = QColor(100, 150, 255)
            else:
                color = QColor(60, 120, 200)
            text_color = QColor(255, 255, 255)
        
        painter.fillRect(clip_rect, color)
        painter.setPen(QPen(text_color, 2))
        painter.drawRect(clip_rect)
        
        # Clip name
        painter.setPen(QPen(text_color))
        clip_name = clip.name[:20] + "..." if len(clip.name) > 20 else clip.name
        painter.drawText(clip_rect.adjusted(5, 5, -5, -5), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, clip_name)
    
    def draw_playhead(self, painter):
        """Draw playhead indicator"""
        x = self.playhead_position * self.pixels_per_second - self.scroll_position
        
        if x < 0 or x > self.width():
            return
        
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.drawLine(int(x), 0, int(x), self.height())
        
        # Draw triangle at top
        from PyQt6.QtCore import QPoint
        triangle = [
            QPoint(int(x) - 5, 0),
            QPoint(int(x) + 5, 0),
            QPoint(int(x), 10)
        ]
        painter.setBrush(QBrush(QColor(255, 0, 0)))
        painter.drawPolygon(triangle)
    
    def mousePressEvent(self, event):
        """Handle mouse clicks"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Calculate time from x position
            x = event.position().x() + self.scroll_position
            time = x / self.pixels_per_second
            
            # Check if clicking on a clip
            clicked_clip = None
            for clip in self.clips:
                clip_x = clip.start_time * self.pixels_per_second
                clip_width = clip.duration * self.pixels_per_second
                if clip_x <= x <= clip_x + clip_width:
                    clicked_clip = clip
                    break
            
            if clicked_clip:
                self.selected_clip = clicked_clip
                self.clip_selected.emit(clicked_clip)
            else:
                self.selected_clip = None
                self.playhead_position = time
                self.position_changed.emit(time)
            
            self.update()
    
    def wheelEvent(self, event):
        """Handle mouse wheel for scrolling"""
        delta = event.angleDelta().y()
        self.scroll_position += delta / 10
        self.scroll_position = max(0, self.scroll_position)
        self.update()

