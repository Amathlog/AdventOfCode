from pathlib import Path
import os

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

def get_data_fron_entry(entry: str):
    row = int('0b' + entry[:7].replace('F', '0').replace('B', '1'), 2)
    column = int('0b' + entry[7:].replace('L', '0').replace('R', '1'), 2)
    return row, column, row * 8 + column

highest_id = 0
seat_ids = []
for entry in entries:
    _, __, seat_id = get_data_fron_entry(entry)
    seat_ids.append(seat_id)
    if seat_id > highest_id:
        highest_id = seat_id

print("Highest id:", highest_id)

seat_ids = sorted(seat_ids)
for i in range(1, len(seat_ids)):
    if seat_ids[i] - seat_ids[i-1] != 1:
        print("Your seat id:", seat_ids[i-1] + 1)
        break
