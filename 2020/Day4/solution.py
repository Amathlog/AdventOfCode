from pathlib import Path
import os

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

def is_valid_first_rule(data: dict):
    return "byr" in data and \
    "iyr" in data and \
    "eyr" in data and \
    "hgt" in data and \
    "hcl" in data and \
    "ecl" in data and \
    "pid" in data

def is_valid_second_rule(data: dict):
    if "byr" not in data or not (1920 <= int(data["byr"]) <= 2002):
        return False
    
    if "iyr" not in data or not (2010 <= int(data["iyr"]) <= 2020):
        return False

    if "eyr" not in data or not (2020 <= int(data["eyr"]) <= 2030):
        return False

    if "hgt" not in data:
        return False
    
    height = data["hgt"]
    if len(height) < 4:
        return False

    metric = height[-2:]
    mesure = int(height[:-2])
    if metric != "cm" and metric != "in":
        return False

    if metric == "cm" and not (150 <= mesure <= 193):
        return False
    if metric == "in" and not (59 <= mesure <= 76):
        return False

    if "hcl" not in data or len(data["hcl"]) != 7 or data["hcl"][0] != "#":
        return False

    for c in data["hcl"][1:]:
        if not(ord('a') <= ord(c) <= ord('f')) and not (ord('0') <= ord(c) <= ord('9')):
            return False

    if "ecl" not in data or data["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False

    if "pid" not in data or len(data["pid"]) != 9:
        return False

    for c in data["pid"]:
        if not (ord('0') <= ord(c) <= ord('9')):
            return False

    return True

with entry_file.open("r") as f:
    entries = f.readlines()

all_data = [{}]
count = 0
for entry in entries:
    if entry == "\n":
        if is_valid_first_rule(all_data[-1]):
            count += 1
        all_data.append({})
        continue
    
    for item in entry[:-1].split(" "):
        key, value = item.split(":")
        all_data[-1][key] = value

print("Valid passports (first rule):", count)

count = 0
for data in all_data:
    if is_valid_second_rule(data):
        count += 1

print("Valid passports (second rule):", count)