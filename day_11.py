from itertools import combinations

from run_util import run_puzzle


def parse_data(data, expand):
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

    x_expand = {x for x, has_galaxy in enumerate(x_has_galaxy) if not has_galaxy}
    y_expand = {y for y, has_galaxy in enumerate(y_has_galaxy) if not has_galaxy}

    expanded_galaxies = [
        (
            x + sum(expand for row in x_expand if row < x),
            y + sum(expand for col in y_expand if col < y)
        )
        for x, y in galaxies
    ]

    return expanded_galaxies


def part_a(data):
    expanded_galaxies = parse_data(data, 1)

    return sum(
        abs(x_1 - x_2) + abs(y_1 - y_2)
        for (x_1, y_1), (x_2, y_2) in combinations(expanded_galaxies, 2)
    )


def part_b(data):
    expanded_galaxies = parse_data(data, 999999)

    return sum(
        abs(x_1 - x_2) + abs(y_1 - y_2)
        for (x_1, y_1), (x_2, y_2) in combinations(expanded_galaxies, 2)
    )


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
