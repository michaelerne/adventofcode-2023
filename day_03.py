from run_util import run_puzzle
from collections import defaultdict
from itertools import product


def parse_data(input):
    symbols = set()
    gears = set()
    digits = dict()
    for y, row in enumerate(input.split('\n')):
        for x, c in enumerate(row):
            if c == '.':
                continue
            if c.isdigit():
                digits[(x, y)] = c
            else:  # symbol
                symbols.add((x, y))
                if c == '*':
                    gears.add((x, y))

    return digits, symbols, gears


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
    digits, symbols, _gears = parse_data(data)

    numbers = get_numbers(digits)

    solution = 0

    for number, parts in numbers:
        for (x, y) in parts:
            if any([(x + d_x, y + d_y) in symbols for d_x in [-1, 0, 1] for d_y in [-1, 0, 1]]):
                solution += number
                break

    return solution


def part_b(data):
    digits, _symbols, gears = parse_data(data)

    numbers = get_numbers(digits)

    solution = 0

    gear_numbers = defaultdict(list)

    for number, parts in numbers:
        for (x, y), d_x, d_y in product(parts, [-1, 0, 1], [-1, 0, 1]):
            if (x + d_x, y + d_y) in gears:
                gear_numbers[(x + d_x, y + d_y)].append(number)
                break

    for numbers in gear_numbers.values():
        if len(numbers) == 2:
            solution += numbers[0] * numbers[1]

    return solution


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
