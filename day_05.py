from run_util import run_puzzle


def parse_data(data):
    chunks = data.split('\n\n')
    numbers = [int(x) for x in chunks[0].split(': ')[1].split(' ') if x != '']
    mappings = [[[int(x) for x in s.split()] for s in chunk.split('\n')[1:]] for chunk in chunks[1:]]

    return numbers, mappings


def solve(mappings, ranges):
    for mapping in mappings:
        new_ranges = []
        for destination_start, source_start, range_length in mapping:
            source_end = source_start + range_length - 1

            bounded_ranges = []
            for range_start, range_end in ranges:
                if source_end < range_start or range_end < source_start:
                    bounded_ranges.append((range_start, range_end))

                else:
                    lower_bound = max(source_start, range_start)
                    upper_bound = min(source_end, range_end)

                    offset = destination_start - source_start
                    new_ranges.append((lower_bound + offset, upper_bound + offset))

                    if range_start < lower_bound:
                        bounded_ranges.append((range_start, lower_bound - 1))
                    elif range_end > upper_bound:
                        bounded_ranges.append((upper_bound + 1, range_end))

            ranges = bounded_ranges

        ranges = ranges + new_ranges
    return min(range_start for (range_start, range_end) in ranges)


def part_a(data):
    numbers, mappings = parse_data(data)
    ranges = [(start, start) for start in numbers]

    return solve(mappings, ranges)


def part_b(data):
    numbers, mappings = parse_data(data)
    ranges = [(start, start + length) for start, length in zip(numbers[::2], numbers[1::2])]

    return solve(mappings, ranges)


def main():
    examples = [
        ('''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4''', 35, 46)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
