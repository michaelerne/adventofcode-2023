from run_util import run_puzzle


def parse_data(data):
    return data.replace('\n', '').split(',')


def hash(string):
    value = 0
    for char in string:
        value = ((value + ord(char)) * 17) % 256
    return value


def part_a(data):
    data = parse_data(data)
    return sum(hash(string) for string in data)


def part_b(instructions):
    instructions = parse_data(instructions)
    boxes = [dict() for _ in range(256)]

    for instruction in instructions:
        if '=' in instruction:
            label, number = instruction.split('=')
            boxes[hash(label)][label] = int(number)
        else:
            label = instruction[:-1]
            boxes[hash(label)].pop(label, None)

    solution = sum(
        box_index * lens_index * box[label]
        for box_index, box in enumerate(boxes, start=1)
        for lens_index, label in enumerate(box, start=1)
    )

    return solution


def main():
    examples = [
        ("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""", 1320, 145)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
