from run_util import run_puzzle


def parse_data(data):
    return [[int(x) for x in line.split()] for line in data.split('\n')]


def extrapolate(row):
    steps = [row]

    while not all([x == 0 for x in steps[-1]]):
        step = [y - x for x, y in zip(steps[-1], steps[-1][1:])]
        steps.append(step)

    for idx in range(len(steps) - 2, -1, -1):
        steps[idx].append(steps[idx][-1] + steps[idx + 1][-1])
        steps[idx].insert(0, steps[idx][0] - steps[idx + 1][0])

    return steps[0]


def part_a(data):
    data = parse_data(data)

    return sum(extrapolate(row)[-1] for row in data)


def part_b(data):
    data = parse_data(data)

    return sum(extrapolate(row)[0] for row in data)


def main():
    examples = [
        ("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""", 114, 2)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
