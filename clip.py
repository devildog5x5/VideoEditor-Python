"""
Video Clip Class
Represents a video clip on the timeline
"""

from moviepy.editor import VideoFileClip
import os

class VideoClip:
    """Represents a video clip with editing properties"""
    
    def __init__(self, filepath, start_time=0):
        self.filepath = filepath
        self.name = os.path.basename(filepath)
        self.start_time = start_time  # Position on timeline
        self.duration = 0
        self.end_time = 0
        self.trim_start = 0  # Trim start point in source video
        self.trim_end = 0  # Trim end point in source video
        
        # Effects
        self.brightness = 0
        self.contrast = 1.0
        self.saturation = 1.0
        self.volume = 1.0
        self.speed = 1.0
        
        # Transitions
        self.fade_in_duration = 0
        self.fade_out_duration = 0
        
        # Load video to get duration
        try:
            self.video_clip = VideoFileClip(filepath)
            self.duration = self.video_clip.duration
            self.trim_end = self.duration
        except Exception as e:
            print(f"Error loading video: {e}")
            self.video_clip = None
            self.duration = 0
    
    def get_clip(self):
        """Get the processed video clip with all effects applied"""
        if not self.video_clip:
            return None
        
        clip = self.video_clip.subclip(self.trim_start, self.trim_end)
        
        # Apply speed
        if self.speed != 1.0:
            clip = clip.fx(lambda c: c.set_duration(c.duration / self.speed))
            clip = clip.fx(lambda c: c.set_fps(c.fps * self.speed))
        
        # Apply brightness/contrast/saturation
        if self.brightness != 0 or self.contrast != 1.0 or self.saturation != 1.0:
            from effects import apply_color_correction
            clip = apply_color_correction(clip, self.brightness, self.contrast, self.saturation)
        
        # Apply volume
        if self.volume != 1.0:
            clip = clip.volumex(self.volume)
        
        # Apply fades
        if self.fade_in_duration > 0:
            clip = clip.fadein(self.fade_in_duration)
        if self.fade_out_duration > 0:
            clip = clip.fadeout(self.fade_out_duration)
        
        return clip
    
    def split(self, split_time):
        """Split clip at specified time (relative to clip start)"""
        if split_time <= 0 or split_time >= self.duration:
            return None
        
        # Create new clip for second part
        new_clip = VideoClip(self.filepath, self.start_time + split_time)
        new_clip.trim_start = self.trim_start + split_time
        new_clip.trim_end = self.trim_end
        
        # Update current clip
        self.trim_end = self.trim_start + split_time
        self.duration = split_time
        self.end_time = self.start_time + self.duration
        
        return new_clip
    
    def trim(self, start, end):
        """Trim clip to specified time range"""
        self.trim_start = max(0, start)
        self.trim_end = min(self.duration, end)
        self.duration = self.trim_end - self.trim_start
    
    def set_start_time(self, time):
        """Set the start time on timeline"""
        self.start_time = time
        self.end_time = self.start_time + self.duration
    
    def to_dict(self):
        """Convert clip to dictionary for saving"""
        return {
            'filepath': self.filepath,
            'start_time': self.start_time,
            'trim_start': self.trim_start,
            'trim_end': self.trim_end,
            'brightness': self.brightness,
            'contrast': self.contrast,
            'saturation': self.saturation,
            'volume': self.volume,
            'speed': self.speed,
            'fade_in_duration': self.fade_in_duration,
            'fade_out_duration': self.fade_out_duration
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create clip from dictionary"""
        clip = cls(data['filepath'], data['start_time'])
        clip.trim_start = data.get('trim_start', 0)
        clip.trim_end = data.get('trim_end', clip.duration)
        clip.brightness = data.get('brightness', 0)
        clip.contrast = data.get('contrast', 1.0)
        clip.saturation = data.get('saturation', 1.0)
        clip.volume = data.get('volume', 1.0)
        clip.speed = data.get('speed', 1.0)
        clip.fade_in_duration = data.get('fade_in_duration', 0)
        clip.fade_out_duration = data.get('fade_out_duration', 0)
        return clip
    
    def update_properties(self, properties):
        """Update clip properties from properties panel"""
        if 'brightness' in properties:
            self.brightness = properties['brightness']
        if 'contrast' in properties:
            self.contrast = properties['contrast']
        if 'saturation' in properties:
            self.saturation = properties['saturation']
        if 'volume' in properties:
            self.volume = properties['volume']
        if 'speed' in properties:
            self.speed = properties['speed']
        if 'fade_in' in properties:
            self.fade_in_duration = properties['fade_in']
        if 'fade_out' in properties:
            self.fade_out_duration = properties['fade_out']

