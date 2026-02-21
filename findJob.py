"""
This module finds a person with a specific job using BFS.
Author: ChoiSY
Date: 2021.2.1
"""

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
    """
    Perform a Breadth-First Search (BFS) to find a person with the specified job role starting from start_name.

    BFS is a graph traversal strategy that explores all neighbors at the present depth prior to moving on to nodes at the next level.
    This approach ensures the shortest path to a person with the given job is found in terms of number of "friend" connections.

    Note: In this implementation, a Python list is used as a FIFO queue with append() for enqueue and pop(0) for dequeue.

    Parameters:
    - start_name (str): The name of the person from which the search begins.
    - role (str): The job role we are searching for.
    - people (dict[str, Person]): A dictionary mapping names to Person objects representing the social graph.

    Returns:
    - Optional[Person]: The first Person found with the matching job role, or None if no such person exists.

    Algorithm flow overview:

      Start with queue = [start_person], visited = {start_name}
               |
               v
      While queue not empty:
           dequeue person
           check if person's job == role
               if yes -> return person
           else enqueue unvisited friends and mark visited
               |
               v
      Continue until found or queue empty -> return None

    ASCII Illustration:
    
      +--------------+
      | Initialize   |
      | queue=[start]|
      | visited={start}|
      +-------+------+
              |
              v
      +-------+--------+
      | While queue:   |
      |   person = pop |
      |   if match ->  |
      |       return   |
      |   for friend in|
      |     person.friends:|
      |       if not visited:|
      |         add to queue |
      |         mark visited |
      +---------------------+
              |
              v
      +-------+--------+
      | Not found ->   |
      | return None    |
      +----------------+
    """
    # Fetch start node from people dict
    start_person = people.get(start_name)
    if not start_person:
        # If start person does not exist, return None immediately
        return None
    
    # Initialize visited set with start_person's name
    # Using set for O(1) membership checks
    visited = {start_person.name}

    # Initialize queue with start_person
    # queue is a FIFO structure for BFS traversal
    queue = [start_person]

    while queue:
        # Dequeue the person at the front of the queue
        person = queue.pop(0)

        # Check if this person has the job we're looking for
        if person.is_job(role):
            return person

        # Add all unvisited friends to queue and mark them visited
        # Marking visited here (on enqueue) prevents duplicate entries in the queue
        for friend in person.friends:
            if friend.name not in visited:
                visited.add(friend.name)
                queue.append(friend)
    # If no person with the role is found after full traversal, return None
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

