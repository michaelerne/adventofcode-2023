from run_util import run_puzzle
import parse


def parse_data(input):
    data = {}
    for line in input.split('\n'):
        left, right = line.split(': ')
        game_id = int(left.split(' ')[-1])
        data[game_id] = {'reveals': []}
        max_revealed = dict()
        for reveal in right.split('; '):
            reveal_data = {}
            for show in reveal.split(', '):
                amount, color = show.split(' ')
                reveal_data[color] = int(amount)
                max_revealed[color] = max(max_revealed.get(color, -1), int(amount))
            data[game_id]['reveals'].append(reveal_data)
        data[game_id]['max'] = max_revealed
    return data


def part_a(data):
    max_possible_by_color = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    data = parse_data(data)

    sum_valid = 0
    for game_id, game_data in data.items():
        violation_found = False
        for color, max_possible in max_possible_by_color.items():
            if game_data['max'][color] > max_possible:
                violation_found = True
        if not violation_found:
            sum_valid += game_id


    return sum_valid


def part_b(data):

    data = parse_data(data)

    solution = 0
    for game_id, game_data in data.items():
        solution += game_data['max']['blue'] * game_data['max']['red'] * game_data['max']['green']

    return solution


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
