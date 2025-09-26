Project Log: Secure Data Hiding in Images
Project: Secure Data Hiding in Images using Enhanced LSB Steganography

Author: Tanmay

Period: August 10 - September 27, 2025

Week 1: Research & Environment Setup
Objective: The primary goal for the first week was to establish a stable development environment and gain a thorough understanding of the foundational concepts of LSB (Least Significant Bit) steganography.

Process and Implementation:

Python Installation: The latest stable version of Python was installed.

IDE Setup: Visual Studio Code was selected as the Integrated Development Environment.

Library Installation: Two key Python libraries were installed using pip:

Pillow (PIL Fork): For opening, manipulating, and saving image file formats.

NumPy: For efficient numerical operations on image pixel arrays.

Theoretical Research: Studied the principles of LSB steganography, where the last bit of a pixel's color value is modified to hide data with minimal visual change.

Image Format Selection: Chose the lossless PNG format to prevent corruption of hidden data during compression, unlike lossy formats like JPEG.

Challenges Faced: The python --version command failed in the terminal, indicating the system's PATH variable was not correctly configured after installation.

Solutions and Improvements: The issue was resolved by:

Disabling default Windows app execution aliases that interfered with the command.

Re-installing Python and ensuring the "Add Python to PATH" option was checked during setup.

Outcome: A fully functional Python development environment was established with a solid theoretical foundation for LSB steganography.

Week 2: Project Scaffolding and File I/O
Objective: To create the project's foundational structure, implement version control, and write functions for loading and saving image files.

Process and Implementation:

Version Control: A Git repository was created on GitHub and cloned locally to track project history.

File Structure: The main logic file, steganography.py, was created.

Image I/O Functions: Implemented load_image and save_image using the Pillow library.

```python
# From steganography.py
from PIL import Image

def load_image(image_path):
    """Opens and loads an image from the specified path."""
    try:
        image = Image.open(image_path)
        return image
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None

def save_image(image_object, save_path):
    """Saves the given Image object to the specified path."""
    if image_object:
        image_object.save(save_path)
```
Challenges Faced: Git commands failed with a fatal: not a git repository error because the terminal was not in the correct project directory.

Solutions and Improvements: Corrected the workflow by ensuring the terminal was navigated into the cloned repository folder (cd Steganography-Project-B.E-2025) before running any Git commands.

Outcome: A version-controlled project structure is now in place, with the fundamental ability to open and save images.

Week 3: Core LSB Encoding
Objective: To implement the core logic for encoding a secret text message into a cover image using the LSB technique.

Process and Implementation: The encode_message function was developed to:

Convert the secret message into a binary string.

Check if the message fits within the image's data capacity.

Iterate through pixels, modifying the LSB of each color channel (R, G, B) to embed the message bits.

```python
# From steganography.py - Snippet from encode_message function
def encode_message(image, secret_message):
    width, height = image.size
    message_binary = ''.join(format(ord(char), '08b') for char in secret_message)
    
    max_bits = width * height * 3
    if len(message_binary) > max_bits:
        raise ValueError("Error: Message is too large for this image.")
        
    encoded_image = image.copy()
    pixel_map = encoded_image.load()
    data_index = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixel_map[x, y][:3]

            # Modify RGB channels
            if data_index < len(message_binary):
                r = (r & 254) | int(message_binary[data_index]); data_index += 1
            if data_index < len(message_binary):
                g = (g & 254) | int(message_binary[data_index]); data_index += 1
            if data_index < len(message_binary):
                b = (b & 254) | int(message_binary[data_index]); data_index += 1

            # Update pixel, preserving Alpha if it exists
            pixel_map[x, y] = (r, g, b) + pixel_map[x, y][3:]
            
            if data_index >= len(message_binary):
                return encoded_image
    return encoded_image
```
Challenges Faced: The initial code failed on PNG images with an Alpha (transparency) channel (RGBA), as it only expected three RGB values per pixel.

Solutions and Improvements: The code was updated to handle both RGB and RGBA images by slicing pixel[:3] to always read the first three channels and preserving the original Alpha channel on write.

Outcome: A robust encode_message function that can embed a secret message into both RGB and RGBA images.

Week 4: Core LSB Decoding & Delimitation
Objective: To implement the logic for extracting a hidden message from a stego-image and to add a delimiter to mark the end of the message.

Process and Implementation:

EOF Marker: A unique 16-bit End-of-File marker (1111111111111110) is now appended to the secret message before encoding.

Decoding Function: The decode_message function was created to reverse the process. It extracts the LSB from each color channel, reconstructs the binary string, and stops when it finds the EOF marker.
```python
# From steganography.py - decode_message function
EOF_MARKER = '1111111111111110'

def decode_message(image):
    pixel_map = image.load()
    extracted_bits = ""
    
    for y in range(image.height):
        for x in range(image.width):
            for color_val in pixel_map[x, y][:3]:
                extracted_bits += str(color_val & 1)
                if extracted_bits.endswith(EOF_MARKER):
                    message_binary = extracted_bits[:-len(EOF_MARKER)]
                    # Convert binary string back to text
                    message = ""
                    for i in range(0, len(message_binary), 8):
                        byte = message_binary[i:i+8]
                        if len(byte) == 8:
                            message += chr(int(byte, 2))
                    return message
    return "No message found or EOF marker is missing."
```
Challenges Faced: Ensuring file paths on Windows were handled correctly to avoid issues with backslash \ escape characters.

Solutions and Improvements: Used Python's raw strings (e.g., r'C:\path\to\file.png') during testing to make file path handling more reliable.

Outcome: The project now has a complete encode-decode cycle. A message can be embedded with an EOF marker and perfectly retrieved. The core application logic is complete.