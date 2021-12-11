from pathlib import Path
import os

class Entry:
    def __init__(self, raw_str: str):
        interval, letter, password = raw_str.split(' ')
        self.min_count, self.max_count = (int(x) for x in interval.split('-'))
        self.letter = letter[0]
        self.password = password

    def is_valid_first_rule(self):
        count = 0
        for c in self.password:
            if c == self.letter:
                count += 1
        
        return self.min_count <= count <= self.max_count

    # We suppose that the password will always have at least self.max_count characters.
    # There is no indication what to do if that's not the case, so it's not handled.
    def is_valid_second_rule(self):
        assert len(self.password) >= self.max_count
        return (self.password[self.min_count-1] == self.letter) ^ (self.password[self.max_count-1] == self.letter)

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = [Entry(s) for s in f.readlines()]

count = 0
for entry in entries:
    if entry.is_valid_first_rule():
        count += 1

print("Valid passwords with first rule:", count)

count = 0
for entry in entries:
    if entry.is_valid_second_rule():
        count += 1

print("Valid passwords with second rule:", count)