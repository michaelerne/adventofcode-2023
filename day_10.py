import math

from run_util import run_puzzle
from collections import deque
from typing import Dict, Tuple, List, Set

DIRECTIONS = {
    ('N', '|'): 'N',
    ('N', 'F'): 'E',
    ('N', '7'): 'W',
    ('E', '-'): 'E',
    ('E', 'J'): 'N',
    ('E', '7'): 'S',
    ('S', '|'): 'S',
    ('S', 'J'): 'W',
    ('S', 'L'): 'E',
    ('W', '-'): 'W',
    ('W', 'L'): 'N',
    ('W', 'F'): 'S'
}

D_X = {'N': 0, 'E': 1, 'S': 0, 'W': -1}
D_Y = {'N': -1, 'E': 0, 'S': 1, 'W': 0}

FIRST_MOVE_OPTIONS = [(0, -1, '|7F', 'N'), (-1, 0, '-J7', 'E'), (0, 1, '|LJ', 'S'), (-1, 0, '-LF', 'E')]


def parse_data(data):
    return {
        (x, y): char
        for y, line in enumerate(data.split('\n'))
        for x, char in enumerate(line)
    }


def walk(grid):
    start_x, start_y = list(k for k, v in grid.items() if v == "S")[0]

    directions = [
        direction
        for d_x, d_y, valid_chars, direction in FIRST_MOVE_OPTIONS
        if (start_x + d_x, start_y + d_y) in grid and grid[(start_x + d_x, start_y + d_y)] in valid_chars
    ]
    direction = directions[0]

    path = {}
    steps = 0
    x, y = start_x, start_y

    while True:
        path[(x, y)] = steps
        x += D_X[direction]
        y += D_Y[direction]
        steps += 1
        if (x, y) == (start_x, start_y):
            break
        direction = DIRECTIONS[(direction, grid[(x, y)])]
    return steps, path


def part_a(data):
    grid = parse_data(data)
    steps, _path = walk(grid)
    return steps // 2


def part_b(data):
    grid = parse_data(data)

    steps, path = walk(grid)

    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    for x, y in path:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)


    solution = 0

    # digits = math.ceil(math.log10(steps))
    for y in range(min_y, max_y + 1):
        # line = ''
        windings = 0
        for x in range(min_x, max_x + 1):
            if (x, y) in path and (x, y + 1) in path:
                if path[(x, y + 1)] == (path[(x, y)] + 1) % steps:
                    windings += 1
                elif (path[(x, y + 1)] + 1) % steps == path[(x, y)]:
                    windings -= 1
            if windings != 0 and (x, y) not in path:
                solution += 1
        #         line += f' {path[(x, y)]:{digits}} ({windings:2})' if (x, y) in path else ' ' * digits + f'X ({windings:2})'
        #     else:
        #         line += f' {path[(x, y)]:{digits}} ({windings:2})' if (x, y) in path else ' ' * digits + f'. ({windings:2})'
        # print(line)

    return solution


def main():
    examples = [
        (""".....
.S-7.
.|.|.
.L-J.
.....""", 4, None),
        ("""..F7.
.FJ|.
SJ.L7
|F--J
LJ...""", 8, None),
        ("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""", None, 4),
        (""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""", None, 8),
        ("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""", None, 10)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
