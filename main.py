import numpy as np
import cv2
from PIL import Image, ImageEnhance

import numpy as np

def sigmoid(x, midpoint=128, steepness=0.05):
    """
    Compute the sigmoid function for smooth transitions.
    
    Parameters:
    x (int): Grayscale value (0-255).
    midpoint (int): Center point of the transition (default: 128).
    steepness (float): Controls the steepness of the curve (default: 0.05).
    
    Returns:
    float: Probability of selecting white dice (0-1).
    """
    return 1 / (1 + np.exp(-steepness * (x - midpoint)))


def render_single_dice(face, pixel_size, dot_size_factor=0.2, background_color=0, dot_color=255):
    """
    Render a single dice face with customizable background and dot colors.
    
    Parameters:
    face (int): Dice face value (1-6).
    pixel_size (int): Size of the dice block in pixels.
    dot_size_factor (float): Proportion of the pixel size used for dots.
    background_color (int): Background color of the dice (0-255).
    dot_color (int): Dot color of the dice (0-255).
    
    Returns:
    PIL.Image.Image: PIL Image of the rendered dice face.
    """
    canvas = np.full((pixel_size, pixel_size), background_color, dtype=np.uint8)  # Background color

    dot_radius = max(1, int(pixel_size * dot_size_factor / 2))
    dot_positions = {
        1: [(0.5, 0.5)],
        2: [(0.25, 0.25), (0.75, 0.75)],
        3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
        4: [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)],
        5: [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75), (0.5, 0.5)],
        6: [(0.25, 0.2), (0.25, 0.5), (0.25, 0.8),
            (0.75, 0.2), (0.75, 0.5), (0.75, 0.8)],
    }

    if face not in dot_positions:
        raise ValueError(f"Invalid face value: {face}. Must be 1-6.")

    for dx, dy in dot_positions[face]:
        cx = int(dx * pixel_size)
        cy = int(dy * pixel_size)
        cv2.circle(canvas, (cy, cx), dot_radius, dot_color, -1)  # Draw filled circle

    return Image.fromarray(canvas)


def block_average(image, block_size):
    """
    Compute block-wise average for an image.
    
    Parameters:
    image (PIL.Image.Image): Input PIL Image (grayscale).
    block_size (int): Size of each block (in pixels).
    
    Returns:
    numpy.ndarray: Numpy array of block-averaged values.
    """
    img_array = np.array(image)
    h, w = img_array.shape
    h_blocks, w_blocks = h // block_size, w // block_size
    avg_blocks = img_array[:h_blocks * block_size, :w_blocks * block_size] \
        .reshape(h_blocks, block_size, w_blocks, block_size) \
        .mean(axis=(1, 3))
    return avg_blocks

def render_dice_artwork(image_path, pixel_size, output_path, contrast_factor=1, upscale_factor=10, upscale_input=False):
    """
    Convert an image to a dice-based representation with smooth nonlinear grayscale-to-dice mapping.
    
    Parameters:
    image_path (str): Path to the input image.
    pixel_size (int): Size of each dice block in pixels.
    output_path (str): Path to save the output image.
    contrast_factor (float): Factor to adjust the contrast of the image.
    upscale_factor (int): Factor to upscale the input image.
    upscale_input (bool): Whether to upscale the input image before processing.
    
    Returns:
    None
    """
    # Load and preprocess the image
    image = Image.open(image_path)

    if upscale_input:
        w, h = image.size
        image = image.resize((w * upscale_factor, h * upscale_factor), Image.Resampling.LANCZOS)

    grayscale_image = image.convert("L")
    enhancer = ImageEnhance.Contrast(grayscale_image)
    grayscale_image = enhancer.enhance(contrast_factor)

    # Compute block averages
    block_data = block_average(grayscale_image, pixel_size)

    # Map grayscale to dice faces and types
    h_blocks, w_blocks = block_data.shape
    dice_faces = np.clip(np.ceil(block_data / 255 * 6), 1, 6).astype(int)

    np.savetxt("output/dice_faces_cf{}.txt".format(contrast_factor), dice_faces, fmt='%d')
    print("Dice face mapping saved to output/dice_faces_cf{}.txt".format(contrast_factor))

    # Create a blank canvas for the dice artwork at upscale resolution
    upscale_pixel_size = pixel_size * upscale_factor
    artwork_canvas = Image.new("L", (w_blocks * upscale_pixel_size, h_blocks * upscale_pixel_size), "black")

    for i in range(h_blocks):
        for j in range(w_blocks):
            face = dice_faces[i, j]
            avg_value = block_data[i, j]

            if use_black_dice_exlusively:
                # Force black dice for all grayscale values
                dice_type = "black"
            else:
                # Compute probability of white dice using sigmoid
                # Midpoint (cc)	Steepness (kk)	Effect
                # 128       	0.05	        Very smooth and gradual transition.
                # 128	        0.1	            Smooth but slightly sharper transition.
                # 128	        0.2	            Quick transition, more distinct separation.
                # 100	        0.1	            Earlier transition to white dice, favoring brighter areas.
                # 150	        0.1	            Later transition, favoring darker areas with black dice.
                prob_white = sigmoid(avg_value, midpoint=128, steepness=0.05)
                dice_type = "white" if np.random.rand() < prob_white else "black"

            # Render the appropriate dice
            if dice_type == "black":
                background_color, dot_color = 0, 255  # Black dice
            else:
                background_color, dot_color = 255, 0  # White dice

            dice_image = render_single_dice(face, upscale_pixel_size, background_color=background_color, dot_color=dot_color)
            artwork_canvas.paste(dice_image, (j * upscale_pixel_size, i * upscale_pixel_size))

    # Downscale the artwork to the desired resolution
    final_canvas = artwork_canvas.resize((w_blocks * pixel_size, h_blocks * pixel_size), Image.Resampling.LANCZOS)

    # Save the final artwork
    output_path = output_path.format(contrast_factor)
    final_canvas.save(output_path)
    print(f"Artwork saved to {output_path}")

# Example usage
input_image_path = "pwatson.jpg"  # Replace with your input image
print('Processing using input image: ', input_image_path)
debug_mode = False
use_black_dice_exlusively = False # If set to True, you will use a mix of black and white dice.
upscaling_input = True # Set to True to upscale the input image. 
#contrast_factor = 1 # original contrast factor of the input image.
contrast_factors = [0.8,1.2,1.5,1.9,2,3] # Range for contrast factor.
upscaling_factor = 10 # Upscaling factor for the input image.
# If you provide an image of 451x664. The output will be 4510x6640. 
# Using 100px dices you will get a 45x66 dices image.(4510/100=45, 6640/100=66)
output_artwork_path = "output/dice_artwork_cf{}.jpg"
pixel_size = 100  # Output dice size in pixels (keep 100 as default. if reduced the dots will squeeze and alter final rendering)
for contrast_factor in contrast_factors:
    render_dice_artwork(input_image_path, pixel_size, output_artwork_path, contrast_factor=contrast_factor, upscale_factor=upscaling_factor, upscale_input=upscaling_input)
