# steganography.py

from PIL import Image

# MODIFICATION: Define the EOF marker as a binary string
EOF_MARKER = '1111111111111110'  # 16 bits unlikely to appear in normal text

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
    width, height = image.size
    
    message_binary = ''.join(format(ord(char), '08b') for char in secret_message)
    
    # MODIFICATION: Add the EOF marker to the end of the message
    message_binary += EOF_MARKER
    
    max_bits = width * height * 3
    if len(message_binary) > max_bits:
        raise ValueError("Error: Message is too large for this image.")
        
    print(f"Hiding a message of {len(message_binary)} bits (including EOF marker).")
    
    encoded_image = image.copy()
    pixel_map = encoded_image.load()
    
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = pixel_map[x, y]
            # Always extract RGB, ignore extra channels
            r, g, b = pixel[0], pixel[1], pixel[2]

            # Modify Red channel
            if data_index < len(message_binary):
                r = (r & 254) | int(message_binary[data_index])
                data_index += 1
            # Modify Green channel
            if data_index < len(message_binary):
                g = (g & 254) | int(message_binary[data_index])
                data_index += 1
            # Modify Blue channel
            if data_index < len(message_binary):
                b = (b & 254) | int(message_binary[data_index])
                data_index += 1

            # Reconstruct pixel with original alpha if it exists
            if len(pixel) == 4:
                a = pixel[3]
                pixel_map[x, y] = (r, g, b, a)
            else:
                pixel_map[x, y] = (r, g, b)

            if data_index >= len(message_binary):
                print("Message embedded successfully.")
                return encoded_image
    
    return encoded_image

# NEW FUNCTION FOR WEEK 4
def decode_message(image):
    """
    Extracts a secret message from an image.
    """
    width, height = image.size
    pixel_map = image.load()
    
    extracted_bits = ""
    
    for y in range(height):
        for x in range(width):
            pixel = pixel_map[x, y]
            
            # Extract LSB from R, G, B channels
            for color_val in pixel[:3]:
                # The '& 1' operation gets the LSB
                extracted_bits += str(color_val & 1)
                
                # Check if the extracted bits end with our EOF marker
                if extracted_bits.endswith(EOF_MARKER):
                    print("EOF marker found. Decoding complete.")
                    # Remove the marker from the bit string
                    message_binary = extracted_bits[:-len(EOF_MARKER)]
                    
                    # Convert binary string back to characters
                    message = ""
                    for i in range(0, len(message_binary), 8):
                        byte = message_binary[i:i+8]
                        if len(byte) == 8:
                            message += chr(int(byte, 2))
                    
                    return message
                    
    return "Could not find a hidden message."

# Updated the testing part of the script to perform a full cycle
if __name__ == '__main__':
    # --- ENCODE ---
    original_img_path = r'd:\Projects\Steganography-Project-B.E-2025\test_image.png'
    stego_img_path = r'd:\Projects\Steganography-Project-B.E-2025\secret_image.png'
    secret = "This is a secret message that we will now retrieve!"

    original_img = load_image(original_img_path)
    if original_img:
        print("\n--- Encoding Process ---")
        encoded_img = encode_message(original_img, secret)
        if encoded_img:
            save_image(encoded_img, stego_img_path)
    
        # --- DECODE ---
        print("\n--- Decoding Process ---")
        stego_img = load_image(stego_img_path)
        if stego_img:
            hidden_message = decode_message(stego_img)
            print(f"\nExtracted Message: {hidden_message}")