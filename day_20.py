from collections import deque, defaultdict
from math import lcm

from run_util import run_puzzle


def parse_input(s):
    wiring = {}

    for line in s.splitlines():
        source, destinations = line.split(' -> ')
        destinations = destinations.split(', ')

        if source == 'broadcaster':
            type = None
        else:
            type = source[0]
            source = source[1:]

        wiring[source] = (type, destinations)

    memory = {}

    input_map = defaultdict(list)

    for source, (_type, destinations) in wiring.items():
        for destination in destinations:
            input_map[destination].append(source)

    for source, (module_type, _destinations) in wiring.items():
        if module_type is None:
            continue
        if module_type == '%':
            memory[source] = False
        if module_type == '&':
            memory[source] = {d: False for d in input_map[source]}

    return wiring, memory, input_map


def process_pulse(wiring, memory, source, module, signal):
    memory = memory.copy()
    generated_pulses = []
    wiring_data = wiring.get(module)
    if wiring_data is not None:
        module_type, destinations = wiring_data
        if module_type == '%':
            if not signal:
                memory[module] = not memory[module]
                for destination in destinations:
                    generated_pulses.append((module, destination, memory[module]))
        elif module_type == '&':
            state = memory[module]
            state[source] = signal
            for destination in destinations:
                generated_pulses.append((module, destination, not all(state.values())))
        elif module_type is None:
            for destination in destinations:
                generated_pulses.append((module, destination, signal))
    return generated_pulses, memory


def part_a(data):
    wiring, memory, _input_map = parse_input(data)

    count = {True: 0, False: 0}

    for _ in range(1000):
        queue = deque([(None, 'broadcaster', False)])
        while queue:
            source, module, signal = queue.popleft()

            count[signal] += 1

            generated_pulses, memory = process_pulse(wiring, memory, source, module, signal)
            queue += generated_pulses

    return count[True] * count[False]


def part_b(wiring):
    wiring, memory, input_map = parse_input(wiring)

    rx_sources = input_map[input_map['rx'][0]]

    cycle_length = {}

    cycle = 0

    while not all(rx_source in cycle_length for rx_source in rx_sources):

        cycle += 1

        queue = deque([(None, 'broadcaster', False)])
        while queue:

            source, module, signal = queue.popleft()

            if module in rx_sources and not signal:
                if module not in cycle_length:
                    cycle_length[module] = cycle

            generated_pulses, memory = process_pulse(wiring, memory, source, module, signal)
            queue += generated_pulses

    return lcm(*cycle_length.values())


def main():
    examples = [
        ("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""", 32000000, None),
        ("""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""", 11687500, None)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
