import cv2
import numpy as np
# from additionalrobustness import embed_watermark
from biterror_test import compare_files
from skimage.metrics import structural_similarity as ssim
original_img = cv2.imread('pic2.jpg')
# encoding = cv2.imread('logo.jpg')
alpha = 0.1


def conversion_dct(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    img = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)
    gray = thresholded
    gray = np.float32(gray)/255.0
    dct = cv2.dct(gray)
    return dct


def embed_watermark(img, watermark, alpha):

    # Resize the images to have the same shape
    watermark = cv2.resize(watermark, (img.shape[1], img.shape[0]))

    # Convert the image and the watermark to the frequency domain
    img_freq = conversion_dct(img)
    watermark_freq = conversion_dct(watermark)

    # Embed the watermark in the image frequency domain
    watermark_embedded_freq = (1 - alpha) * img_freq + alpha * watermark_freq

    # Convert the watermarked image back to the spatial domain
    watermark_embedded = cv2.idct(watermark_embedded_freq)

    # Save the watermarked image
    cv2.imwrite('watermarked_image.jpg', img)
    return watermark_embedded.astype(np.uint8)


# print(embed_watermark1(original_img, encoding, 0.1))


def embed_watermark1(img, alpha: float, encoding: str = 'My Watermark'):
    # Generate the watermark
    watermark = np.zeros((80, 80, 3), dtype=np.uint8)
    cv2.putText(watermark, encoding, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 255, 255))

    # Add alpha channel to the image and the watermark
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    # watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)

    # Get the dimensions of the watermark
    w, h, _ = watermark.shape

    # Define the region of interest (ROI) in the bottom-right corner of the image
    roi = img[-w:, -h:]

    # Add the watermark to the ROI using alpha blending

    blend = cv2.addWeighted(roi, 1-alpha, watermark, alpha, 0)

    # Lets do multiple blends
    # Replace the ROI with the blended image
    img[-w:, -h:] = blend

    # Save the watermarked image
    cv2.imwrite('watermarked_image2.png', img)

    # extract same image
    extracted_watermark = img[-w:, -h:]

    cv2.imwrite('extracted_watermark.png', extracted_watermark)
    # cv2.imwrite('extracted_watermark1.png', extracted_watermark1)

    comparison = watermark == extracted_watermark
    match_rate = comparison.mean()

    # return match_rate, img, extracted_watermark, extracted_watermark1, watermark
    return match_rate, img, extracted_watermark, watermark


results = embed_watermark1(original_img, 0.05)

# #cv2.imshow('Watermarked Image', results[1])
# cv2.imshow('Extracted Watermark', results[2])
# # cv2.imshow('Extracted Watermark2', results[3])
# cv2.imshow('Watermark', results[3])
# print('Watermark match rate: {:.2f}%'.format(results[0] * 100))
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# # # Extract the watermark from the watermarked image
# # extracted_watermark = img[-w:, -h:]

# # # Save the extracted watermarka
# # cv2.imwrite('extracted_watermark.png', extracted_watermark)


# def embed_watermark2(img, alpha: float, encoding: str = 'My Watermark'):
#     # Get image dimensions and calculate the center coordinates
#     height, width, channels = img.shape
#     center_x = int(width / 2)
#     center_y = int(height / 2)

#     # Define ROI as a rectangular region around the center coordinates
#     roi_width = int(width / 4)
#     roi_height = int(height / 4)
#     roi_top_left_x = center_x - int(roi_width / 2)
#     roi_top_left_y = center_y - int(roi_height / 2)
#     roi_bottom_right_x = roi_top_left_x + roi_width
#     roi_bottom_right_y = roi_top_left_y + roi_height

#     # Add watermark to the ROI
#     # Generate the watermark
#     watermark = np.zeros((100, 100, 4), dtype=np.uint8)
#     cv2.putText(watermark, encoding, (10, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255, 255), 2)
#     watermark = cv2.resize(watermark, (roi_width, roi_height))

#     alpha_channel = watermark[:, :, 3]
#     alpha_channel = cv2.cvtColor(alpha_channel, cv2.COLOR_GRAY2BGR)
#     alpha_channel = alpha_channel / 255.0
#     watermark = watermark[:, :, :3] * alpha_channel

#     # Embed watermark by replacing ROI with the watermarked data
#     img_with_watermark = img.copy()
#     img_with_watermark[roi_top_left_y:roi_bottom_right_y,
#                        roi_top_left_x:roi_bottom_right_x] = watermark
#     # img_with_watermark[roi_top_left_y:roi_bottom_right_y,
#     #                    roi_top_left_x:roi_bottom_right_x] = \
#     #     (1.0 - alpha_channel) * img[roi_top_left_y:roi_bottom_right_y,
#     #                                 roi_top_left_x:roi_bottom_right_x] + watermark
#     # Save watermarked image
#     cv2.imwrite('watermarked_image3.jpg', img_with_watermark)

#     extracted_watermark = img[roi_top_left_y:roi_bottom_right_y,
#                               roi_top_left_x:roi_bottom_right_x]
#     comparison = watermark == extracted_watermark
#     match_rate = comparison.mean()
#     return match_rate, img, extracted_watermark, img_with_watermark


# # results = embed_watermark2(original_img, 0.2)
# # Display results
def attacks(watermarked_img):
    # Define a list of attacks to apply to the watermarked image
    attacks = ['JPEG', 'Blur', 'Salt&Pepper', 'Rotation']

    # Iterate over the attacks and measure the robustness of the watermark
    for attack in attacks:
        # Apply the attack to the watermarked image
        if attack == 'JPEG':
            # Compress the image using JPEG with a quality factor of 50
            encoded_img, buffer = cv2.imencode('.jpg', watermarked_img, [
                cv2.IMWRITE_JPEG_QUALITY, 50])
            watermarked_img_compressed = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

        elif attack == 'Blur':
            # Apply a Gaussian blur with a kernel size of 3x3
            watermarked_img_blur = cv2.GaussianBlur(watermarked_img, (3, 3), 0)
        elif attack == 'Salt&Pepper':
            # Add salt and pepper noise with a noise level of 0.1
            noise = np.zeros(watermarked_img.shape, np.uint8)
            cv2.randu(noise, 0, 255)
            noise = cv2.cvtColor(noise, cv2.COLOR_BGR2GRAY)
            salt = noise > 255 * 0.9
            pepper = noise < 255 * 0.1
            watermarked_img[salt] = 255
            watermarked_img[pepper] = 0
            watermarked_img_noise = watermarked_img
        elif attack == 'Rotation':
            # Rotate the image by 45 degrees
            rows, cols, _ = watermarked_img.shape
            M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
            watermarked_img_rotation = cv2.warpAffine(
                watermarked_img, M, (cols, rows))

        return watermarked_img_compressed


def embed_watermark3(img, alpha: float, watermark_size: int, encoding: str):
    # Get image dimensions and calculate the center coordinates
    height, width, channels = img.shape
    center_x = int(width / 2)
    center_y = int(height / 2)

    # Define ROI as a rectangular region around the center coordinates
    roi_width = int(width / 4)
    roi_height = int(height / 4)
    roi_top_left_x = center_x - int(roi_width / 2)
    roi_top_left_y = center_y - int(roi_height / 2)
    roi_bottom_right_x = roi_top_left_x + roi_width
    roi_bottom_right_y = roi_top_left_y + roi_height

    # Generate random watermark and scale to match ROI dimensions
    watermark = np.zeros((roi_height, roi_width, 4), dtype=np.uint8)
    # watermark = np.random.rand(roi_height, roi_width, 3)
    cv2.putText(watermark, encoding, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255, 255), 1)
    watermark = cv2.resize(watermark, (watermark_size, watermark_size))

    # Reset
    roi_bottom_right_y = watermark_size + roi_top_left_y
    roi_bottom_right_x = watermark_size + roi_top_left_x

    # Add alpha channel to the image and the watermark
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    # watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)

    # Embed watermark by replacing ROI with the watermarked data
    img_with_watermark = img.copy()
    # breakpoint()
    img_with_watermark[roi_top_left_y:roi_bottom_right_y,
                       roi_top_left_x: roi_bottom_right_x] = watermark

    # Extract watermark by selecting ROI and comparing with original data
   # img_with_watermark = attacks(img_with_watermark)[1]

    extracted_watermark = img_with_watermark[roi_top_left_y:
                                             roi_bottom_right_y,
                                             roi_top_left_x:
                                             roi_bottom_right_x]

    cv2.imwrite('extracted_watermark.png', extracted_watermark)
    cv2.imwrite('watermark.png', watermark)
    cv2.imwrite('img_with_watermark.png', img_with_watermark)

    comparison = watermark == extracted_watermark
    print("Here")
    match_rate = comparison.mean()
    # breakpoint()
    return match_rate, img, extracted_watermark, img_with_watermark, watermark


# here we setting up the fundementals for
watermark_bit1 = 100
watermark_bit2 = 100
a = embed_watermark3(original_img, 0.2, watermark_bit1,
                     "My Watermark")
b = embed_watermark3(original_img, 0.1, watermark_bit2, "My Watermark")


def bit_rate_error(watermark_bit1, watermark_bit2):

    # initiate
    n_errors = 0

    for i in range(min(watermark_bit1, watermark_bit2)-1):
        # breakpoint()

        if np.sum(a[2][i]) != np.sum(b[2][i]):
            n_errors += 1
            bit_rate_error = float(n_errors) / \
                min(watermark_bit1, watermark_bit2)

        if np.sum(a[2]) == np.sum(b[2]):
            bit_rate_error = 0

        check = np.sum(b[2])/np.sum(a[2])
    return (print(f'bit_rate_error is : {bit_rate_error}'), print(f'check of value {check}'))


bit_rate_error(watermark_bit1, watermark_bit2)


def evaluate(original_img, watermarked_img):
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


evaluate(a[2], b[2])

# breakpoint()
# if comparison == False:
#     print("Watermark match rate: 0%")
# else:
#     match_rate = comparison.mean()
#     print('Watermark match rate: {:.2f}%'.format(match_rate * 100))

# # use bit_rate error now
# cv2.imwrite('extracted_a.png', a[2])
# cv2.imwrite('extracted_b.png', b[2])

# compare_files('extracted_a.png', 'extracted_a.png')
# results = embed_watermark3(original_img, 0.2, 10)
# # cv2.imshow('Original Image', results[1])
# # cv2.imshow('Watermarked Image', results[3])
# cv2.imshow('Extracted Watermark', results[2])
# cv2.imshow('Watermark', results[4]da)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
