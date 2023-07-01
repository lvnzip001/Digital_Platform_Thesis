import cv2
import numpy as np

# from skimage.measure import compare_ssim as ssim

# Watermarking function


def embed_watermark(img, watermark, alpha):
    # Convert the image and the watermark to the frequency domain

    img_freq = cv2.dct(img.astype(np.float32))
    watermark_freq = cv2.dct(watermark.astype(np.float32))

    # Embed the watermark in the image frequency domain
    watermark_embedded_freq = (1 - alpha) * img_freq + alpha * watermark_freq

    # Convert the watermarked image back to the spatial domain
    watermark_embedded = cv2.idct(watermark_embedded_freq)

    return watermark_embedded.astype(np.uint8)


# Load the original image and the watermark
original_img = cv2.imread('original_image.png')
watermark = cv2.imread('watermark.png', cv2.IMREAD_GRAYSCALE)

# Watermark the image
alpha = 0.1
watermarked_img = embed_watermark(original_img, watermark, alpha)

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
    extracted_watermark_freq = cv2.dct(watermarked_img[:, :, 0])
    extracted_watermark = np.round(extracted_watermark_freq).astype(np.uint8)

    # Compare the extracted watermark to the original watermark
    ssim_score = ssim(watermark, extracted_watermark,
                      data_range=watermark.max() - watermark.min())

    # Print the similarity score for the current attack
    print(f"Similarity score after {attack} attack: {ssim_score}")
