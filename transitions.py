"""
Video Transitions
Transition effects between clips
"""

from moviepy.editor import VideoClip, CompositeVideoClip
import numpy as np

def crossfade(clip1, clip2, duration=1.0):
    """Crossfade transition between two clips"""
    clip1_fadeout = clip1.fadeout(duration)
    clip2_fadein = clip2.fadein(duration)
    
    return CompositeVideoClip([
        clip1_fadeout.set_position('center'),
        clip2_fadein.set_position('center').set_start(clip1.duration - duration)
    ])

def slide_transition(clip1, clip2, direction='left', duration=1.0):
    """Slide transition"""
    # Simple implementation - can be enhanced
    return crossfade(clip1, clip2, duration)

def wipe_transition(clip1, clip2, direction='left', duration=1.0):
    """Wipe transition"""
    # Simple implementation - can be enhanced
    return crossfade(clip1, clip2, duration)

def fade_in(clip, duration=1.0):
    """Fade in effect"""
    return clip.fadein(duration)

def fade_out(clip, duration=1.0):
    """Fade out effect"""
    return clip.fadeout(duration)

