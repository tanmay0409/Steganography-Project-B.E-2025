# steganography.py

from PIL import Image

def load_image(image_path):
    """
    Opens and loads an image from the specified path.
    Returns an Image object or None if the file is not found.
    """
    try:
        image = Image.open(image_path)
        print(f"Image '{image_path}' loaded successfully.")
        return image
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None

def save_image(image_object, save_path):
    """
    Saves the given Image object to the specified path.
    """
    if image_object:
        image_object.save(save_path)
        print(f"Image saved successfully to '{save_path}'.")

# This part is for testing the functions directly
if __name__ == '__main__':
    # Find a sample PNG image, name it 'test_image.png', 
    # and place it in your project folder.
    img = load_image('test_image.png')

    if img:
        # Save the loaded image as a new file to prove it works
        save_image(img, 'test_image_copy.png')