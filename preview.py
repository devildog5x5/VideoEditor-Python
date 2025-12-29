"""
Preview Widget
Displays video preview
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
import cv2
import numpy as np

class PreviewWidget(QWidget):
    """Video preview widget"""
    
    def __init__(self):
        super().__init__()
        self.current_clip = None
        self.current_frame = None
        self.position = 0
        self.cap = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        # Preview label
        self.preview_label = QLabel("No video loaded")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(400)
        self.preview_label.setStyleSheet("background-color: black; color: white;")
        layout.addWidget(self.preview_label)
        
    def set_clip(self, clip):
        """Set the clip to preview"""
        self.current_clip = clip
        if clip and clip.filepath:
            try:
                self.cap = cv2.VideoCapture(clip.filepath)
                self.update_frame()
            except Exception as e:
                print(f"Error opening video: {e}")
                self.cap = None
    
    def set_position(self, position):
        """Set preview position"""
        self.position = position
        self.update_frame()
    
    def update_frame(self):
        """Update the preview frame"""
        if not self.cap or not self.current_clip:
            return
        
        # Calculate frame position
        clip_position = self.position - self.current_clip.start_time
        if clip_position < 0 or clip_position >= self.current_clip.duration:
            return
        
        # Seek to position
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(clip_position * fps)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # Read frame
        ret, frame = self.cap.read()
        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Resize to fit preview
            height, width = frame_rgb.shape[:2]
            preview_width = self.preview_label.width()
            preview_height = self.preview_label.height()
            
            if preview_width > 0 and preview_height > 0:
                scale = min(preview_width / width, preview_height / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame_resized = cv2.resize(frame_rgb, (new_width, new_height))
            else:
                frame_resized = frame_rgb
            
            # Convert to QPixmap
            h, w, ch = frame_resized.shape
            bytes_per_line = ch * w
            q_image = QImage(frame_resized.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            
            self.preview_label.setPixmap(pixmap)
            self.current_frame = frame_resized
    
    def clear(self):
        """Clear preview"""
        if self.cap:
            self.cap.release()
            self.cap = None
        self.current_clip = None
        self.preview_label.clear()
        self.preview_label.setText("No video loaded")
    
    def refresh(self):
        """Refresh preview"""
        self.update_frame()
    
    def resizeEvent(self, event):
        """Handle resize"""
        super().resizeEvent(event)
        if self.current_clip:
            self.update_frame()

