from itertools import combinations

from run_util import run_puzzle


def parse_data(data):
    lines = data.split('\n')
    galaxies = []
    x_has_galaxy = [False] * len(lines[0])
    y_has_galaxy = [False] * len(lines)

    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char == '#':
                galaxies.append((x, y))
                x_has_galaxy[x] = True
                y_has_galaxy[y] = True

    x_has_no_galaxy = [not has_galaxy for has_galaxy in x_has_galaxy]
    y_has_no_galaxy = [not has_galaxy for has_galaxy in y_has_galaxy]

    return galaxies, x_has_no_galaxy, y_has_no_galaxy


def part_a(data):
    galaxies, x_has_no_galaxy, y_has_no_galaxy = parse_data(data)

    solution = 0
    for (x_1, y_1), (x_2, y_2) in combinations(galaxies, 2):

        x_1, x_2 = min(x_1, x_2), max(x_1, x_2)
        y_1, y_2 = min(y_1, y_2), max(y_1, y_2)

        count = x_2 - x_1 + sum(x_has_no_galaxy[x_1:x_2 + 1])
        count += y_2 - y_1 + sum(y_has_no_galaxy[y_1:y_2 + 1])

        solution += count

    return solution


def part_b(data):
    galaxies, x_has_no_galaxy, y_has_no_galaxy = parse_data(data)
    solution = 0
    for (x_1, y_1), (x_2, y_2) in combinations(galaxies, 2):

        x_1, x_2 = min(x_1, x_2), max(x_1, x_2)
        y_1, y_2 = min(y_1, y_2), max(y_1, y_2)

        count = x_2 - x_1 + sum(x_has_no_galaxy[x_1:x_2 + 1]) * (1000000 - 1)
        count += y_2 - y_1 + sum(y_has_no_galaxy[y_1:y_2 + 1]) * (1000000 - 1)

        solution += count

    return solution

def main():
    examples = [
        ("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""", 374, 82000210)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
