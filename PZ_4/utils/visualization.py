import matplotlib.pyplot as plt


def plot_histogram(values: list[int]) -> None:
    plt.hist(values, bins=20, color='black')
    plt.xlabel('Длина проводника, мм')
    plt.ylabel('Частота встречаемости')
    plt.title('Гистограмма длин проводников')
    plt.show()