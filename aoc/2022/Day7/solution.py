from typing import List, Optional, Dict
from pathlib import Path
import os
import copy

class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    @staticmethod
    def from_input(input: str) -> "File":
        size, name = input.split(" ")
        return File(name, int(size))

    def to_string(self, depth: int = 0) -> str:
        tabs = "  " * depth
        return tabs + f"- {self.name} (file, size={self.size})\n"


class Directory:
    def __init__(self, name: str, parent: Optional["Directory"] = None):
        self.name = name
        self.dirs: Dict[str, "Directory"] = {}
        self.files: Dict[str, File] = {}
        self.parent = parent
        self.cached_size = None

    def invalidate_cache(self):
        if self.cached_size is not None:
            self.cached_size = None
            if self.parent != None:
                self.parent.invalidate_cache()

    def add_dir(self, dir: "Directory"):
        assert dir != self
        if dir.name not in self.dirs:
            self.dirs[dir.name] = dir
            self.invalidate_cache()

    def remove_dir(self, dir: "Directory"):
        if dir.name in self.dir:
            del self.dirs[dir.name]
            self.invalidate_cache()

    def add_file(self, file: File):
        if file.name not in self.files:
            self.files[file.name] = file
            self.invalidate_cache()

    def remove_dir(self, file: File):
        if file.name in self.files:
            del self.files[file.name]
            self.invalidate_cache()

    @property
    def size(self):
        if self.cached_size == None:
            self.cached_size = sum((d.size for d in self.dirs.values())) + sum((f.size for f in self.files.values()))

        return self.cached_size

    def to_string(self, depth: int = 0) -> str:

        tabs = "  " * depth
        res = tabs + f"- {self.name} (dir)\n"
        for d in self.dirs.values():
            res += d.to_string(depth + 1)
        for f in self.files.values():
            res += f.to_string(depth + 1)
        
        return res


entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

root_dir = Directory("/")
current_dir = root_dir

# Parse our directories
for e in entries:
    if e == "":
        continue

    if e[0] == "$":
        # Instruction
        inst = e.split(" ") + [None]
        inst, extra = inst[1], inst[2]

        if inst == "cd":
            if extra == "/":
                current_dir = root_dir
            elif extra == "..":
                current_dir = current_dir.parent
            else:
                if extra not in current_dir.dirs:
                    current_dir.add_dir(Directory(extra, current_dir))
                current_dir = current_dir.dirs[extra]
            
        continue

    if e[0] == "d":
        _, d = e.split(" ")
        current_dir.add_dir(Directory(d, current_dir))
    else:
        current_dir.add_file(File.from_input(e))


# Then find our dirs with a given size
threshold = 100000
filter_dirs = []
dir_stack = [root_dir]

dir_to_delete = []

total_size = 70000000
update_size = 30000000
current_size = total_size - root_dir.size

while len(dir_stack) != 0:
    current = dir_stack.pop()
    if current.size <= threshold:
        filter_dirs.append(current)

    if current_size + current.size >= update_size:
        dir_to_delete.append(current)

    dir_stack.extend(current.dirs.values())
    

print(f"Part 1: Sum of all dirs of size at most {threshold}: ", sum((d.size for d in filter_dirs)))
print(f"Part 2: Size of the dir to delete: ", sorted(dir_to_delete, key=lambda x: x.size)[0].size)
