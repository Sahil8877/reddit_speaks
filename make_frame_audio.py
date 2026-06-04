import numpy as np

def make_frame_factory(pitch, duration):
    """Creates a custom function scoped to a specific pitch and duration."""
    def make_frame(t):
        t = np.asarray(t)
        
        # Calculate standard time fade envelope
        fade_duration = 0.1  # seconds
        envelope = np.ones_like(t)
        
        # Fade in
        mask_in = t < fade_duration
        envelope[mask_in] = t[mask_in] / fade_duration
        
        # Fade out
        mask_out = t > (duration - fade_duration)
        envelope[mask_out] = (duration - t[mask_out]) / fade_duration

        # Generate the single sine wave tone for this pitch
        tone = 0.5 * envelope * np.sin(pitch * 2 * np.pi * t)
        return tone
        
    return make_frame
