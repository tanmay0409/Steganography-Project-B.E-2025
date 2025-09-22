Project Log: Secure Data Hiding in Images
Project: Secure Data Hiding in Images using Enhanced LSB Steganography
Author: Tanmay
Period: August 10 - September 27, 2025

Week 1: Research & Environment Setup
Objective
The primary goal for the first week was to establish a stable development environment and gain a thorough understanding of the foundational concepts of LSB (Least Significant Bit) steganography.

Process and Implementation
The initial phase involved setting up the necessary tools for the project. The chosen language was Python, valued for its extensive libraries for image manipulation.

Python Installation: The latest stable version of Python was installed.

IDE Setup: Visual Studio Code was selected as the Integrated Development Environment for its robust features, including an integrated terminal and Git support.

Library Installation: Two key Python libraries were installed using the pip package manager:

Pillow (PIL Fork): An essential library for opening, manipulating, and saving various image file formats.

NumPy: A library for numerical operations, which is highly efficient for handling the array-based structure of image pixels.

Theoretical Research: A study was conducted on the principles of LSB steganography. The core concept is that a computer represents images as a grid of pixels, where each pixel's color is defined by RGB (Red, Green, Blue) values from 0-255. Each value is an 8-bit byte. By altering the last bit (the LSB) of a color value, we can change the value by only 1, a modification that is imperceptible to the human eye. This LSB can be replaced with a bit from a secret message.

Image Format Selection: The PNG format was chosen for this project. As a lossless format, it preserves every pixel's data perfectly, which is critical for steganography. Lossy formats like JPEG would corrupt the hidden data during compression.

Challenges Faced
Upon setting up the environment, a verification check using python --version in the Windows Command Prompt failed. The system returned an error: Python was not found..., suggesting an installation from the Microsoft Store. This indicated that the system's PATH variable was not correctly configured to locate the installed Python executable.

Solutions and Improvements
The issue was resolved by systematically addressing the PATH configuration:

Disabling App Execution Aliases: The default Windows shortcuts that redirect the python command to the Microsoft Store were disabled in the "Manage app execution aliases" settings.

Correct Re-installation: Python was reinstalled, ensuring that the crucial checkbox "Add Python to PATH" was selected during the setup process. This correctly configured the system's environment variables.

After this, both python --version and pip --version commands executed successfully.

Outcome
By the end of Week 1, a fully functional and verified Python development environment was established, and a solid theoretical foundation for LSB steganography was in place.

Week 2: Project Scaffolding and File I/O
Objective
To create the project's foundational structure, including version control, and to implement the basic functions for loading and saving image files.

Process and Implementation
Version Control (Git & GitHub): A remote repository was created on GitHub to track project history and serve as a cloud backup. The repository was then cloned to a local development folder (D:\Projects\Steganography-Project-B.E-2025). This establishes a professional workflow and a safety net for the codebase.

File Structure: The main logic file, steganography.py, was created within the project directory.

Image I/O Functions: Using the Pillow library, two core functions were implemented: load_image and save_image.

# From steganography.py
from PIL import Image

def load_image(image_path):
    """
    Opens and loads an image from the specified path.
    """
    try:
        image = Image.open(image_path)
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

Challenges Faced
Several challenges related to the Git workflow were encountered:

Incorrect Working Directory: Initially, work was being done in a separate, manually created folder, not the one created by the git clone command. This meant Git was not tracking any of the changes.

Git Command Failure: When attempting to run git add ., the terminal returned a fatal: not a git repository error. This was because the terminal's active directory was D:\Projects and not the actual project folder D:\Projects\Steganography-Project-B.E-2025.

Solutions and Improvements
The workflow was corrected and refined:

Centralized Project Folder: All work was moved into the officially cloned Git repository folder.

Terminal Navigation: The process was clarified: before running any Git commands, it is essential to first navigate into the project directory using the cd (change directory) command. For example: cd Steganography-Project-B.E-2025. After this, Git commands worked as expected.

Successful Sync: The standard git add, git commit, and git push workflow was successfully executed, syncing the local code with the remote GitHub repository for the first time.

Outcome
A properly version-controlled project structure is now in place. The application has the fundamental ability to open an image from the disk into memory and save a modified image back to the disk.

Week 3: Core LSB Encoding
Objective
To implement the core logic for encoding a secret text message into a cover image using the LSB technique.

Process and Implementation
The encode_message function was developed. Its logic follows a precise sequence:

Message to Binary Conversion: The input string message is converted into a continuous string of bits. Each character is converted to its 8-bit ASCII representation.

Capacity Check: The function calculates the maximum storage capacity of the image (width x height x 3 bits) and verifies that the binary message will fit. If not, it raises an error.

Pixel Iteration and Embedding: The function iterates through each pixel of the image. For each pixel, it modifies the LSB of the Red, Green, and Blue values to match the next available bits from the secret message. This is achieved using bitwise operations: (color_value & 254) clears the LSB, and | message_bit sets it.

# From steganography.py - encode_message function
def encode_message(image, secret_message):
    width, height = image.size
    message_binary = ''.join(format(ord(char), '08b') for char in secret_message)
    
    max_bits = width * height * 3
    if len(message_binary) > max_bits:
        raise ValueError("Error: Message too large for image.")
        
    encoded_image = image.copy()
    pixel_map = encoded_image.load()
    data_index = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixel_map[x, y][:3] # Get original RGB

            # Modify Red channel
            if data_index < len(message_binary):
                r = (r & 254) | int(message_binary[data_index])
                data_index += 1
            # ... (similar logic for Green and Blue) ...

            pixel_map[x, y] = (r, g, b) # Update pixel
            # ... (code continues) ...

Challenges Faced
The initial implementation did not account for PNG images that contain an Alpha (transparency) channel (RGBA). The code assumed all pixels were RGB, which would cause an error when trying to unpack 4 values into 3 variables (r, g, b).

Solutions and Improvements
The encode_message function was made more robust by adding logic to handle both RGB and RGBA images:

The code now checks the format of each pixel.

It always reads just the first three (RGB) values for modification.

When writing the modified pixel back, it preserves the original Alpha channel if one was present. This prevents data loss and makes the function compatible with a wider range of PNG files.

Outcome
A functional encode_message function that can successfully embed a secret message into both RGB and RGBA images, creating a visually identical stego-image.

Week 4: Core LSB Decoding & Delimitation
Objective
To implement the logic to extract the hidden message from a stego-image and to introduce a mechanism to identify the end of the message.

Process and Implementation
End-of-File (EOF) Marker: To solve the problem of not knowing when the message ends, a unique 16-bit EOF marker (1111111111111110) was introduced. This marker is appended to the secret message before encoding.

Decoding Function (decode_message): This new function reverses the encoding process.

It iterates through the stego-image's pixels in the same order.

For each color channel (R, G, B), it extracts the LSB using the bitwise operation (color_value & 1).

It appends these bits to a string.

After every bit is extracted, it checks if the end of the string matches the EOF marker.

Once the marker is found, it removes the marker from the bitstream, converts the remaining bits back into characters (8 bits at a time), and returns the final message.

# From steganography.py - decode_message function
EOF_MARKER = '1111111111111110'

def decode_message(image):
    pixel_map = image.load()
    extracted_bits = ""
    
    for y in range(image.height):
        for x in range(image.width):
            pixel = pixel_map[x, y]
            for color_val in pixel[:3]:
                extracted_bits += str(color_val & 1)
                if extracted_bits.endswith(EOF_MARKER):
                    message_binary = extracted_bits[:-len(EOF_MARKER)]
                    # Convert binary back to text
                    message = ""
                    for i in range(0, len(message_binary), 8):
                        byte = message_binary[i:i+8]
                        message += chr(int(byte, 2))
                    return message
    return "No message found."

Challenges Faced
A minor challenge was ensuring file paths were handled correctly, especially on Windows where the backslash \ character can cause issues in strings.

Solutions and Improvements
During testing, "raw strings" (e.g., r'D:\path\to\file.png') were used for file paths. This tells Python to treat backslashes literally, preventing them from being misinterpreted as escape sequences and making the test script more reliable.

Outcome
The project now features a complete and working encode-decode cycle. A secret message can be successfully embedded into an image with an EOF marker and then perfectly retrieved from the resulting stego-image. The core logic of the steganography application is now complete.