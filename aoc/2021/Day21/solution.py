from pathlib import Path
import os
import copy
from typing import Dict, Tuple

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

######### Utilities #######
def roll_deterministic_100() -> int:
    i = 0
    while True:
        yield i + 1
        i = (i + 1) % 100


def get_update_pos_and_score(previous_pos: int, previous_score: int, roll: int) -> Tuple[int, int]:
    new_pos = (previous_pos + roll) % 10
    if new_pos == 0:
        new_pos = 10
    return new_pos, previous_score + new_pos


def get_next_player(curr_player: int) -> int:
    return (curr_player + 1) % 2


### PART 1 ###
def first_part(p1_pos: int, p2_pos: int) -> None:
    curr_player = 0
    nb_rolls = 0
    generator = roll_deterministic_100()
    player1_score, player2_score = 0, 0
    while player1_score < 1000 and player2_score < 1000:
        r = sum([generator.__next__() for _ in range(3)])
        nb_rolls += 3
        if curr_player == 0:
            p1_pos, player1_score = get_update_pos_and_score(p1_pos, player1_score, r)
        else:
            p2_pos, player2_score = get_update_pos_and_score(p2_pos, player2_score, r)

        curr_player = get_next_player(curr_player)

    final_score = player1_score if player2_score >= 1000 else player2_score
    print("First answer:", final_score * nb_rolls)


### PART 2 ###
def second_part(initial_p1_pos: int, initial_p2_pos: int, max_score: int = 21) -> None:
    # Number of parallel universe for each roll
    # We roll 3 dices with 3 faces, the possibilities for the sum of
    # those 3 rolls are here.
    parallels = {
        3: 1,
        4: 3,
        5: 6,
        6: 7,
        7: 6,
        8: 3,
        9: 1
    }

    def recursion(p1_pos: int, p1_score: int, p2_pos: int, p2_score: int, curr_player: int, cache: dict = None) -> Tuple[int, int]:
        # Keep a cache of already computed states
        if cache is None:
            cache = {}

        # Each player position and score + which turn is it is enough to
        # differientiate all the possible states.
        state = (p1_pos, p1_score, p2_pos, p2_score, curr_player)

        if state not in cache:
            # It is not in the cache yet, therefore compute it.
            if p1_score < max_score and p2_score < max_score:
                # There is no winner yet, keep rolling
                res = [0, 0]
                for r in range(3, 10):
                    if curr_player == 0:
                        new_pos, new_score = get_update_pos_and_score(p1_pos, p1_score, r)
                        temp = recursion(new_pos, new_score, p2_pos, p2_score, 1, cache)
                    else:
                        new_pos, new_score = get_update_pos_and_score(p2_pos, p2_score, r)
                        temp = recursion(p1_pos, p1_score, new_pos, new_score, 0, cache)

                    # For each roll, we compute the number of universe where player 1 and player 2 win
                    # and we multiply by the number of copy of the universe there are with this roll
                    # It is given by the dict "parallels" 
                    res[0] += temp[0] * parallels[r]
                    res[1] += temp[1] * parallels[r]

                cache[state] = tuple(res)
            else:
                # We reach the universe where one player win.
                if p1_score >= max_score:
                    cache[state] = (1, 0)
                else:
                    cache[state] = (0, 1)
            
        return cache[state]

    res = recursion(initial_p1_pos, 0, initial_p2_pos, 0, 0)
    print(f"Second answer:", max(res))


if __name__ == "__main__":
    player1_pos = int(entries[0].split(":")[-1])
    player2_pos = int(entries[1].split(":")[-1])

    first_part(player1_pos, player2_pos)
    second_part(player1_pos, player2_pos)
