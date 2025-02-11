from PIL import Image

# Function to encode a message into an image
def encode_message(image_path, message):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Check if message can fit in the image
    if len(binary_message) > width * height * 3:
        raise ValueError("Message too large to encode in the image")

    index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Encode binary data into the least significant bit of each color pixel
            if index < len(binary_message):
                pixels[x, y] = (r & 254 | int(binary_message[index]), g & 254 | int(binary_message[index + 1]), b & 254 | int(binary_message[index + 2]))
                index += 3
            else:
                img.save("encoded_image.png")
                return

    img.save("encoded_image.png")

# Function to decode a message from an image
def decode_message(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    binary_message = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Extract least significant bit from each color pixel
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

    # Convert binary message back to string
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))

        # Stop decoding if reaching the end of the message
        if message[-1] == '\x00':
            break

    return message.rstrip('\x00')

# Example usage:
# Encode a message into an image
image_path = "example.png"
message_to_encode = "Hello, this is a secret message!"
encode_message(image_path, message_to_encode)

# Decode the message from the encoded image
decoded_message = decode_message("encoded_image.png")
print("Decoded message:", decoded_message)