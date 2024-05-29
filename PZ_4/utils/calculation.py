import os
import cv2 as cv
import pandas as pd
import numpy as np
from .debug import print_length_amounts
from .load_env import get_data

def calculate_widths(photo_path: str, dpi: int, inverted: bool, verbose=False) -> list[float]:
    # Load data from the environment
    MAX_ERROR = int(get_data('MAX_ERROR'))
    BINARY_THRESHOLD = int(get_data('BINARY_THRESHOLD'))

    # Если цвета инвертированы, проводники на фотках белого цвета (т.е. 255)
    conductor_color = 255 if inverted else 0

    # Load an image
    img = cv.imread(photo_path, cv.IMREAD_GRAYSCALE)

    # Apply thresholding
    _, img = cv.threshold(img, BINARY_THRESHOLD, 255, cv.THRESH_BINARY)

    if verbose:
        # Display the image
        cv.imshow('Thresholded Image', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Initialize an empty list to store lengths of black pixels
    black_pixel_lengths = []

    # Iterate over each row in the image
    for row in img:
        black_pixel_count = 0
        row_black_pixel_lengths = []
        white_pixel_count = 0

        for pixel in row:
            if pixel == conductor_color:
                black_pixel_count += 1
                if white_pixel_count > 0 and white_pixel_count <= MAX_ERROR:
                    black_pixel_count += white_pixel_count
                    white_pixel_count = 0
            else:
                white_pixel_count += 1
                if black_pixel_count > 0:
                    row_black_pixel_lengths.append(black_pixel_count)
                    black_pixel_count = 0

        # If the last pixel in the row was black, store the length of the sequence
        if black_pixel_count > 0:
            row_black_pixel_lengths.append(black_pixel_count)

        # Filter out lengths that are less than or equal to MAX_ERROR and add them to the main list
        black_pixel_lengths.append([length for length in row_black_pixel_lengths if length > MAX_ERROR])

    if verbose:
        # Print the lengths of black pixels
        print('Before filtering:')
        print_length_amounts(black_pixel_lengths)

    conductors_in_row = np.bincount([len(row) for row in black_pixel_lengths]).argmax()
    for row_lengths in black_pixel_lengths:
        while len(row_lengths) > conductors_in_row:
            row_lengths.remove(min(row_lengths))

    if verbose:
        # Print the lengths of black pixels
        print('After filtering:')
        print_length_amounts(black_pixel_lengths)

    # Combine all lengths into one list
    all_pixel_lengths = []
    for row_lengths in black_pixel_lengths:
        all_pixel_lengths.extend(row_lengths)

    all_mm_lengths = [length / (dpi / 25.4) for length in all_pixel_lengths]
    return all_mm_lengths

def calculate_statistical_data(sample: list[int], ideal_size, photo: str, inverted: bool) -> list[int]:
    # Считаем мат. ожидание и ст. отклонение разницы между идеальным размером и полученным
    sample = [abs(ideal_size - length) for length in sample]
    expected_value = np.mean(sample)
    standard_deviation = np.std(sample)
    # print(f'Expected value: {expected_value:.2f} mm')
    # print(f'Standard deviation: {standard_deviation:.2f} mm')

    # Calculate 10 and 90 percentiles
    percentile_10 = np.percentile(sample, 10)
    percentile_90 = np.percentile(sample, 90)
    # print(f'10th percentile: {percentile_10:.2f} mm')
    # print(f'90th percentile: {percentile_90:.2f} mm')
    type = 'shablon' if inverted else 'provodnik'

    return [expected_value, standard_deviation, percentile_10, percentile_90, ideal_size, photo, type]

def read_data() -> dict[str, pd.DataFrame]:
    data_folder = 'data'
    result = dict()
    for file in os.listdir(data_folder):
        df = pd.read_csv(os.path.join(data_folder, file), sep=';')
        result[file.removesuffix('.csv')] = df
    return result

def load_dpi_for(folder_name: str) -> int:
    if 'dip_ecsp' in folder_name:
        return int(get_data('DPI_DIP_ECSP'))
    elif 'ph_for_exp' in folder_name:
        return int(get_data('DPI_PH_FOR_EXP'))
    elif 'ecsp_plate_lit_cond' in folder_name:
        return int(get_data('DPI_ECSP_PLATE_LIT_COND'))
    else:
        return -1
    
def get_photo_type_and_size_by_filename(file_name: str) -> tuple[str | None, float | None]:
    if ' ' in file_name or 'test' in file_name or not file_name.endswith('.bmp'):
        return None, None
    file_name = file_name[:file_name.rfind('.')]
    try:
        value, _, type = file_name.partition('_')
        value = value[:1] + '.' + value[1:]
        value = float(value)
        if 'vert' in type:
            type = 'vertical'
        elif 'gor' in type:
            type = 'horizontal'
        elif 'ang' in type:
            type = 'diagonal'
        else:
            return None, None
        return type, value
    except ValueError:
        return None, None