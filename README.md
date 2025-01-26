### README.md

# Pixel Dice Art Generator

This project converts an image into a dice-based representation, where each pixel block is represented by a dice face. The dice faces are determined based on the grayscale value of the pixel block. The project supports using both black and white dice, or exclusively black dice.

## Features

- Convert images to dice-based artwork.
- Option to use both black and white dice or only black dice.
- Adjustable contrast factor for image preprocessing.
- Upscaling of input images for higher resolution output.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/benlec/pixeldice.git
    cd pixeldice
    ```

2. Install the required dependencies:
    ```sh
    pip install numpy opencv-python pillow
    ```

## Usage

1. Place your input image in the project directory.

2. Update the main.py file with your desired settings:
    - input_image_path: Path to your input image.
    - debug_mode: Set to `True` to enable debugging (saves intermediate images).
    - use_only_black_dice: Set to `True` to use only black dice, `False` to use both black and white dice.
    - upscaling_input: Set to `True` to upscale the input image.
    - contrast_factors: List of contrast factors to apply.
    - upscaling_factor: Factor to upscale the input image.
    - output_artwork_path: Path to save the final dice-based artwork.
    - pixel_size: Size of each dice block in the output image.

3. Run the script:
    ```sh
    python main.py
    ```

## Example

```python
# Example usage
input_image_path = "pwatson.jpg"  # Replace with your input image
print('Processing using input image: ', input_image_path)
debug_mode = False
use_only_black_dice = True  # If set to True, you will use only black dice.
upscaling_input = True  # Set to True to upscale the input image.
contrast_factors = [0.8, 1.2, 1.5, 1.9, 2, 3]  # Range for contrast factor.
upscaling_factor = 10  # Upscaling factor for the input image.
# If you provide an image of 451x664, the output will be 4510x6640.
# Using 100px dices you will get a 45x66 dices image (4510/100=45, 6640/100=66).
output_artwork_path = "output/dice_artwork_cf{}.jpg"
pixel_size = 100  # Output dice size in pixels (keep 100 as default. if reduced the dots will squeeze and alter final rendering)

for contrast_factor in contrast_factors:
    render_dice_artwork(input_image_path, pixel_size, output_artwork_path, contrast_factor=contrast_factor, upscale_factor=upscaling_factor, upscale_input=upscaling_input, use_only_black_dice=use_only_black_dice)
```

## Output Samples

|Black Dice Only | Contrast Factor | Output Image                                   |
|----------------|-----------------|------------------------------------------------|
|True            | 0.8             | ![Output 0.8](output/dice_artwork_cf0.8.jpg)   |
|True            | 1.2             | ![Output 1.2](output/dice_artwork_cf1.2.jpg)   |
|True            | 1.5             | ![Output 1.5](output/dice_artwork_cf1.5.jpg)   |
|True            | 1.9             | ![Output 1.9](output/dice_artwork_cf1.9.jpg)   |
|True            | 2               | ![Output 2.0](output/dice_artwork_cf2.jpg)     |
|False           | 1.5             | ![Output 2.0](output/dice_artwork_bw_cf1.5.jpg)|
|False           | 3               | ![Output 2.0](output/dice_artwork_bw_cf3.jpg)  |

## Similar Resources

- [Dice Mosaic Generator](https://dicemosaicgenerator.com/)
- [Dice Effect Tool](https://online.visual-paradigm.com/photo-effects-studio/dice-effect-tool/)
- [Diceify Art](http://www.diceify.art/)
```
