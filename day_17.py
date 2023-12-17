from heapq import heappush, heappop

from run_util import run_puzzle

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_data(data):
    grid = [[int(cell) for cell in row] for row in data.split('\n')]
    return grid


def solve(grid, min_distance, max_distance):
    max_x = len(grid)
    max_y = len(grid[0])
    end = (max_x - 1, max_y - 1)
    queue = [(0, 0, 0, -1)]
    seen = set()
    costs = {}

    while queue:
        cost, x, y, disallowed_direction = heappop(queue)

        if (x, y) == end:
            return cost

        if (x, y, disallowed_direction) in seen:
            continue

        seen.add((x, y, disallowed_direction))

        for direction in range(4):

            if direction == disallowed_direction or (direction + 2) % 4 == disallowed_direction:
                continue

            cost_increase = 0

            for distance in range(1, max_distance + 1):
                d_x, d_y = DIRECTIONS[direction]
                new_x = x + d_x * distance
                new_y = y + d_y * distance

                if 0 <= new_x < max_x and 0 <= new_y < max_y:

                    cost_increase += grid[new_x][new_y]

                    if distance < min_distance:
                        continue

                    new_cost = cost + cost_increase

                    if costs.get((new_x, new_y, direction), 1_000_000_000) <= new_cost:
                        continue

                    costs[(new_x, new_y, direction)] = new_cost

                    heappush(queue, (new_cost, new_x, new_y, direction))


def part_a(data):
    grid = parse_data(data)
    return solve(grid, 1, 3)


def part_b(data):
    grid = parse_data(data)
    return solve(grid, 4, 10)


def main():
    examples = [
        ("""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""", 102, 94),
        ("""111111111111
999999999991
999999999991
999999999991
999999999991""", None, 71)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
