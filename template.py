from run_util import run_puzzle


def parse_data(data):
    return []


def part_a(data):
    data = parse_data(data)
    return 0


def part_b(data):
    data = parse_data(data)
    return 0


def main():
    examples = [
        ("""""", 1, 1)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
