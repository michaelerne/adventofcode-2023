from functools import cache

from run_util import run_puzzle


def parse_data(data):
    lines = data.split('\n')
    rows = []
    for line in lines:
        pattern, splits = line.split()
        splits = tuple(int(number) for number in splits.split(','))
        rows.append([pattern, splits])
    return rows


@cache
def count_permutations(pattern, pattern_length, splits):
    if len(splits) == 0:
        if all(c in '.?' for c in pattern):
            return 1
        return 0

    current_split, remaining_splits = splits[0], splits[1:]
    after = sum(remaining_splits) + len(remaining_splits)

    count = 0

    for before in range(pattern_length - after - current_split + 1):
        candidate = '.' * before + '#' * current_split + '.'
        if all(c_0 == '?' or c_0 == c_1 for c_0, c_1 in zip(pattern, candidate)):
            count += count_permutations(
                pattern[len(candidate):],
                pattern_length - current_split - before - 1,
                remaining_splits
            )

    return count


def part_a(data):
    rows = parse_data(data)
    solution = 0
    for pattern, splits in rows:
        solution += count_permutations(pattern, len(pattern), splits)
    return solution


def part_b(data):
    rows = parse_data(data)
    solution = 0
    for pattern, splits in rows:
        pattern = '?'.join((pattern,) * 5)
        splits = splits * 5
        solution += count_permutations(pattern, len(pattern), splits)
    return solution


def main():
    examples = [
        ("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""", 21, 525152)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
