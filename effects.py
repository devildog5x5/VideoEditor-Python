"""
Video Effects
Various video effects and filters
"""

from moviepy.editor import VideoClip
import numpy as np

def apply_color_correction(clip, brightness=0, contrast=1.0, saturation=1.0):
    """Apply color correction (brightness, contrast, saturation)"""
    def adjust_frame(frame):
        # Convert to float
        frame = frame.astype(np.float32) / 255.0
        
        # Apply brightness
        frame = frame + brightness / 100.0
        frame = np.clip(frame, 0, 1)
        
        # Apply contrast
        frame = (frame - 0.5) * contrast + 0.5
        frame = np.clip(frame, 0, 1)
        
        # Apply saturation
        gray = np.dot(frame[...,:3], [0.299, 0.587, 0.114])
        gray = np.stack([gray, gray, gray], axis=2)
        frame = gray + (frame - gray) * saturation
        frame = np.clip(frame, 0, 1)
        
        # Convert back to uint8
        return (frame * 255).astype(np.uint8)
    
    return clip.fl_image(adjust_frame)

def apply_blur(clip, blur_amount=5):
    """Apply blur effect"""
    from scipy import ndimage
    
    def blur_frame(frame):
        return ndimage.gaussian_filter(frame, sigma=blur_amount)
    
    return clip.fl_image(blur_frame)

def apply_sharpen(clip, strength=1.0):
    """Apply sharpen effect"""
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]]) * strength
    
    def sharpen_frame(frame):
        from scipy import ndimage
        return ndimage.convolve(frame, kernel)
    
    return clip.fl_image(sharpen_frame)

def apply_sepia(clip):
    """Apply sepia tone effect"""
    def sepia_frame(frame):
        frame = frame.astype(np.float32)
        sepia_matrix = np.array([[0.393, 0.769, 0.189],
                                [0.349, 0.686, 0.168],
                                [0.272, 0.534, 0.131]])
        frame = np.dot(frame, sepia_matrix.T)
        return np.clip(frame, 0, 255).astype(np.uint8)
    
    return clip.fl_image(sepia_frame)

def apply_black_white(clip):
    """Convert to black and white"""
    def grayscale_frame(frame):
        gray = np.dot(frame[...,:3], [0.299, 0.587, 0.114])
        return np.stack([gray, gray, gray], axis=2).astype(np.uint8)
    return clip.fl_image(grayscale_frame)

def apply_invert(clip):
    """Invert colors"""
    def invert_frame(frame):
        return 255 - frame
    
    return clip.fl_image(invert_frame)

def change_speed(clip, speed_factor):
    """Change playback speed"""
    return clip.fx(lambda c: c.set_duration(c.duration / speed_factor))

def reverse_video(clip):
    """Reverse video playback"""
    return clip.fx(lambda c: c.set_duration(c.duration))[::-1]

