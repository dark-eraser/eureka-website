from PIL import Image
import os

def resize_and_pad_logo(path, output_path, target_width, target_height, background_color=(255, 255, 255)):
    """
    Resize a logo to fit within the target dimensions while maintaining the aspect ratio, add padding to match the target size exactly. Convert palette images with transparency to RGBA to properly handle transparency.
    """
    with Image.open(path) as img:
        # Check if the image is a palette image and convert to RGBA to handle transparency correctly
        if img.mode == 'P':
            img = img.convert('RGBA')
        
        # Ensure we're working in RGB for JPEG compatibility (if not saving as PNG)
        if not output_path.endswith('.png'):
            img = img.convert("RGB")
            background_color = background_color[:3]  # Use only RGB part of the background color

        # Calculate the new size preserving the aspect ratio
        original_width, original_height = img.size
        ratio = min(target_width / original_width, target_height / original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        
        # Resize the image using the LANCZOS filter
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Create a new image with the target size
        new_img_mode = "RGBA" if output_path.endswith('.png') else "RGB"
        new_img = Image.new(new_img_mode, (target_width, target_height), color=background_color)
        
        # Calculate padding
        padding_x = (target_width - new_size[0]) // 2
        padding_y = (target_height - new_size[1]) // 2
        
        # Paste the resized image onto the center of the new image
        new_img.paste(resized_img, (padding_x, padding_y), resized_img.convert('RGBA'))

        # Save the new image to the output path
        new_img.save(output_path)

def normalize_and_pad_logos(input_dir, output_dir, target_width, target_height, background_color=(255, 255, 255, 0)):
    """
    Normalize and pad all logos in the input directory, then save them to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for logo_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, logo_name)
        output_path = os.path.join(output_dir, logo_name)
        resize_and_pad_logo(input_path, output_path, target_width, target_height, background_color)

# Specify the input and output directories
input_dir = 'assets/img/partnerss'  # Update this path
output_dir = 'assets/img/new_partners'   # Update this path

# Target dimensions and background color
target_width = 1000
target_height = 500
background_color = (255, 255, 255, 0)  # RGBA for transparent background; change as needed

# Normalize and pad all logos
normalize_and_pad_logos(input_dir, output_dir, target_width, target_height, background_color)
