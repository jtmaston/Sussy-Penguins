import random
friendlies = ["Engineer", "Programmer", "Security Guard", "Diplomat", "Medic", "Detective"]
friendly_stats = {
    "Engineer": {
        'repair': +1,
        'technical': +1,
        'health': -2,
        'computer': 0
    },
    "Programmer": {
        'computer': +1,
        'repair': +1,
        'health': -2,
        'technical': 0
    },
    "Security Guard": {
        'health': +2,
        'repair': -1,
        'technical': -1,
        'computer': 0
    },
    "Diplomat": {
        'repair': -1,
        'technical': -1,
        'health': -1,
        'computer': -1
    },
    "Medic": {
        'repair': -2,
        'technical': -2,
        'computer': -2,
        'health': +2,
    },
    "Detective": {
        'repair': -2,
        'computer': -2,
        'health': +1,
        'technical': 0
    },
}
foes = [
    'Saboteur',
    'Politician',
    'Lobbyist',
    'Evil doctor'
]


def generate_stat_block(evil=False):
    def get_key(val, source):
        for key, value in source.items():
            if val == value:
                return key
    if not evil:
        n = random.randint(1000, 5555)
        n = [int(i) if int(i) < 5 else 5 for i in str(n)]
        modifier = {
            'health': n[0],
            'repair': n[1],
            'computer': n[2],
            'technical': n[3]
        }
        stats = {key: int(value) + 2 for (key, value) in modifier.items()}
        occupation = random.choice(friendlies)
        stats['occupation'] = occupation
        for key, value in friendly_stats[occupation].items():
            stats[key] += value

    else:
        stats = {'occupation': random.choice(foes), 'health': random.randint(5, 7)}
    return stats

