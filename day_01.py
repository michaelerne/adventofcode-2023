from run_util import run_puzzle

DIGITS = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine'
]


def startswith_number(line: str):
    for value, digit in enumerate(DIGITS, start=1):
        if line.startswith(digit):
            return value


def parse_data(data: str):
    lines = data.split('\n')
    digit_lines = []
    for line in lines:
        digit_line = []

        for index, char in enumerate(line):
            for value, digit in enumerate(DIGITS, start=1):
                if line[index:].startswith(digit):
                    digit_line.append(value)
            if char.isnumeric():
                digit_line.append(int(char))
        digit_lines.append(digit_line)
    return digit_lines


def part_a(data):
    data = parse_data(data)
    sum = 0
    for line in data:
        number = 10 * line[0] + line[-1]
        sum += number

    return sum


def part_b(data):
    data = parse_data(data)
    sum = 0
    for line in data:
        number = 10 * line[0] + line[-1]
        sum += number

    return sum


def main():
    examples = [
        ("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""", 142, None),
        ("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""", None, 281)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
