from run_util import run_puzzle


def parse_data(data):
    return data.split('\n')


def update_position(position, direction):
    return position[0] + direction[0], position[1] + direction[1]


def modulo_position(position, grid_size):
    return position[0] % grid_size, position[1] % grid_size


def part_a(data):
    grid = parse_data(data)
    return possible_positions(grid, 64)


def part_b(data):
    grid = parse_data(data)
    return possible_positions(grid, 26501365)


def possible_positions(grid, steps):
    # great implementation by Julian Neff (https://github.com/neffjulian/advent_of_code_2023/blob/main/day21.py)
    grid_size = len(grid)

    traversable = {(x, y) for x in range(grid_size) for y in range(grid_size) if grid[x][y] in '.S'}
    start = next((x, y) for x in range(grid_size) for y in range(grid_size) if grid[x][y] == 'S')
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited_positions, new_positions, position_cache = {start}, {start}, {0: 1}
    grids, remainder = divmod(steps, grid_size)
    for step in range(1, remainder + 2 * grid_size + 1):
        visited_positions, new_positions = new_positions, {
            new_position
            for position in new_positions
            for direction in directions
            if (new_position := update_position(position, direction)) not in visited_positions
               and modulo_position(new_position, grid_size) in traversable
        }
        position_cache[step] = len(new_positions) + (position_cache[step - 2] if step > 1 else 0)
    additional_distance = position_cache[remainder + 2 * grid_size] + position_cache[remainder] - 2 * position_cache[remainder + grid_size]
    accumulated_distance = position_cache[remainder + 2 * grid_size] - position_cache[remainder + grid_size]
    answer = position_cache[remainder + 2 * grid_size] + (grids - 2) * (2 * accumulated_distance + (grids - 1) * additional_distance) // 2
    return answer


def main():
    examples = []
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
