import math

import parse

from run_util import run_puzzle


def parse_data(data):
    instructions_data, maps_data = data.split('\n\n')

    instructions = [
        0 if instruction == 'L' else 1
        for instruction in instructions_data
    ]
    maps = {
        source.strip(): (destination_left, destination_right)
        for source, destination_left, destination_right in parse.findall('{} = ({}, {})', maps_data)
    }

    return instructions, maps


def move(location, destination, instructions, maps):
    moves = 0

    while not location.endswith(destination):
        location = maps[location][instructions[moves % len(instructions)]]
        moves += 1

    return moves


def part_a(data):
    instructions, maps = parse_data(data)

    location, destination = 'AAA', 'ZZZ'

    return move(location, destination, instructions, maps)


def part_b(data):
    instructions, maps = parse_data(data)

    locations = [location for location in maps.keys() if location[-1] == 'A']

    cycles = [move(location, 'Z', instructions, maps) for location in locations]

    return math.lcm(*cycles)


def main():
    examples = [
        ("""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""", 2, None),
        ("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""", 6, None),
        ("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""", None, 6)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
