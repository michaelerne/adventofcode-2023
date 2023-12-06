from functools import reduce
from operator import mul

from run_util import run_puzzle


def parse_data(input):
    # Time:      7  15   30
    # Distance:  9  40  200
    time_line, distance_line = input.split('\n')
    races = (
        [int(x) for x in time_line.split(':')[1].split()],
        [int(x) for x in distance_line.split(':')[1].split()]
    )
    return races


def get_ways_to_win(time, distance):
    lowest_win = 0
    highest_win = time

    approx_step = int(time ** 0.5)

    while (time - lowest_win) * lowest_win <= distance:
        lowest_win += approx_step
    while (time - lowest_win) * lowest_win > distance:
        lowest_win -= 1
    lowest_win += 1

    while (time - highest_win) * highest_win <= distance:
        highest_win -= approx_step
    while (time - highest_win) * highest_win > distance:
        highest_win += 1
    highest_win -= 1

    return highest_win - lowest_win + 1


def part_a(input):
    times, distances = parse_data(input)
    return reduce(mul, [get_ways_to_win(time, distance) for time, distance in zip(times, distances)], 1)


def part_b(input):
    times, distances = parse_data(input)
    time = int("".join([str(x) for x in times]))
    distance = int("".join([str(x) for x in distances]))

    return get_ways_to_win(time, distance)


def main():
    examples = [
        ("""Time:      7  15   30
Distance:  9  40  200""", 288, None)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
