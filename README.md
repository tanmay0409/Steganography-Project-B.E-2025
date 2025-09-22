# Secure Data Hiding in Images using Enhanced LSB Steganography

This project is a Python-based application that implements steganography using the Least Significant Bit (LSB) technique to hide secret messages inside images. It serves as a proof-of-concept for Digital Software Provenance, providing a method to embed invisible digital fingerprints into software assets for tracing and authentication.

## How It Works

The application performs two core functions:

1.  **Encoding:**
    * A secret text message is converted into a binary string.
    * A unique End-of-File (EOF) marker is appended to the binary data to signal the end of the message.
    * The application iterates through the pixels of a cover image (PNG) and replaces the least significant bit of each color channel (Red, Green, Blue) with a bit from the message.
    * The resulting stego-image, which is visually identical to the original, is saved.

2.  **Decoding:**
    * The application reads the stego-image and extracts the least significant bit from each color channel in the correct order.
    * It reconstructs the binary string until it detects the EOF marker.
    * The binary string is then converted back into text to reveal the original secret message.

## Current Features
* Core LSB encoding and decoding for text messages.
* Support for both RGB and RGBA (with transparency) PNG images.
* Robust message delimitation using a unique EOF marker.
* Command-line interface for performing the encode/decode cycle.