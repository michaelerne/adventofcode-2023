from run_util import run_puzzle


def parse_data(input):
    return []


def part_a(input):
    data = parse_data(input)
    return 0


def part_b(input):
    data = parse_data(input)
    return 0


def main():
    examples = [
        ("""""", 1, 1)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
