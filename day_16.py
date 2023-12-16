from collections import deque
from multiprocessing.pool import Pool

from run_util import run_puzzle

MOVES = {
    '.': {'E': 'E', 'N': 'N', 'S': 'S', 'W': 'W'},
    '-': {'E': 'E', 'N': 'EW', 'S': 'EW', 'W': 'W'},
    '|': {'E': 'NS', 'N': 'N', 'S': 'S', 'W': 'NS'},
    '/': {'E': 'N', 'N': 'E', 'S': 'W', 'W': 'S'},
    '\\': {'E': 'S', 'N': 'W', 'S': 'E', 'W': 'N'}
}

DIRECTIONS = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}


def parse_data(data):
    grid = [[cell for cell in row] for row in data.split('\n')]
    return grid


def run(grid, start):
    max_x, max_y = len(grid[0]), len(grid)

    beams = deque([start])
    seen = set()
    energized = set()

    while beams:
        (x, y, direction) = beams.pop()
        d_x, d_y = DIRECTIONS[direction]
        x, y = x + d_x, y + d_y

        if not (0 <= x < max_x and 0 <= y < max_y):
            continue

        for direction in MOVES[grid[x][y]][direction]:
            if (x, y, direction) in seen:
                continue

            seen.add((x, y, direction))
            energized.add((x, y))
            beams.append((x, y, direction))

    return len(energized)


def part_a(data):
    grid = parse_data(data)

    return run(grid, (0, -1, "E"))


def part_b(data):
    grid = parse_data(data)

    max_x, max_y = len(grid[0]), len(grid)

    starts = [(grid, (y, -1, 'E')) for y in range(max_y)]
    starts += [(grid, (y, max_x, 'W')) for y in range(max_y)]
    starts += [(grid, (-1, x, 'S')) for x in range(max_x)]
    starts += [(grid, (max_y, x, 'N')) for x in range(max_x)]

    with Pool(8) as pool:
        runs = pool.starmap(run, starts)

    return max(runs)


def main():
    examples = [
        (r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""", 46, 51)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
