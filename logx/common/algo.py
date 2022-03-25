from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict
from .common_object import CustomDate, Multiple, Record


@dataclass
class Node:

    value:  Multiple = field(init=False, default=None)
    left:   Node = field(init=False, default=None)
    right:  Node = field(init=False, default=None)


@dataclass
class BinarySearch:

    """
    Custom Implementation of Binary Search Tree
    """

    traverse_result: List[Multiple] = field(init=False, default_factory=list)

    def add(self, root_node: Node, data: Multiple) -> None:
        if root_node.value == None:
            root_node.value = data
            return

        if root_node.value._date == data._date:
            return
        else:
            if data._date > root_node.value._date:
                if root_node.right != None:
                    self.add(root_node.right, data)
                else:
                    root_node.right = Node()
                    root_node.right.value = data
            else:
                if root_node.left != None:
                    self.add(root_node.left, data)
                else:
                    root_node.left = Node()
                    root_node.left.value = data

    def find(self, node: Node, date: str | CustomDate) -> Multiple:
        if type(date) == str:
            date = CustomDate(date)

        if date.system_date == node.value._date.system_date:
            print("Found!")
            return node.value
        else:
            if date.system_date > node.value._date.system_date:
                if node.right != None:
                    return self.find(node.right, date)
            else:
                if node.left != None:
                    return self.find(node.left, date)

        print("Not Found!")
        return {}

    def traverse(self, node: Node) -> None:
        if node == None:
            return

        self.traverse(node.left)
        self.traverse_result.append(node.value)
        self.traverse(node.right)


def update_process(old: Multiple, new: Multiple) -> Dict[str, List]:
    result = []

    # Copy
    old_copy = old.records.copy()
    new_copy = new.records.copy()

    # Sorting
    old_copy.sort(key = lambda x: x.trx, reverse=True)
    new_copy.sort(key = lambda x: x.trx, reverse=True)

    status = "Added" if len(old_copy) < len(new_copy) else "Remove"

    def search(data: Record, new: List) -> bool:
        for i in new:
            if i == data:
                return True
            else:
                continue

        return False

    if len(new_copy) > len(old_copy):
        for item in new_copy:
            if not search(item, old_copy):
                result.append(item)
    else:
        for item in old_copy:
            if not search(item, new_copy):
                result.append(item)

    for num, i in enumerate(result):
        result[num] = i.unpack()

    return {'operation': status, 'data': result}
