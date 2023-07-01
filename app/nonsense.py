import cv2
import numpy as np

# Define the path of the input and output images
input_image_path = 'pic2.jpg'
output_image_path = 'output_image.png'

# Define the watermark text
watermark_text = 'Watermark'

# Load the input image
img = cv2.imread(input_image_path)

# Define the font properties
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2

# Get the size of the watermark text
text_size, _ = cv2.getTextSize(
    watermark_text, font, font_scale, font_thickness)

# Calculate the position to place the watermark text
x = img.shape[1] - text_size[0] - 10
y = img.shape[0] - text_size[1] - 10

# Add the watermark text to the image
cv2.putText(img, watermark_text, (x, y), font, font_scale,
            (255, 255, 255), font_thickness, cv2.LINE_AA)

# Save the watermarked image to the output path
cv2.imwrite(output_image_path, img)

# Load the watermarked image
watermarked_img = cv2.imread(output_image_path)

# Extract the watermark by subtracting the original image from the watermarked image
watermark = cv2.subtract(watermarked_img, img)

# Save the extracted watermark to a file
cv2.imwrite('extracted_watermark.png', watermark)
