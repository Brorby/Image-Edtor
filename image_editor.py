from PIL import Image, ImageEnhance, ImageFilter
import os

# Function to apply a sepia filter
def apply_sepia(image):
    width, height = image.size
    pixels = image.load()

    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))

            # Apply sepia filter
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            if tr > 255:
                tr = 255
            if tg > 255:
                tg = 255
            if tb > 255:
                tb = 255

            pixels[px, py] = (tr, tg, tb)

    return image

# Function to add a slight blur and noise for an analogue look
def apply_analogue_effect(image):
    image = image.filter(ImageFilter.GaussianBlur(1))  # Slight blur
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(0.85)  # Reduce contrast slightly

    # Adding grain (noise)
    px = image.load()
    width, height = image.size
    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))
            noise = int((os.urandom(1)[0] - 128) / 64)  # Adding random noise
            r = max(0, min(r + noise, 255))
            g = max(0, min(g + noise, 255))
            b = max(0, min(b + noise, 255))
            image.putpixel((px, py), (r, g, b))

    return image

# Ask the user for their preferences
bw_input = input("Do you want it to be black and white? (yes or no): ").lower()
analogue_input = input("Do you want it to look like it was taken with an analogue camera from 1980? (yes or no): ").lower()

path = './images'
pathOut = './editedImages'

if not os.path.exists(pathOut):
    os.makedirs(pathOut)

for filename in os.listdir(path):
    if filename.endswith("JPG") or filename.endswith("jpg"):
        img = Image.open(f"{path}/{filename}")

        # Apply sepia and analogue effects if user chose "yes"
        if analogue_input == 'yes':
            img = apply_sepia(img)
            img = apply_analogue_effect(img)

        # Convert to black and white if user chose "yes"
        if bw_input == 'yes':
            img = img.convert('L')
        
        clean_name = os.path.splitext(filename)[0]
        img.save(f"{pathOut}/{clean_name}_edited.jpg")

print("Image editing completed.")
