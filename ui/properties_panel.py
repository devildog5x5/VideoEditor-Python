"""
Properties Panel
Displays and edits clip properties
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
                             QDoubleSpinBox, QGroupBox, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal

class PropertiesPanel(QWidget):
    """Properties panel for editing clip properties"""
    
    properties_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.current_clip = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Properties"))
        
        # Brightness
        self.brightness_group = self.create_slider_group(
            "Brightness", -100, 100, 0, self.on_brightness_changed
        )
        layout.addWidget(self.brightness_group)
        
        # Contrast
        self.contrast_group = self.create_slider_group(
            "Contrast", 0, 200, 100, self.on_contrast_changed, scale=100
        )
        layout.addWidget(self.contrast_group)
        
        # Saturation
        self.saturation_group = self.create_slider_group(
            "Saturation", 0, 200, 100, self.on_saturation_changed, scale=100
        )
        layout.addWidget(self.saturation_group)
        
        # Volume
        self.volume_group = self.create_slider_group(
            "Volume", 0, 200, 100, self.on_volume_changed, scale=100
        )
        layout.addWidget(self.volume_group)
        
        # Speed
        self.speed_group = self.create_slider_group(
            "Speed", 25, 400, 100, self.on_speed_changed, scale=100
        )
        layout.addWidget(self.speed_group)
        
        # Fade In
        self.fade_in_group = self.create_slider_group(
            "Fade In", 0, 500, 0, self.on_fade_in_changed, scale=10, unit="s"
        )
        layout.addWidget(self.fade_in_group)
        
        # Fade Out
        self.fade_out_group = self.create_slider_group(
            "Fade Out", 0, 500, 0, self.on_fade_out_changed, scale=10, unit="s"
        )
        layout.addWidget(self.fade_out_group)
        
        layout.addStretch()
    
    def create_slider_group(self, label, min_val, max_val, default, callback, scale=1, unit=""):
        """Create a slider group"""
        group = QGroupBox(label)
        layout = QVBoxLayout(group)
        
        slider_layout = QHBoxLayout()
        
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.valueChanged.connect(callback)
        slider_layout.addWidget(slider)
        
        value_label = QLabel(f"{default / scale:.2f}{unit}")
        slider.valueChanged.connect(lambda v: value_label.setText(f"{v / scale:.2f}{unit}"))
        slider_layout.addWidget(value_label)
        
        layout.addLayout(slider_layout)
        
        # Store slider and label for later access
        group.slider = slider
        group.value_label = value_label
        
        return group
    
    def set_clip(self, clip):
        """Set the clip to edit"""
        self.current_clip = clip
        if clip:
            self.brightness_group.slider.setValue(int(clip.brightness))
            self.contrast_group.slider.setValue(int(clip.contrast * 100))
            self.saturation_group.slider.setValue(int(clip.saturation * 100))
            self.volume_group.slider.setValue(int(clip.volume * 100))
            self.speed_group.slider.setValue(int(clip.speed * 100))
            self.fade_in_group.slider.setValue(int(clip.fade_in_duration * 10))
            self.fade_out_group.slider.setValue(int(clip.fade_out_duration * 10))
        else:
            self.clear()
    
    def clear(self):
        """Clear properties"""
        self.current_clip = None
        self.brightness_group.slider.setValue(0)
        self.contrast_group.slider.setValue(100)
        self.saturation_group.slider.setValue(100)
        self.volume_group.slider.setValue(100)
        self.speed_group.slider.setValue(100)
        self.fade_in_group.slider.setValue(0)
        self.fade_out_group.slider.setValue(0)
    
    def on_brightness_changed(self, value):
        """Handle brightness change"""
        self.emit_property_change('brightness', value)
    
    def on_contrast_changed(self, value):
        """Handle contrast change"""
        self.emit_property_change('contrast', value / 100.0)
    
    def on_saturation_changed(self, value):
        """Handle saturation change"""
        self.emit_property_change('saturation', value / 100.0)
    
    def on_volume_changed(self, value):
        """Handle volume change"""
        self.emit_property_change('volume', value / 100.0)
    
    def on_speed_changed(self, value):
        """Handle speed change"""
        self.emit_property_change('speed', value / 100.0)
    
    def on_fade_in_changed(self, value):
        """Handle fade in change"""
        self.emit_property_change('fade_in', value / 10.0)
    
    def on_fade_out_changed(self, value):
        """Handle fade out change"""
        self.emit_property_change('fade_out', value / 10.0)
    
    def emit_property_change(self, property_name, value):
        """Emit property change signal"""
        self.properties_changed.emit({property_name: value})

