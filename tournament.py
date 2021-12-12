#!/usr/bin/env python3

import argparse
import os
import random

def read_description(description):
    with open(description, 'r') as f:
        description_lines = [x for x in f.read().strip().split('\n')
                if (x != '' and not x.startswith('#'))]
    if len(description_lines) < 2:
        print('wrong description')
        return None, None

    title = description_lines[0]
    candidates = description_lines[1:]
    return title, candidates

class Match:
    left = None
    right = None
    winner = None

    def __init__(self, left, right, winner):
        self.left = left
        self.right = right
        self.winner = winner

def read_matches(round_txt):
    paragraphs = [x for x in round_txt.split('\n\n')]

    matches = []
    for paragraph in paragraphs:
        lines = [line for line in paragraph.split('\n')
                if not line.startswith('#')]
        if len(lines) < 2 or len(lines) > 3:
            print('wrong status:\n%s' % paragraph)
            return None
        left = lines[0]
        right = lines[1]
        winner = None
        if len(lines) == 3:
            winner = lines[2]
            if not winner in lines[0:2]:
                print('wrong winner:\n%s' % paragraph)
        matches.append(Match(left, right, winner))
    return matches

def read_status(status):
    if not os.path.isfile(status):
        return []

    with open(status, 'r') as f:
        rounds_txt = [x for x in f.read().strip().split('\n\n\n')]

    rounds = []
    for round_txt in rounds_txt:
        rounds.append(read_matches(round_txt))
    return rounds

def write_status(rounds, status_file):
    lines = []
    for round_ in rounds:
        for match in round_:
            lines.append(match.left)
            lines.append(match.right)
            if match.winner:
                lines.append(match.winner)
            if match != round_[-1]:
                lines.append('')
        lines.append('')
        lines.append('')
    with open(status_file, 'w') as f:
        f.write('\n'.join(lines))

def add_fake_candidates(candidates):
    if len(candidates) % 2 != 0:
        candidates.append('None')

def get_losers(rounds, exception):
    losers = []
    for round_ in rounds:
        for match_ in round_:
            winner = match_.winner
            if winner:
                loser = match_.left if winner == match_.right else match_.right
                if loser in [exception, 'None']:
                    continue
                if loser in losers:
                    continue
                losers.append(loser)
    random.shuffle(losers)
    return losers

def build_first_round(candidates):
    random.shuffle(candidates)
    add_fake_candidates(candidates)
    i = 0
    round_ = []
    while i < len(candidates):
        left = candidates[i]
        right = candidates[i + 1]
        round_.append(Match(left, right, None))
        i += 2
    return round_

def build_next_round(last_round):
    next_round = []
    for i in range(0, len(last_round), 2):
        left = last_round[i].winner
        if len(last_round) > i + 1:
            right = last_round[i + 1].winner
        else:
            right = 'None'
        next_round.append(Match(left, right, None))
    return next_round

def run_game(title, candidates, rounds):
    if len(rounds) <= 0:
        print('empty rounds?')
        exit(1)

    round_ = rounds[-1]

    match_made = False
    for match in round_:
        if match.winner:
            continue
        if match.right == 'None':
            losers = get_losers(rounds, match.left)
            match.right = losers[0]
            print('%s comes up from the losers (%s)' % (
                match.right, ', '.join(losers)))
            print()

        selection = input('%s\n1. %s\n2. %s\nPlease select: ' %
                (title, match.left, match.right))
        if selection == '1':
            match.winner = match.left
        elif selection == '2':
            match.winner = match.right
        else:
            print('wrong selection')
            exit(1)
        match_made = True
        break
    if not match_made or len(round_) == 1:
        print('The tournament is completed')
        return rounds

    if match == round_[-1]:
        rounds.append(build_next_round(rounds[-1]))
    return rounds

def print_status(title, candidates, rounds):
    print(title)
    print('candidates:', ', '.join(candidates))
    losers = {}
    for idx, round_ in enumerate(rounds):
        print('%d round (%d matches)' % (idx, len(round_)))
        for match in round_:
            if match.left == 'None' and match.right == 'None':
                break
            left = match.left
            if left in losers:
                left += ' (was a loser)'

            right = match.right
            if right in losers:
                right += ' (was a loser)'

            winner = match.winner
            if winner == None:
                winner = 'not decided yet'

            print('%s vs %s (winner: %s)' % (left, right, winner))
            losers[match.left if match.winner == match.right
                    else match.right] = True
        print()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['run', 'status'],
            help='run next game or print status')
    parser.add_argument('--description', metavar='<file>',
            default='description',
            help='file containing description of the tournament')
    parser.add_argument('--status', metavar='<file>', default='status',
            help='file containing current state')
    args = parser.parse_args()

    if not os.path.isfile(args.description):
        print('description file is not found')
        exit(1)

    title, candidates = read_description(args.description)
    if title == None and candidates == None:
        exit(1)
    rounds = read_status(args.status)

    if args.action == 'run':
        if rounds == []:    # first game
            rounds.append(build_first_round(candidates))
        print('\ncurrent status:')
        print_status(title, candidates, rounds)

        rounds = run_game(title, candidates, rounds)
        write_status(rounds, args.status)
    elif args.action == 'status':
        print_status(title, candidates, rounds)
    else:
        print('this is impossible')
        exit(1)

if __name__ == '__main__':
    main()
