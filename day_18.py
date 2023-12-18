from run_util import run_puzzle

DIRECTIONS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0)
}

NUMBER_TO_DIRECTION = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U'
}


def parse_data(data):
    part_a = []
    part_b = []
    lines = data.split('\n')
    for line in lines:
        direction, steps, color_string = line.split(' ')
        part_a.append((direction, int(steps)))

        direction = NUMBER_TO_DIRECTION[int(color_string[-2:-1])]
        steps = int(color_string[2:-2], 16)

        part_b.append((direction, int(steps)))
    return part_a, part_b


def walk(instructions):
    x = y = 0
    edges = [(x, y)]
    perimeter = 0
    for direction, steps in instructions:
        d_x, d_y = DIRECTIONS[direction]
        x += d_x * steps
        y += d_y * steps
        edges.append((x, y))
        perimeter += steps
    return edges, perimeter


def shoelace(edges, perimeter):
    enclosed_area = sum(
        (x_1 - x_2) * (y_1 + y_2)
        for (x_1, y_1), (x_2, y_2) in zip(edges, edges[1:])
    )
    return perimeter // 2 + enclosed_area // 2 + 1


def part_a(data):
    instructions, _ = parse_data(data)
    edges, perimeter = walk(instructions)
    return shoelace(edges, perimeter)


def part_b(data):
    _, instructions = parse_data(data)
    edges, perimeter = walk(instructions)
    return shoelace(edges, perimeter)


def main():
    examples = [
        ("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""", 62, 952408144115)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
