import os
import subprocess
from PIL import Image

# Define ASCII characters for different pixel brightness levels
ASCII_CHARS = "@%#*+=-:. "

def install_pillow():
    """Install Pillow using pip if it's not installed."""
    try:
        subprocess.check_call(["pip", "install", "Pillow"])
        print("Pillow installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Pillow: {e}")

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65  # Aspect ratio adjustment for ASCII
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")  # Convert image to grayscale

def pixels_to_ascii(image):
    pixels = image.getdata()  # Get pixel data
    ascii_str = ""
    for pixel in pixels:
        # Ensure the index does not go out of bounds
        ascii_str += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]  # Map pixel value to ASCII character
    return ascii_str

def image_to_ascii(image_path, new_width=100):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}. {e}")
        return

    image = resize_image(image, new_width)
    image = grayify(image)  # Convert to grayscale
    ascii_str = pixels_to_ascii(image)  # Generate ASCII art

    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join(ascii_str[i:i + img_width] for i in range(0, ascii_str_len, img_width))
    
    return ascii_img

def save_ascii_art(ascii_art, output_path="ascii_art.txt"):
    try:
        with open(output_path, "w") as f:
            f.write(ascii_art)
        print(f"ASCII art saved to {output_path}.")
    except Exception as e:
        print(f"Error saving ASCII art: {e}")

def main():
    # Try to import Pillow, install if not available
    try:
        from PIL import Image
    except ImportError:
        print("Pillow is not installed. Installing...")
        install_pillow()

    image_path = input("Enter the path to the image: ")

    while True:
        try:
            new_width = int(input("Enter the desired width (default is 100): ") or 100)
            if new_width <= 0:
                raise ValueError("Width must be a positive integer.")
            break
        except ValueError as ve:
            print(ve)
    
    ascii_art = image_to_ascii(image_path, new_width)
    
    if ascii_art:
        print(ascii_art)  # Print ASCII art to console

        output_path = input("Enter the output file name (default is 'ascii_art.txt'): ") or "ascii_art.txt"
        save_ascii_art(ascii_art, output_path)  # Save to a specified text file

if __name__ == "__main__":
    main()
