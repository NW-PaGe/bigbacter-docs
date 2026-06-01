from wand.image import Image

with Image(filename="bigbacter_logo.png") as img:
    img.resize(256, 256)  # Resize to ICO-safe dimensions
    img.format = 'ico'
    img.save(filename="bigbacter_logo.ico")

