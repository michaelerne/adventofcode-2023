from run_util import run_puzzle


def parse_data(input):
    cards = []
    for card in input.split('\n'):
        winning, play = card.split(':')[1].split('|')

        cards.append((
            {int(x) for x in winning.split(' ') if x != ''},
            {int(x) for x in play.split(' ') if x != ''}
        ))
    return cards


def part_a(input):
    cards = parse_data(input)
    solution = 0
    for winning, play in cards:
        matching = play.intersection(winning)
        if matching:
            score = 2 ** (len(matching) - 1)
        else:
            score = 0
        solution += score
    return solution


def part_b(input):
    cards = parse_data(input)
    card_by_id = {index: card for index, card in enumerate(cards)}

    copies = {index: 1 for index in card_by_id.keys()}

    for index, (winning, play) in enumerate(cards):
        matching = play.intersection(winning)
        for i in range(len(matching)):
            copies[index + i + 1] += copies[index]
    return sum(x for x in copies.values())


def main():
    examples = [
        ("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""", 13, 30)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
