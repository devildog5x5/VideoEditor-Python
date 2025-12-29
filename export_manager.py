"""
Export Manager
Handles video export and rendering
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
import os

class ExportManager:
    """Manages video export"""
    
    def __init__(self):
        self.progress_callback = None
    
    def export(self, clips, output_path, progress_callback=None, quality='high'):
        """Export video from clips"""
        self.progress_callback = progress_callback
        
        if not clips:
            raise ValueError("No clips to export")
        
        # Get processed clips
        processed_clips = []
        for i, clip in enumerate(clips):
            if progress_callback:
                progress = int((i / len(clips)) * 100)
                progress_callback(progress)
            
            processed_clip = clip.get_clip()
            if processed_clip:
                processed_clips.append(processed_clip)
        
        if not processed_clips:
            raise ValueError("No valid clips to export")
        
        # Concatenate clips
        if progress_callback:
            progress_callback(50)
        
        final_clip = concatenate_videoclips(processed_clips, method="compose")
        
        # Determine codec and bitrate based on quality
        codec_settings = self.get_codec_settings(quality)
        
        if progress_callback:
            progress_callback(75)
        
        # Write video file
        final_clip.write_videofile(
            output_path,
            codec=codec_settings['codec'],
            bitrate=codec_settings['bitrate'],
            fps=codec_settings.get('fps', 30),
            preset=codec_settings.get('preset', 'medium'),
            threads=4
        )
        
        if progress_callback:
            progress_callback(100)
        
        # Clean up
        final_clip.close()
        for clip in processed_clips:
            clip.close()
    
    def get_codec_settings(self, quality='high'):
        """Get codec settings based on quality"""
        settings = {
            'low': {
                'codec': 'libx264',
                'bitrate': '1000k',
                'preset': 'ultrafast',
                'fps': 24
            },
            'medium': {
                'codec': 'libx264',
                'bitrate': '5000k',
                'preset': 'medium',
                'fps': 30
            },
            'high': {
                'codec': 'libx264',
                'bitrate': '10000k',
                'preset': 'slow',
                'fps': 30
            },
            'ultra': {
                'codec': 'libx264',
                'bitrate': '20000k',
                'preset': 'veryslow',
                'fps': 60
            }
        }
        return settings.get(quality, settings['high'])

