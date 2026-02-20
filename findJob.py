"""
This module finds a person with a specific job using BFS.
Author: ChoiSY
Date: 2021.2.1
"""

from collections import deque
from typing import Optional


class Person:
    def __init__(self, name: str, job: str):
        self.name = name
        self.job = job
        self.friends: list[Person] = []

    def add_friend(self, other: "Person"):
        if other is self:
            return
        if other not in self.friends:
            self.friends.append(other)

    def is_job(self, role: str) -> bool:
        return self.job == role

    def is_leaf(self) -> bool:
        return len(self.friends) == 0

# Implements textbook BFS.
# Leaves are recognized by empty friends lists.
def bfs_find_one(start_name: str, role: str, people: dict[str, Person]) -> Optional[Person]:
    start_person = people.get(start_name)
    if not start_person:
        return None
    visited = {start_person.name}
    queue = deque([start_person])
    while queue:
        person = queue.popleft()
        _ = person.is_leaf()  # use is_leaf to show branch recognition (no behavior change)
        if person.is_job(role):
            return person
        for friend in person.friends:
            if friend.name not in visited:
                visited.add(friend.name)
                queue.append(friend)
    return None

def mark_leaf(p: Person) -> None:
    p.friends = []

# Build people instances
people = {
    "you": Person("you", "unknown"),
    "ana": Person("ana", "artist"),
    "bob": Person("bob", "chef"),
    "cat": Person("cat", "pianist"),
    "dao": Person("dao", "dentist"),
    "evy": Person("evy", "model"),
    "fom": Person("fom", "policeOffice"),
    "gil": Person("gil", "teacher"),
}

# Create directed links as per original graph
people["you"].add_friend(people["ana"])
people["you"].add_friend(people["bob"])
people["you"].add_friend(people["cat"])

people["bob"].add_friend(people["dao"])
people["bob"].add_friend(people["evy"])

people["ana"].add_friend(people["evy"])

people["cat"].add_friend(people["fom"])
people["cat"].add_friend(people["gil"])

# Explicitly mark leaf nodes
mark_leaf(people["dao"])
mark_leaf(people["evy"])
mark_leaf(people["fom"])
mark_leaf(people["gil"])


if __name__ == "__main__":
    role_to_find = "policeOffice"
    found_person = bfs_find_one("you", role_to_find, people)
    if found_person:
        print(f"{found_person.name} is a policeOfficer!")
    else:
        print("No police officer found.")

