from run_util import run_puzzle


def parse_data(data):
    return [[[char for char in line] for line in chunk.split('\n')] for chunk in data.split('\n\n')]


def transpose(grid):
    return [list(i) for i in zip(*grid)]


def check_grid(grid, allowed_smudges):
    num_rows = len(grid)
    num_cols = len(grid[0])

    for column in range(num_cols - 1):
        non_matches = 0
        for remaining_columns in range(num_cols):
            left = column - remaining_columns
            right = column + 1 + remaining_columns
            if 0 <= left < right < num_cols:
                for row in range(num_rows):
                    if grid[row][left] != grid[row][right]:
                        non_matches += 1
        if non_matches == allowed_smudges:
            return column + 1
    return 0


def solve(data, allowed_smudges=0):
    return sum(
        check_grid(grid, allowed_smudges) + 100 * check_grid(transpose(grid), allowed_smudges)
        for grid in data
    )


def part_a(data):
    data = parse_data(data)
    return solve(data)


def part_b(data):
    data = parse_data(data)
    return solve(data, allowed_smudges=1)


def main():
    examples = [
        ("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""", 405, 400)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
