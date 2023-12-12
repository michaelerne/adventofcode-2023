from functools import cache

from run_util import run_puzzle


def parse_data(data, copies=1):
    lines = data.split('\n')
    rows = []
    for line in lines:
        pattern, splits = line.split()
        splits = tuple(int(number) for number in splits.split(','))

        pattern = '?'.join((pattern,) * copies)
        splits = splits * copies

        rows.append([pattern, splits])
    return rows


@cache
def count_permutations(pattern, groups):
    if len(pattern) == 0:
        if len(groups) == 0:
            return 1
        else:
            return 0

    if pattern[0] == "#":
        if len(groups) == 0 or len(pattern) < groups[0] or any(c == "." for c in pattern[:groups[0]]):
            return 0
        if len(groups) > 1:
            if len(pattern) < groups[0] + 1 or pattern[groups[0]] == "#":
                return 0
            return count_permutations(pattern[groups[0] + 1:], groups[1:])
        else:
            return count_permutations(pattern[groups[0]:], groups[1:])

    if pattern[0] == ".":
        return count_permutations(pattern.strip("."), groups)

    if pattern[0] == "?":
        return count_permutations(pattern.replace("?", ".", 1), groups) + count_permutations(pattern.replace("?", "#", 1), groups)


def part_a(data):
    rows = parse_data(data)
    return sum(count_permutations(pattern, splits) for pattern, splits in rows)


def part_b(data):
    rows = parse_data(data, copies=5)
    return sum(count_permutations(pattern, splits) for pattern, splits in rows)


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
