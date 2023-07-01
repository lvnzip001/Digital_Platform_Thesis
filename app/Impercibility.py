import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Load the original image and the watermarked image
original_img = cv2.imread('original_image.png')
watermarked_img = cv2.imread('watermarked_image.png')

# Define a list of image quality metrics to compute
metrics = ['PSNR', 'SSIM', 'MSE']

# Compute the metrics for the watermarked image
for metric in metrics:
    if metric == 'PSNR':
        # Compute the peak signal-to-noise ratio (PSNR)
        mse = np.mean((original_img - watermarked_img) ** 2)
        psnr = 10 * np.log10(255 ** 2 / mse)
        print(f"PSNR: {psnr}")
    elif metric == 'SSIM':
        # Compute the structural similarity index (SSIM)
        ssim_score = ssim(cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY), cv2.cvtColor(
            watermarked_img, cv2.COLOR_BGR2GRAY), data_range=255)
        print(f"SSIM: {ssim_score}")
    elif metric == 'MSE':
        # Compute the mean squared error (MSE)
        mse = np.mean((original_img - watermarked_img) ** 2)
        print(f"MSE: {mse}")


"""This code computes three common image quality metrics for the watermarked image:
        -   peak signal-to-noise ratio (PSNR),
        -   structural similarity index (SSIM),
        -   mean squared error (MSE).

Use to evaluate the imperceptibility of a watermark.
"""