from operator import lt, gt

from run_util import run_puzzle

OPS = {
    '>': gt,
    '<': lt
}

BOUNDARY = 4001
POSSIBLE_NUMBERS = set(range(1, BOUNDARY))


def get_lambda_part(category, operator, value):
    return lambda part: OPS[operator](part[category], value)


def get_set(operator, value):
    if operator == '>':
        return POSSIBLE_NUMBERS - set(range(1, value + 1))
    else:
        return POSSIBLE_NUMBERS - set(range(value, BOUNDARY))


def parse_data(s):
    workflow_data, parts_data = s.split('\n\n')

    workflows = {}
    workflow_data = workflow_data.replace('}', '')

    for line in workflow_data.split('\n'):
        name, rule_data = line.split('{')

        rules = []

        for rule in rule_data.split(','):
            if ':' in rule:
                condition, destination_workflow = rule.split(':')
                category = condition[0]
                operator = condition[1]
                value = int(condition[2:])
                rules.append(
                    (
                        get_lambda_part(category, operator, value),
                        destination_workflow,
                        category,
                        get_set(operator, value)
                    )
                )
            else:
                # rules.append(rule)
                rules.append(
                    (
                        None,
                        rule,
                        None,
                        None,
                    )
                )

        workflows[name] = rules

    parts = []
    for line in parts_data.split('\n'):
        part = {}
        for category_line in line[1:-1].split(','):
            category, value = category_line.split('=')
            part[category] = int(value)
        parts.append(part)

    return workflows, parts


def examine(workflows, part, workflow_name='in'):
    if workflow_name == 'A':
        return sum(part.values())
    elif workflow_name == 'R':
        return 0

    for condition, destination_workflow, *_ in workflows[workflow_name]:

        if condition is None:
            return examine(workflows, part, destination_workflow)
        else:
            if condition(part):
                return examine(workflows, part, destination_workflow)


def part_a(s):
    workflows, parts = parse_data(s)

    answer = sum(examine(workflows, part) for part in parts)

    return answer


def combinations(workflows, workflow_name, xmas):
    if workflow_name == 'A':
        product = 1
        for values in xmas.values():
            product *= len(values)
        return product
    if workflow_name == 'R':
        return 0

    count = 0

    for _, destination_workflow, category, possible in workflows[workflow_name]:
        if possible is not None:

            accepted = xmas[category] & possible
            if len(accepted):
                count += combinations(workflows, destination_workflow, {k: accepted if k == category else v for k, v in xmas.items()})
            xmas[category] = xmas[category] - accepted

        else:
            count += combinations(workflows, destination_workflow, xmas)

    return count


def part_b(s):
    workflows, _ = parse_data(s)

    answer = combinations(workflows, 'in', {k: set(range(1, 4001)) for k in 'xmas'})

    return answer


def main():
    examples = [
        ("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""", 19114, 167409079868000)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
