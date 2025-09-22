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
    except OSError:
        print(f"Error: Cannot identify image file '{image_path}'.")
        return None

def save_image(image_object, save_path):
    """
    Saves the given Image object to the specified path.
    """
    if image_object:
        image_object.save(save_path)
        print(f"Image saved successfully to '{save_path}'.")

def encode_message(image, secret_message):
    """
    Hides a secret message within an image using the LSB technique.
    Returns a new Image object with the message embedded.
    """
    # Get the dimensions of the image
    width, height = image.size
    
    # 1. Convert the secret message into a binary string
    # '08b' ensures each character is represented by 8 bits
    message_binary = ''.join(format(ord(char), '08b') for char in secret_message)
    
    # 2. Check if the image has enough capacity to hold the message
    # Each pixel can hold 3 bits (in R, G, B channels)
    max_bits = width * height * 3
    if len(message_binary) > max_bits:
        raise ValueError("Error: Message is too large to be hidden in this image.")
        
    print(f"Hiding a message of {len(message_binary)} bits.")
    
    # 3. Create a copy of the image to modify
    encoded_image = image.copy()
    pixel_map = encoded_image.load()
    
    data_index = 0
    
    # 4. Iterate through each pixel and embed the data
    for y in range(height):
        for x in range(width):
            pixel = pixel_map[x, y]
            if len(pixel) == 3:
                r, g, b = pixel
                a = None
            elif len(pixel) == 4:
                r, g, b, a = pixel
            else:
                raise ValueError("Unsupported pixel format.")

            # Modify the LSB of the Red channel if there's still data
            if data_index < len(message_binary):
                r = (r & 254) | int(message_binary[data_index])
                data_index += 1

            # Modify the LSB of the Green channel if there's still data
            if data_index < len(message_binary):
                g = (g & 254) | int(message_binary[data_index])
                data_index += 1

            # Modify the LSB of the Blue channel if there's still data
            if data_index < len(message_binary):
                b = (b & 254) | int(message_binary[data_index])
                data_index += 1

            # Update the pixel in the new image with the modified values
            if a is not None:
                pixel_map[x, y] = (r, g, b, a)
            else:
                pixel_map[x, y] = (r, g, b)

            # If the entire message is hidden, we can stop early
            if data_index >= len(message_binary):
                print("Message embedded successfully.")
                return encoded_image
    
    return encoded_image


# Update the testing part of the script
if __name__ == '__main__':
    img_to_load = 'test_image.png'
    img = load_image(img_to_load)

    if img:
        secret = "This is a secret message!"
        # Call our new function
        encoded_img = encode_message(img, secret)
        
        if encoded_img:
            # Save the result to a new file
            save_image(encoded_img, 'secret_image.png')
    else:
        print("Error: The file 'test_image.png' was not found.")
