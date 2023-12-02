# Solution assumes no directories are empty.

import functools
import re

SIZE_THRESHOLD = 100_000

CHANGE_DIR_REGEX = r"\$ cd (.+)"
CREATE_DIR_REGEX = r"dir (.+)"
CREATE_FILE_REGEX = r"(\d+) (.+)"

class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

class FileNode(Node):
    def __init__(self, name, parent, size):
        super().__init__(name, parent)
        self.size = size

class DirNode(Node):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.children = {}

    def add_child_dir(self, name):
        self.children[name] = DirNode(name, self)

    def add_child_file(self, name, size):
        self.children[name] = FileNode(name, self, size)

    @functools.cache
    def get_size(self):
        size = 0
        for child in self.children.values():
            if isinstance(child, DirNode):
                size += child.get_size()
            else:
                size += child.size

        return size

def resolve_cd(curr_node, target):
    if target == "/":
        return ROOT_NODE
    elif target == "..":
        return curr_node.parent
    else:
        return curr_node.children[target]

@functools.cache
def get_dirs_within(node, threshold):
    if node.get_size() <= threshold:
        yield node

    for child in node.children.values():
        if isinstance(child, DirNode):
            yield from get_dirs_within(child, threshold)

with open("input.txt") as file:
    input = file.read().splitlines()

ROOT_NODE = DirNode("/", None)

# notice curr_node is always a DirNode
curr_node = None

for line in input:
    if out := re.match(CHANGE_DIR_REGEX, line):
        curr_node = resolve_cd(curr_node, out.group(1))
    elif out := re.match(CREATE_DIR_REGEX, line):
        curr_node.add_child_dir(out.group(1))
    elif out := re.match(CREATE_FILE_REGEX, line):
        curr_node.add_child_file(out.group(2), int(out.group(1)))

smaller_dirs = get_dirs_within(ROOT_NODE, SIZE_THRESHOLD)

print(sum(dir.get_size() for dir in smaller_dirs))
