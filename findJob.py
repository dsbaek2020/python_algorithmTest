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

def visualize_people_graph(
    people: dict[str, Person],
    figsize: tuple[float, float] = (8, 8),
    layout: str = "circular",
    show_arrows: bool = True,
    node_radius: float = 0.03,
    node_color: str = "#4C78A8",
    edge_color: str = "#999999",
    font_size: int = 9,
    save_path: str | None = None,
) -> None:
    """
    Visualize the social graph represented by `people` using Matplotlib.

    - Nodes are placed using a simple layout: circular (default), grid, or hierarchical.
    - Each node is labeled as 'name\n(job)'.
    - Edges represent 'friends' (directed if show_arrows=True).
    - Hierarchical layout arranges nodes by BFS depth levels and is suitable for DAG-like graphs (diagonal edges allowed).

    Parameters:
    - people: Dict[str, Person]
    - figsize: Figure size
    - layout: 'circular', 'grid', or 'hierarchical'
    - show_arrows: If True, draw directed edges with arrowheads
    - node_radius: Circle radius for nodes
    - node_color, edge_color: Colors for nodes and edges
    - font_size: Label font size
    - save_path: If provided, save the figure to this path instead of showing
    """
    import math
    import matplotlib.pyplot as plt

    names = list(people.keys())
    n = len(names)
    if n == 0:
        print("No nodes to visualize.")
        return

    # Compute positions
    positions: dict[str, tuple[float, float]] = {}

    if layout == "circular":
        angles = [2 * math.pi * i / n for i in range(n)]
        positions = {name: (math.cos(theta), math.sin(theta)) for name, theta in zip(names, angles)}
    elif layout == "grid":
        # Simple grid layout with auto-sized columns
        cols = max(1, int(math.sqrt(n)))
        h, v = 1.0, 1.0
        for idx, name in enumerate(names):
            r = idx // cols
            c = idx % cols
            positions[name] = (c * h, -r * v)
        # Normalize to roughly fit into [-1,1] range
        if positions:
            xs = [x for x, _ in positions.values()]
            ys = [y for _, y in positions.values()]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            span_x = max(1e-9, (max_x - min_x))
            span_y = max(1e-9, (max_y - min_y))
            for k, (x, y) in positions.items():
                nx = -1 + 2 * (x - min_x) / span_x
                ny = -1 + 2 * (y - min_y) / span_y
                positions[k] = (nx, ny)
    elif layout == "hierarchical":
        # Assign BFS depth levels as y coordinate, and evenly distribute nodes in each level horizontally
        # Heuristic root: 'you' if present, else first key
        from collections import deque, defaultdict

        unvisited = set(names)
        depth_map = {}
        depth_levels = defaultdict(list)

        # Helper function to BFS from a root to assign minimal depth to reachable nodes
        def bfs_depth(root_name: str):
            queue = [root_name]
            depth_map[root_name] = 0
            unvisited.discard(root_name)
            idx = 0
            while idx < len(queue):
                curr = queue[idx]
                idx += 1
                curr_depth = depth_map[curr]
                # Add friends to queue if not visited
                for friend in people[curr].friends:
                    fname = friend.name
                    if fname not in depth_map:
                        depth_map[fname] = curr_depth + 1
                        unvisited.discard(fname)
                        queue.append(fname)

        # Process all nodes to handle disconnected components
        roots = []
        if "you" in people:
            roots.append("you")
        else:
            roots.append(names[0])
        for root in roots:
            bfs_depth(root)
        # For any remaining unvisited nodes (disconnected), assign depths by repeated BFS
        while unvisited:
            new_root = next(iter(unvisited))
            bfs_depth(new_root)

        # Group nodes by depth preserving insertion order from depth_map
        # Sort nodes by their depth and insertion order
        max_depth = max(depth_map.values()) if depth_map else 0
        for name in names:
            d = depth_map.get(name, max_depth + 1)
            depth_levels[d].append(name)

        # Assign y positions top=1.0 (depth=0), bottom=-1.0 (max depth)
        if max_depth == 0:
            # Only one level, place all at y=0
            y_positions = {0: 0.0}
        else:
            y_positions = {d: 1.0 - 2.0 * d / max_depth for d in depth_levels.keys()}

        # Assign x positions evenly spaced in [-1,1] per depth level
        for d, nodes_in_level in depth_levels.items():
            count = len(nodes_in_level)
            if count == 1:
                positions[nodes_in_level[0]] = (0.0, y_positions[d])
            else:
                for i, node_name in enumerate(nodes_in_level):
                    x = -1.0 + 2.0 * i / (count - 1)
                    positions[node_name] = (x, y_positions[d])
    else:
        raise ValueError(f"Unsupported layout: {layout}")

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    ax.axis("off")

    # Draw edges
    for src_name, src_person in people.items():
        x0, y0 = positions[src_name]
        for friend in src_person.friends:
            dst_name = friend.name
            if dst_name not in positions:
                continue
            x1, y1 = positions[dst_name]
            if show_arrows:
                ax.annotate(
                    "",
                    xy=(x1, y1),
                    xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=edge_color, lw=1.0, connectionstyle="arc3,rad=0.12"),
                )
            else:
                ax.plot([x0, x1], [y0, y1], color=edge_color, lw=1.0)

    # Draw nodes and labels
    for name, (x, y) in positions.items():
        circle = plt.Circle((x, y), radius=node_radius, color=node_color, zorder=2)
        ax.add_patch(circle)
        person = people[name]
        label = f"{person.name}\n({person.job})"
        ax.text(
            x,
            y - (node_radius + 0.03),
            label,
            ha="center",
            va="top",
            fontsize=font_size,
            color="black",
            zorder=3,
        )

    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    else:
        plt.show()

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

    # Example: visualize the graph (uncomment to use)
    visualize_people_graph(people, figsize=(7, 7), layout="circular", show_arrows=True, font_size=10)
