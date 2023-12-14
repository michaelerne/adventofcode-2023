from run_util import run_puzzle


def parse_data(data):
    return [list(row) for row in data.split("\n")]


def transpose(grid):
    return tuple(["".join(row) for row in zip(*grid)])


def tilt(grid, reverse_bool):
    return tuple([
        "#".join(
            "".join(fragment)
            for fragment in [
                sorted(fragment, reverse=reverse_bool) for fragment in row.split("#")
            ]
        )
        for row in grid
    ])


def calculate_load(grid):
    row_length = len(grid[0])
    return sum(
        sum(
            row_length - i
            for i, char in enumerate(row)
            if char == "O"
        )
        for row in grid
    )


def spin_cycle(grid):
    for reverse_bool in [True, False]:
        for _ in range(2):
            grid = transpose(grid)
            grid = tilt(grid, reverse_bool)

    return grid


def spin_cycles(grid):
    memo, grids = {}, {}
    counter = 1
    while (grid := spin_cycle(grid)) not in memo:
        memo[grid] = counter
        grids[counter] = grid
        counter += 1

    first_appearance = memo[grid]
    index = (1_000_000_000 - first_appearance) % (
            counter - first_appearance
    ) + first_appearance

    return transpose(grids[index])


def part_a(data):
    grid = parse_data(data)
    return calculate_load(tilt(transpose(grid), True))


def part_b(data):
    grid = parse_data(data)
    return calculate_load(spin_cycles(grid))


def main():
    examples = [
        ("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""", 136, 64)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
