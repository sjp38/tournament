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
    if len(candidates) >= 1<<10:
        print('too many candidates')
        exit(1)
    for i in range(1,10):
        if len(candidates) > (1<<i) and len(candidates) <= (1<<(i + 1)):
            candidates += ['no-real-candidate'] * ((1<<(i + 1)) -
                    len(candidates))
            break

def run_game(title, candidates, rounds):
    if rounds == []:    # first game
        random.shuffle(candidates)
        add_fake_candidates(candidates)
        i = 0
        round_ = []
        while i < len(candidates):
            left = candidates[i]
            right = candidates[i + 1]
            winner = None
            if left == 'no-real-candidate':
                winner = right
            elif right == 'no-real-candidate':
                winner = left
            round_.append(Match(left, right, None))
            i += 2
        rounds.append(round_)

    match_made = False
    for round_ in rounds:
        for match in round_:
            if not match.winner:
                selection = input('1: %s\n2: %s\n' % (match.left, match.right))
                if selection == '1':
                    match.winner = match.left
                elif selection == '2':
                    match.winner = match.right
                else:
                    print('wrong selection')
                    exit(1)
                match_made = True
                break
        if match_made:
            break
    if not match_made or len(rounds[-1]) == 1:
        print('The tournament is completed')
        return rounds

    game_left = False
    for match in rounds[-1]:
        if match.winner == None:
            game_left = True
            break
    if game_left:
        return rounds

    next_round = []
    i = 0
    while i < len(rounds[-1]):
        left = rounds[-1][i].winner
        right = rounds[-1][i + 1].winner
        next_round.append(Match(left, right, None))
        i += 2
    rounds.append(next_round)
    return rounds

def print_status(title, candidates, rounds):
    print(title)
    print('candidates:', ', '.join(candidates))
    for idx, round_ in enumerate(rounds):
        print('%d round' % idx)
        for match in round_:
            print('%s vs %s (winner: %s)' % (match.left, match.right,
                match.winner if match.winner != None else 'not decided yet'))
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
    rounds = read_status(args.status)

    if args.action == 'run':
        rounds = run_game(title, candidates, rounds)
        write_status(rounds, args.status)
    elif args.action == 'status':
        print_status(title, candidates, rounds)
    else:
        print('this is impossible')
        exit(1)

if __name__ == '__main__':
    main()
