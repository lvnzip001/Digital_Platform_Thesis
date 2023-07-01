import cv2
import numpy as np

# Load the original image and the watermarked image
original_img = cv2.imread('original_image.png')
watermarked_img = cv2.imread('watermarked_image.png')


# Define a list of attacks to apply to the watermarked image
attacks = ['JPEG', 'Blur', 'Salt&Pepper', 'Rotation']

# Iterate over the attacks and measure the robustness of the watermark
for attack in attacks:
    # Apply the attack to the watermarked image
    if attack == 'JPEG':
        # Compress the image using JPEG with a quality factor of 50
        encoded_img, buffer = cv2.imencode('.jpg', watermarked_img, [
                                           cv2.IMWRITE_JPEG_QUALITY, 50])
        watermarked_img = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    elif attack == 'Blur':
        # Apply a Gaussian blur with a kernel size of 3x3
        watermarked_img = cv2.GaussianBlur(watermarked_img, (3, 3), 0)
    elif attack == 'Salt&Pepper':
        # Add salt and pepper noise with a noise level of 0.1
        noise = np.zeros(watermarked_img.shape, np.uint8)
        cv2.randu(noise, 0, 255)
        noise = cv2.cvtColor(noise, cv2.COLOR_BGR2GRAY)
        salt = noise > 255 * 0.9
        pepper = noise < 255 * 0.1
        watermarked_img[salt] = 255
        watermarked_img[pepper] = 0
    elif attack == 'Rotation':
        # Rotate the image by 45 degrees
        rows, cols, _ = watermarked_img.shape
        M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
        watermarked_img = cv2.warpAffine(watermarked_img, M, (cols, rows))

    # Extract the watermark from the attacked image
    extracted_watermark = cv2.dct(watermarked_img[:, :, 0])

    # Compare the extracted watermark to the original watermark
    similarity = compare_watermarks(original_watermark, extracted_watermark)

    # Print the similarity score for the current attack
    print(f"Similarity score after {attack} attack: {similarity}")


"""This code applies four different attacks to the watermarked image 
    - JPEG compression, 
    - Gaussian blur, 
    - salt and pepper noise, 
    - rotation.
    
    It evaluates the similarity between the extracted watermark and 
the original watermark using a custom compare_watermarks function."""