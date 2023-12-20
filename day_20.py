import collections
import math
from collections import deque

from run_util import run_puzzle


# def parse_data(data):
#     broadcast_destinations = {}
#     flipflops_destinations = {}
#     conjunction_sources = defaultdict(list)
#     conjunction_destinations = {}
#     destination_type = {}
#
#     names = []
#
#     first_module = data.split(' -> ')[0].replace('%', '').replace('&', '')
#     for line in data.split('\n'):
#
#         name, destination = line.split(' -> ')
#
#         if line.startswith('%'):  # flipflop
#             flipflops_destinations[name[1:]] = destination
#             destination_type[name[1:]] = 'flip-flop'
#             names.append(name[1:])
#         elif name.startswith('&'):  # conjunction
#             conjunction_destinations[name[1:]] = destination
#             destination_type[name[1:]] = 'conjunction'
#             names.append(name[1:])
#         else:  # broadcaster
#             broadcast_destinations[name] = destination.split(', ')
#             destination_type[name] = 'broadcast'
#             names.append(name)
#
#     name_to_id = {name: id for id, name in enumerate(names)}
#
#     for name, destinations in broadcast_destinations.items():
#         for destination in destinations:
#             if destination in conjunction_destinations:
#                 conjunction_sources[destination].append(name)
#     for name, destination in flipflops_destinations.items():
#         if destination in conjunction_destinations:
#             conjunction_sources[destination].append(name)
#     for name, destination in conjunction_destinations.items():
#         if destination in conjunction_destinations:
#             conjunction_sources[destination].append(name)
#
#     return destination_type, broadcast_destinations, flipflops_destinations, conjunction_destinations, conjunction_sources, name_to_id, first_module
#
# def push_button(state, destination_type, broadcast_destinations, flipflops_destinations, conjunction_destinations, conjunction_sources, name_to_id, first_module):
#     pulses_low = 0
#     pulses_high = 0
#     pulses = []
#     pulse_queue = deque([('button', False, first_module)])
#     state = [
#         [x for x in state[0]],
#         [[y for y in x] for x in state[1]]
#     ]
#
#     flipflop_ids = {name: id for id, name in enumerate(flipflops_destinations)}
#     conjunction_ids = {name: id for id, name in enumerate(conjunction_destinations)}
#     conjunction_source_ids = {destination_name: {source_name: source_id for source_id, source_name in enumerate(conjunction_sources[destination_name])} for destination_name in conjunction_sources}
#
#     while pulse_queue:
#         source_module, pulse, destination_module = pulse_queue.popleft()
#
#         # accounting
#         if pulse:
#             pulses_high += 1
#         else:
#             pulses_low += 1
#         pulses.append((source_module, pulse, destination_module))
#
#         module_type = destination_type[destination_module]
#
#         if module_type == 'flip-flop':
#             if not pulse:
#                 flipflop_id = flipflop_ids[destination_module]
#                 state[0][flipflop_id] = not state[0][flipflop_id]
#                 pulse_queue.append((destination_module, state[0][flipflop_id], flipflops_destinations[destination_module]))
#
#         elif module_type == 'conjunction':
#             conjunction_id = conjunction_ids[destination_module]
#             source_id = conjunction_source_ids[destination_module][source_module]
#             state[1][conjunction_id][source_id] = pulse
#             pulse_queue.append((destination_module, not all(state[1][conjunction_id]), conjunction_destinations[destination_module]))
#
#         elif module_type == 'broadcast':
#             for broadcast_destination in broadcast_destinations[destination_module]:
#                 pulse_queue.append((destination_module, pulse, broadcast_destination))
#
#     state = (
#         tuple(x for x in state[0]),
#         tuple(tuple(y for y in x) for x in state[1])
#     )
#     for source, pulse, destination in pulses:
#         print(f'{source} -{'high' if pulse else 'low'}-> {destination}')
#     return state, pulses_low, pulses_high
#
# def part_a(data):
#     destination_type, broadcast_destinations, flipflops_destinations, conjunction_destinations, conjunction_sources, name_to_id, first_module = parse_data(data)
#     state = (
#         tuple(False for _ in flipflops_destinations),
#         tuple(tuple(False for _ in conjunction_sources[name]) for name in conjunction_destinations)
#     )
#     count_low = 0
#     count_high = 0
#     for _ in range(1000):
#         state, pulses_low, pulses_high = push_button(state, destination_type, broadcast_destinations, flipflops_destinations, conjunction_destinations, conjunction_sources, name_to_id, first_module)
#         count_low += pulses_low
#         count_high += pulses_high
#
#     solution = count_low * count_high
#     return solution

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

    input_map = collections.defaultdict(list)

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

    return math.lcm(*cycle_length.values())


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
