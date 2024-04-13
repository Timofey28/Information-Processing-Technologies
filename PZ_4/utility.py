def print_length_amounts(black_pixel_lengths):
    length_amounts = dict()
    for row in black_pixel_lengths:
        if len(row) in length_amounts:
            length_amounts[len(row)] += 1
        else:
            length_amounts[len(row)] = 1
    for key, value in length_amounts.items():
        print(f'{key}: {value} times')