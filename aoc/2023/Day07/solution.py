from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
from enum import IntEnum
from aoc.common.parse_entry import parse_all

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

CardMap = {
    '2': 0,
    '3': 1,
    '4': 2,
    '5': 3,
    '6': 4,
    '7': 5,
    '8': 6,
    '9': 7,
    'T': 8,
    'J': 9,
    'Q': 10,
    'K': 11,
    'A': 12
}

class HandType(IntEnum):
    HighCard = 0,
    OnePair = 1,
    TwoPairs = 2,
    ThreeOfAKind = 3,
    FullHouse = 4,
    FourOfAKind = 5,
    FiveOfAKind = 6


class Card:
    def __init__(self, c: str, with_joker: bool) -> None:
        self.c = c
        if c == "J" and with_joker:
            self.type = -1
        else:
            self.type = CardMap[c]

    def __ne__(self, other: "Card") -> bool:
        return self.type != other.type

    def __eq__(self, other: "Card") -> bool:
        return self.type == other.type

    def __lt__(self, other: "Card") -> bool:
        return self.type <= other.type

    def __repr__(self) -> str:
        return self.c
    
class Hand:
    def __init__(self, cards: str, with_joker: bool) -> None:
        self.cards = [Card(c, with_joker) for c in cards]
        self.value: HandType = None
        self.compute_value()

    def __lt__(self, other: "Hand") -> None:
        if self.value != other.value:
            return self.value < other.value
        
        for c1, c2 in zip(self.cards, other.cards):
            if c1 != c2:
                return c1 < c2
            
        return False

    def compute_value(self) -> None:
        sorted_cards = sorted(self.cards)
        curr_type = sorted_cards[0].type
        curr_count = 1
        curr_joker = 1 if curr_type == -1 else 0
        curr_hand_type = HandType.HighCard

        for i in range(1, len(sorted_cards) + 1):
            if i == len(sorted_cards) or sorted_cards[i].type != curr_type and curr_type != -1:
                if curr_count == 2:
                    if curr_hand_type == HandType.HighCard:
                        curr_hand_type = HandType.OnePair
                    elif curr_hand_type == HandType.OnePair:
                        curr_hand_type = HandType.TwoPairs
                    elif curr_hand_type == HandType.ThreeOfAKind:
                        curr_hand_type = HandType.FullHouse
                    else:
                        assert(False)
                elif curr_count == 3:
                    if curr_hand_type == HandType.HighCard:
                        curr_hand_type = HandType.ThreeOfAKind
                    elif curr_hand_type == HandType.OnePair:
                        curr_hand_type = HandType.FullHouse
                    else:
                        assert(False)
                elif curr_count == 4:
                    curr_hand_type = HandType.FourOfAKind
                elif curr_count == 5:
                    curr_hand_type = HandType.FiveOfAKind
            
            if i == len(sorted_cards):
                break

            other_card = sorted_cards[i]
            if other_card.type == curr_type and curr_type != -1:
                curr_count += 1
            else:
                curr_count = 1
                curr_type = other_card.type

            if curr_type == -1:
                curr_joker += 1

        if curr_joker != 0:
            if curr_joker == 1:
                if curr_hand_type == HandType.HighCard:
                    curr_hand_type = HandType.OnePair
                elif curr_hand_type == HandType.OnePair:
                    curr_hand_type = HandType.ThreeOfAKind
                elif curr_hand_type == HandType.TwoPairs:
                    curr_hand_type = HandType.FullHouse
                elif curr_hand_type == HandType.ThreeOfAKind:
                    curr_hand_type =  HandType.FourOfAKind
                elif curr_hand_type == HandType.FourOfAKind:
                    curr_hand_type = HandType.FiveOfAKind
                else:
                    assert(False)
            elif curr_joker == 2:
                if curr_hand_type == HandType.HighCard:
                    curr_hand_type = HandType.ThreeOfAKind
                elif curr_hand_type == HandType.OnePair:
                    curr_hand_type = HandType.FourOfAKind
                elif curr_hand_type == HandType.ThreeOfAKind:
                    curr_hand_type =  HandType.FiveOfAKind
                else:
                    assert(False)
            elif curr_joker == 3:
                if curr_hand_type == HandType.HighCard:
                    curr_hand_type = HandType.FourOfAKind
                elif curr_hand_type == HandType.OnePair:
                    curr_hand_type = HandType.FiveOfAKind
                else:
                    assert(False)
            elif curr_joker == 4 or curr_joker == 5:
                if curr_hand_type == HandType.HighCard:
                    curr_hand_type = HandType.FiveOfAKind
                else:
                    assert(False)

        self.value = curr_hand_type

    def __repr__(self) -> str:
        return str(self.cards)


def solve(entry: List[str], with_joker: bool) -> int:
    hands_and_bids = []
    for e in entry:
        hand, bid = e.split()
        hands_and_bids.append((Hand(hand, with_joker), int(bid)))

    hands_and_bids.sort(key=lambda x: x[0])
    
    res = 0
    for i in range(len(hands_and_bids)):
        res += (i + 1) * hands_and_bids[i][1]
    
    return res


def part_one(entry: List[str]) -> int:
    return solve(entry, False)


def part_two(entry: List[str]) -> int:
    return solve(entry, True)


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))

