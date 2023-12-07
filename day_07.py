from collections import Counter

from run_util import run_puzzle

MATCH_TYPES = [(1, 1, 1, 1, 1), (1, 1, 1, 2), (1, 2, 2), (1, 1, 3), (2, 3), (1, 4), (5,)]


def parse_data(data):
    hands, bids = [], []
    for line in data.split('\n'):
        hand, bid = line.split()
        hands.append(hand)
        bids.append(int(bid))
    return hands, bids


def rank_hand(hand):
    hand_list = ['J23456789TXQKA'.index(i) for i in hand]
    match_indexes = []
    if 'J' in hand:
        for joker_value in '23456789TQKA':
            counter = Counter(hand.replace('J', joker_value))
            match_type = tuple(sorted(counter.values()))
            match_indexes.append(MATCH_TYPES.index(match_type))
    else:
        counter = Counter(hand)
        match_type = tuple(sorted(counter.values()))
        match_indexes.append(MATCH_TYPES.index(match_type))

    return max(match_indexes), *hand_list

def winnings(hands, bids):
    ranked_hands = sorted((rank_hand(hand), bid) for hand, bid in zip(hands, bids))
    return sum(rank * bid for rank, (_hand, bid) in enumerate(ranked_hands, start=1))

def part_a(data):
    hands, bids = parse_data(data)

    hands = [hand.replace('J', 'X') for hand in hands]

    return winnings(hands, bids)


def part_b(data):
    hands, bids = parse_data(data)

    return winnings(hands, bids)


def main():
    examples = [
        ("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""", 6440, 5905)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
