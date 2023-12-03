from collections import defaultdict
from itertools import product

from run_util import run_puzzle


def parse_data(input):
    symbols = dict()
    neighbors = defaultdict(list)
    digits = dict()

    for y, row in enumerate(input.split('\n')):
        for x, c in enumerate(row):
            if c == '.':
                continue
            if c.isdigit():
                digits[(x, y)] = c
            else:  # symbol
                symbols[(x, y)] = c

    for number, parts in get_numbers(digits):
        possible_connected_symbols = {(x + d_x, y + d_y) for (x, y), d_x, d_y in product(parts, [-1, 0, 1], [-1, 0, 1])}
        for neighbor in possible_connected_symbols.intersection(symbols):
            neighbors[neighbor].append(number)

    return symbols, neighbors


def get_numbers(digits):
    numbers = []
    seen = set()
    for (x, y), digit in digits.items():
        if (x, y) in seen:
            continue
        parts = {(x, y)}
        d_x = 1
        number = digit
        while (x + d_x, y) in digits:
            parts.add((x + d_x, y))
            number += digits[(x + d_x, y)]
            d_x += 1

        seen.update(parts)
        numbers.append((int(number), parts))
    return numbers


def part_a(data):
    symbols, neighbors = parse_data(data)

    return sum(
        sum(neighbors[symbol])
        for symbol in symbols
    )


def part_b(data):
    symbols, neighbors = parse_data(data)

    return sum(
        neighbors[symbol][0] * neighbors[symbol][1]
        for symbol, symbol_type in symbols.items()
        if symbol_type == '*' and len(neighbors[symbol]) == 2
    )


def main():
    examples = [
        ("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""", 4361, 467835)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
