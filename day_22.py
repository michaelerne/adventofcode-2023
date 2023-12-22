from collections import defaultdict
from itertools import product

from run_util import run_puzzle


def parse_data(data):
    return sorted([
        tuple([int(x) for x in line.replace('~', ',').split(',')])
        for line in data.split('\n')
    ], key=lambda x: x[2])


def move_down(brick):
    return brick[0], brick[1], brick[2] - 1, brick[3], brick[4], brick[5] - 1


def positions(brick):
    return product(range(brick[0], brick[3] + 1), range(brick[1], brick[4] + 1), range(brick[2], brick[5] + 1))


def place_brick(bricks):
    occupied = {}
    fallen_bricks = []
    for brick in bricks:
        while (next_brick := move_down(brick))[2] > 0 and not any(position in occupied for position in positions(next_brick)):
            brick = next_brick

        for brick_position in positions(brick):
            occupied[brick_position] = brick
        fallen_bricks.append(brick)

    bricks_above = defaultdict(set)
    bricks_below = defaultdict(set)

    for brick in fallen_bricks:
        brick_positions = set(positions(brick))
        for brick_position in positions(move_down(brick)):
            if brick_position in occupied and brick_position not in brick_positions:
                bricks_above[occupied[brick_position]].add(brick)
                bricks_below[brick].add(occupied[brick_position])

    return fallen_bricks, bricks_above, bricks_below


def disintegrate(brick, bricks_above, bricks_below):
    falling_blocks = set()

    queue = [brick]

    while queue:
        brick = queue.pop()
        falling_blocks.add(brick)
        for parent in bricks_above[brick]:
            if not bricks_below[parent] - falling_blocks:
                queue.append(parent)

    return len(falling_blocks)


def part_a(data):
    bricks = parse_data(data)

    for brick in bricks:
        if brick[0] > brick[3] or brick[1] > brick[4] or brick[2] > brick[5]:
            print('PANIC')
    fallen_bricks, bricks_above, bricks_below = place_brick(bricks)

    return sum(disintegrate(brick, bricks_above, bricks_below) == 1 for brick in fallen_bricks)


def part_b(data):
    bricks = parse_data(data)

    fallen_bricks, bricks_above, bricks_below = place_brick(bricks)

    return sum(disintegrate(brick, bricks_above, bricks_below) - 1 for brick in fallen_bricks)


def main():
    examples = [
        ("""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""", 5, 7)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
