import numpy as np

def apply_intensity_reduction(normal_map, mask, intensity_reduction=0.5, isReduceNoise=False):
    # Normalize mask to [0, 1] and add channel dimension if needed
    if len(mask.shape) == 2:
        mask_normalized = mask[:, :, np.newaxis] / 255.0
    else:
        mask_normalized = mask / 255.0

    # Use a fixed target color (e.g., (128, 128, 255) in RGB)
    # Convert to BGR order for OpenCV
    target_color = np.array([255, 128, 128], dtype=np.float32)  # BGR
    target_color_array = np.full_like(normal_map, target_color)

    # Blending factor
    blending_factor = intensity_reduction * mask_normalized

    # Perform linear interpolation (lerp)
    result = (1 - blending_factor) * normal_map + blending_factor * target_color_array

    if isReduceNoise:
        # Apply noise reduction within the masked areas
        result = fix_noise(result, mask)

    return result

def fix_noise(normal_map, mask):
    # TODO: implement noise reduction
    return normal_map
