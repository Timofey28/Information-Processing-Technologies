import cv2 as cv
from .load_env import get_data



def print_length_amounts(black_pixel_lengths: list[list[int]]) -> None:
    length_amounts = dict()
    for row in black_pixel_lengths:
        if len(row) in length_amounts:
            length_amounts[len(row)] += 1
        else:
            length_amounts[len(row)] = 1
    for key, value in length_amounts.items():
        print(f'{key}: {value} times')


def print_image_chb(img_path: str):
    # Load an image
    img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)

    # Apply thresholding
    BINARY_THRESHOLD = int(get_data('BINARY_THRESHOLD'))
    _, img = cv.threshold(img, BINARY_THRESHOLD, 255, cv.THRESH_BINARY)

    # Display the image
    cv.imshow('Thresholded Image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()