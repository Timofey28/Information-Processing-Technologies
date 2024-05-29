import os
import cv2 as cv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import shutil
from utils import *


# path = 'photos/ph_for_exp_big/040_gor.bmp'
# print_image_chb(path)


photos_folder = 'photos'
selected_photos_folder = 'selected_photos'


result = {
    'vertical': pd.DataFrame(columns=['mean', 'std', '10th', '90th', 'ideal_size', 'photo', 'type']),
    'horizontal': pd.DataFrame(columns=['mean', 'std', '10th', '90th', 'ideal_size', 'photo', 'type']),
    'diagonal': pd.DataFrame(columns=['mean', 'std', '10th', '90th', 'ideal_size', 'photo', 'type'])
}

amount_vert = 0
amount_diag = 0
amount_hori = 0

for folder_name in os.listdir(photos_folder):
    dpi = load_dpi_for(folder_name)
    # df = pd.DataFrame(columns=['mean', 'std', '10th', '90th', 'ideal_size'])

    print(f'Processing {folder_name}...')

    for photo in os.listdir(os.path.join(photos_folder, folder_name)):
        type, ideal_size = get_photo_type_and_size_by_filename(photo)
        if type is None:
            continue
        assert type in ['vertical', 'horizontal', 'diagonal']

        match type:
            case 'vertical':
                amount_vert += 1
            case 'diagonal':
                amount_diag += 1
            case 'horizontal':
                amount_hori += 1
        # shutil.copy(os.path.join(photos_folder, folder_name, photo), os.path.join(selected_photos_folder, type))

        print(f'\tProcessing {photo}... (ideal size: {ideal_size}', end='')
        inverted = True if folder_name.startswith('ph') else False
        print(f', inverted)' if inverted else ')')
        widths = calculate_widths(os.path.join(photos_folder, folder_name, photo), dpi, inverted)
        path_to_photo = os.path.join(photos_folder, folder_name, photo).replace('\\', '/')
        statistical_data = calculate_statistical_data(widths, ideal_size, path_to_photo, inverted)
        result[type].loc[len(result[type].index)] = statistical_data

# Write the data to a .csv files
if not os.path.exists('data'):
    os.mkdir('data')
for photo_type, df in result.items():
    df.to_csv(f'data/{photo_type}.csv', index=False, sep=';')

print(f'{amount_vert = }')
print(f'{amount_hori = }')
print(f'{amount_diag = }')


# data = read_data()

# title = None
# for group_name, df in data.items():
#     plt.figure()
#     match group_name:
#         case 'vertical':
#             title = 'Вертикальное'
#         case 'horizontal':
#             title = 'Горизонтальное'
#         case 'diagonal':
#             title = 'Диагональное'

#     # Для показа запятых вместо точек в числах на осях графика
#     import locale
#     locale.setlocale(locale.LC_NUMERIC, "ru_RU.utf-8")
#     plt.rcdefaults()
#     plt.rcParams['axes.formatter.use_locale'] = True

#     plt.title(title + ' расположение')
#     plt.plot(df['mean'], label='Математическое ожидание')
#     plt.plot(df['std'], label='Стандартное отклонение')
#     plt.xlabel('Номер фотографии')
#     plt.ylabel('Разн. между идеал. и факт. шириной, мм')
#     plt.legend()
#     plt.grid()
#     plt.show()

