import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from utility import print_length_amounts
from config import MAX_ERROR, DPI, BINARY_THRESHOLD

# Load an image
img = cv.imread('055_vert.bmp', cv.IMREAD_GRAYSCALE)

# Apply thresholding
_, img = cv.threshold(img, BINARY_THRESHOLD, 255, cv.THRESH_BINARY)

# Display the image
# cv.imshow('Thresholded Image', img)
# cv.waitKey(0)
# cv.destroyAllWindows()

# Initialize an empty list to store lengths of black pixels
black_pixel_lengths = []

# Iterate over each row in the image
for row in img:
    # Initialize a counter for black pixels
    black_pixel_count = 0
    # Initialize an empty list to store lengths of black pixels in the current row
    row_black_pixel_lengths = []
    # Initialize a counter for white pixels
    white_pixel_count = 0

    # Iterate over each pixel in the row
    for pixel in row:
        # If the pixel is black, increment the black counter
        if pixel == 0:
            black_pixel_count += 1
            # If there was a sequence of white pixels before it and it's less than MAX_ERROR, consider them as black
            if white_pixel_count > 0 and white_pixel_count <= MAX_ERROR:
                black_pixel_count += white_pixel_count
                white_pixel_count = 0
        # If the pixel is white, increment the white counter
        else:
            white_pixel_count += 1
            # If there was a sequence of black pixels before it, store the length of the sequence
            if black_pixel_count > 0:
                row_black_pixel_lengths.append(black_pixel_count)
                black_pixel_count = 0

    # If the last pixel in the row was black, store the length of the sequence
    if black_pixel_count > 0:
        row_black_pixel_lengths.append(black_pixel_count)

    # Filter out lengths that are less than or equal to MAX_ERROR and add them to the main list
    black_pixel_lengths.append([length for length in row_black_pixel_lengths if length > MAX_ERROR])

# # Print the lengths of black pixels
# print('Before filtering:')
# print_length_amounts(black_pixel_lengths)

conductors_in_row = min([len(row) for row in black_pixel_lengths])
for row_lengths in black_pixel_lengths:
    while len(row_lengths) > conductors_in_row:
        row_lengths.remove(min(row_lengths))

# # Print the lengths of black pixels
# print('After filtering:')
# print_length_amounts(black_pixel_lengths)

# Combine all lengths into one list
all_pixel_lengths = []
for row_lengths in black_pixel_lengths:
    all_pixel_lengths.extend(row_lengths)

# Convert lengths from pixel to mm
all_mm_lengths = [length / (DPI / 25.4) for length in all_pixel_lengths]

# Calculate expected value and standard deviation
expected_value = np.mean(all_mm_lengths)
standard_deviation = np.std(all_mm_lengths)
print(f'Expected value: {expected_value:.2f} mm')
print(f'Standard deviation: {standard_deviation:.2f} mm')

# Calculate 10 and 90 percentiles
percentile_10 = np.percentile(all_mm_lengths, 10)
percentile_90 = np.percentile(all_mm_lengths, 90)
print(f'10th percentile: {percentile_10:.2f} mm')
print(f'90th percentile: {percentile_90:.2f} mm')

# Plot histogram of black pixel lengths
plt.hist(all_mm_lengths, color='black')
plt.xlabel('Длина проводника, мм')
plt.ylabel('Частота встречаемости')
plt.title('Гистограмма длин проводников')
plt.show()