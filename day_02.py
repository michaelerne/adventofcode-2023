from collections import defaultdict

import parse

from run_util import run_puzzle

COLORS = ['blue', 'red', 'green']


def parse_data(input):
    data = dict()

    for (game_id, game_data) in parse.findall('Game {:d}: {}\n', input + '\n'):
        by_color = defaultdict(list)

        for reveal in game_data.split('; '):
            for match in parse.findall('{amount:d} {color:w}', reveal):
                by_color[match['color']].append(match['amount'])

        data[game_id] = {
            color: max(by_color[color])
            for color in COLORS
        }
    return data


def part_a(data):
    data = parse_data(data)

    max_possible_by_color = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    return sum(
        game_id
        for game_id, game_data in data.items()
        if all(game_data[color] <= max_possible_by_color[color] for color in COLORS)
    )


def part_b(data):
    data = parse_data(data)

    return sum(
        game_data['blue'] * game_data['red'] * game_data['green']
        for game_data in data.values()
    )


def main():
    examples = [
        ("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""", 8, 2286)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
