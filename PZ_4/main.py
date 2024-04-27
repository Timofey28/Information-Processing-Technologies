import os
import cv2 as cv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from utils import *


photos_folder = 'photos'

# result = {
#     'vertical': pd.DataFrame(columns=['mean', 'std', '10th', '90th']),
#     'horizontal': pd.DataFrame(columns=['mean', 'std', '10th', '90th']),
#     'diagonal': pd.DataFrame(columns=['mean', 'std', '10th', '90th'])
# }

# for folder_name in os.listdir(photos_folder):
#     dpi = load_dpi_for(folder_name)
#     df = pd.DataFrame(columns=['mean', 'std', '10th', '90th'])

#     print(f'Processing {folder_name}...')

#     for photo in os.listdir(os.path.join(photos_folder, folder_name)):
#         type, ideal_size = get_photo_type_and_size_by_filename(photo)
#         if type is None:
#             continue
        
#         print(f'\tProcessing {photo}...')
#         widths = calculate_widths(os.path.join(photos_folder, folder_name, photo), dpi)
#         statistical_data = calculate_statistical_data(widths, ideal_size)
#         assert type in ['vertical', 'horizontal', 'diagonal']
#         result[type].loc[len(result[type].index)] = statistical_data

# # Write the data to a .csv files
# if not os.path.exists('data'):
#     os.mkdir('data')
# for photo_type, df in result.items():
#     df.to_csv(f'data/{photo_type}.csv', index=False)


data = read_data()

for group_name, df in data.items():
    plt.figure()
    match group_name:
        case 'vertical':
            title = 'Вертикальное'
        case 'horizontal':
            title = 'Горизонтальное'
        case 'diagonal':
            title = 'Диагональное'
    plt.title(title + ' расположение')
    plt.plot(df['mean'], label='Математическое ожидание')
    plt.plot(df['std'], label='Стандартное отклонение')
    plt.xlabel('Номер фотографии')
    plt.ylabel('Разн. между идеал. и факт. шириной, мм')
    plt.legend()
    plt.grid()
    plt.show()