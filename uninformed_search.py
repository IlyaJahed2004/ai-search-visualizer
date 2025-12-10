import time
import tracemalloc
import heapq
from collections import deque
from romania_problem import neighbors,distances

# Node + expand
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = depth


def expand(node):
    children = []
    for neighbor in neighbors.get(node.state, []):
        if (node.state, neighbor) not in distances and (neighbor, node.state) not in distances:
            continue
        step = distances.get((node.state, neighbor),
                             distances.get((neighbor, node.state)))
        children.append(Node(neighbor, node, neighbor,
                        node.path_cost + step, node.depth + 1))
    return children


# Utilities
def extract_path(node):
    if not node:
        return None
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return list(reversed(path))


def path_cost_expression(path):
    if not path or len(path) < 2:
        return None
    total = 0
    terms = []
    for i in range(len(path)-1):
        w = distances.get((path[i], path[i+1]),
                          distances.get((path[i+1], path[i]), 0))
        total += w
        terms.append(str(w))
    return f"Path Cost = {' + '.join(terms)} = {total}"


def _list_has(frontier, state):
    return any(n.state == state for n in frontier)


# BFS
def BFS_with_metrics(start, goal):
    tracemalloc.start()
    t0 = time.perf_counter()

    root = Node(start)
    frontier = deque([root])
    explored = set()

    expanded_list = []
    generated_list = []
    nodes_expanded = 0
    nodes_generated = 0

    while frontier:
        node = frontier.popleft()
        expanded_list.append(node.state)

        if node.state == goal:
            t1 = time.perf_counter()
            curr, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return {
                "goal_node": node, "time": t1-t0, "peak_memory": peak,
                "nodes_expanded": nodes_expanded, "nodes_generated": nodes_generated,
                "expanded_list": expanded_list, "generated_list": generated_list
            }

        explored.add(node.state)
        nodes_expanded += 1

        for child in expand(node):
            nodes_generated += 1
            generated_list.append(child.state)
            if child.state not in explored and not _list_has(frontier, child.state):
                frontier.append(child)

    # Failure
    t1 = time.perf_counter()
    curr, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"goal_node": None, "time": t1-t0, "peak_memory": peak}


# DFS

def DFS_with_metrics(start, goal):
    tracemalloc.start()
    t0 = time.perf_counter()

    root = Node(start)
    frontier = [root]
    explored = set()

    expanded_list = []
    generated_list = []
    nodes_expanded = 0
    nodes_generated = 0

    while frontier:
        node = frontier.pop()
        expanded_list.append(node.state)

        if node.state == goal:
            t1 = time.perf_counter()
            curr, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return {
                "goal_node": node, "time": t1-t0, "peak_memory": peak,
                "nodes_expanded": nodes_expanded, "nodes_generated": nodes_generated,
                "expanded_list": expanded_list, "generated_list": generated_list
            }

        explored.add(node.state)
        nodes_expanded += 1

        children = expand(node)
        for child in reversed(children):
            nodes_generated += 1
            generated_list.append(child.state)
            if child.state not in explored and not _list_has(frontier, child.state):
                frontier.append(child)

    # Failure
    t1 = time.perf_counter()
    curr, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"goal_node": None, "time": t1-t0, "peak_memory": peak}



# UCS
def UCS_with_metrics(start, goal):
    tracemalloc.start()
    t0 = time.perf_counter()

    root = Node(start)
    frontier = []
    heapq.heappush(frontier, (root.path_cost, root))
    explored = set()

    expanded_list = []
    generated_list = []
    nodes_expanded = 0
    nodes_generated = 0

    while frontier:
        _, node = heapq.heappop(frontier)

        if node.state in explored:
            continue

        expanded_list.append(node.state)

        if node.state == goal:
            t1 = time.perf_counter()
            curr, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return {
                "goal_node": node, "time": t1-t0, "peak_memory": peak,
                "nodes_expanded": nodes_expanded, "nodes_generated": nodes_generated,
                "expanded_list": expanded_list, "generated_list": generated_list
            }

        explored.add(node.state)
        nodes_expanded += 1

        for child in expand(node):
            nodes_generated += 1
            generated_list.append(child.state)
            if child.state not in explored:
                heapq.heappush(frontier, (child.path_cost, child))

    # Failure
    t1 = time.perf_counter()
    curr, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"goal_node": None, "time": t1-t0, "peak_memory": peak}


# DLS
def DLS_with_metrics(start, goal, limit):
    tracemalloc.start()
    t0 = time.perf_counter()

    expanded_list = []
    generated_list = []
    nodes_expanded = 0
    nodes_generated = 0
    found_node = None

    def dls(node, depth, visited):
        nonlocal nodes_expanded, nodes_generated, found_node
        expanded_list.append(node.state)

        if node.state == goal:
            found_node = node
            return "FOUND"

        if depth == limit:
            return "CUTOFF"

        nodes_expanded += 1
        cutoff = False

        for child in expand(node):
            nodes_generated += 1
            generated_list.append(child.state)
            if child.state in visited:
                continue
            visited.add(child.state)
            res = dls(child, depth+1, visited)
            visited.remove(child.state)

            if res == "FOUND":
                return "FOUND"
            if res == "CUTOFF":
                cutoff = True

        return "CUTOFF" if cutoff else "FAIL"

    root = Node(start)
    outcome = dls(root, 0, {start})

    t1 = time.perf_counter()
    curr, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "goal_node": found_node, "outcome": outcome, "limit": limit,
        "time": t1-t0, "peak_memory": peak,
        "nodes_expanded": nodes_expanded, "nodes_generated": nodes_generated,
        "expanded_list": expanded_list, "generated_list": generated_list
    }

# IDS
def IDS_with_metrics(start, goal, max_limit=50):
    tracemalloc.start()
    t0 = time.perf_counter()

    total_expanded = 0
    total_generated = 0
    all_expanded = []
    all_generated = []
    peak_memory = 0
    found_node = None
    final_limit = None

    for limit in range(max_limit + 1):
        res = DLS_with_metrics(start, goal, limit)
        total_expanded += res["nodes_expanded"]
        total_generated += res["nodes_generated"]
        all_expanded.extend(res["expanded_list"])
        all_generated.extend(res["generated_list"])
        peak_memory = max(peak_memory, res["peak_memory"])

        if res["outcome"] == "FOUND":
            found_node = res["goal_node"]
            final_limit = limit
            break

    t1 = time.perf_counter()
    curr, global_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_memory = max(peak_memory, global_peak)

    return {
        "goal_node": found_node, "found_limit": final_limit,
        "time": t1-t0, "peak_memory": peak_memory,
        "nodes_expanded": total_expanded, "nodes_generated": total_generated,
        "expanded_list": all_expanded, "generated_list": all_generated
    }


# Backtracking
def Backtracking_with_metrics(start, goal):
    tracemalloc.start()
    t0 = time.perf_counter()

    expanded_list = []
    generated_list = []
    nodes_expanded = 0
    nodes_generated = 0
    found = None

    def backtrack(node, visited):
        nonlocal nodes_expanded, nodes_generated, found
        expanded_list.append(node.state)

        if node.state == goal:
            found = node
            return True

        nodes_expanded += 1

        for child in expand(node):
            nodes_generated += 1
            generated_list.append(child.state)
            if child.state in visited:
                continue
            visited.add(child.state)
            child.parent = node
            child.path_cost = node.path_cost + \
                distances.get((node.state, child.state), 0)

            if backtrack(child, visited):
                return True

            visited.remove(child.state)

        return False

    root = Node(start)
    backtrack(root, {start})

    t1 = time.perf_counter()
    curr, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "goal_node": found, "time": t1-t0, "peak_memory": peak,
        "nodes_expanded": nodes_expanded, "nodes_generated": nodes_generated,
        "expanded_list": expanded_list, "generated_list": generated_list
    }


# Bidirectional BFS
def Bidirectional_with_metrics(start, goal):
    tracemalloc.start()
    t0 = time.perf_counter()

    if start == goal:
        curr, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return {
            "goal_node": Node(start),
            "path": [start],
            "path_cost": 0,
            "time": 0,
            "nodes_expanded": 0,
            "nodes_generated": 0,
            "expanded_list": [start],
            "generated_list": [],
            "peak_memory": peak
        }

    f_frontier = deque([Node(start)])
    b_frontier = deque([Node(goal)])
    f_seen = {start: f_frontier[0]}
    b_seen = {goal: b_frontier[0]}

    expanded_list = []
    generated_list = []
    nodes_expanded = 0
    nodes_generated = 0

    meet = None
    meet_f = None
    meet_b = None

    def expand_step(frontier, seen, other, direction):
        nonlocal nodes_expanded, nodes_generated, meet, meet_f, meet_b

        if not frontier:
            return False

        node = frontier.popleft()
        expanded_list.append(node.state)
        nodes_expanded += 1

        for child in expand(node):
            nodes_generated += 1
            generated_list.append(child.state)

            if child.state in seen:
                continue

            seen[child.state] = child
            child.parent = node
            child.path_cost = node.path_cost + \
                distances.get((node.state, child.state), 0)
            frontier.append(child)

            if child.state in other:
                meet = child.state
                if direction == "f":
                    meet_f = child
                    meet_b = other[child.state]
                else:
                    meet_b = child
                    meet_f = other[child.state]
                return True

        return False

    found = False
    while f_frontier and b_frontier and not found:
        if expand_step(f_frontier, f_seen, b_seen, "f"):
            found = True
            break
        if expand_step(b_frontier, b_seen, f_seen, "b"):
            found = True
            break

    t1 = time.perf_counter()
    curr, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if not found:
        return {
            "goal_node": None, "time": t1-t0, "peak_memory": peak,
            "nodes_expanded": nodes_expanded, "nodes_generated": nodes_generated,
            "expanded_list": expanded_list, "generated_list": generated_list
        }

    # Construct path
    path_f = []
    n = meet_f
    while n:
        path_f.append(n.state)
        n = n.parent
    path_f.reverse()

    path_b = []
    n = meet_b.parent
    while n:
        path_b.append(n.state)
        n = n.parent

    full_path = path_f + path_b

    total_cost = 0
    for i in range(len(full_path) - 1):
        total_cost += distances.get(
            (full_path[i], full_path[i+1]),
            distances.get((full_path[i+1], full_path[i]), 0)
        )

    return {
        "goal_node": Node(goal, path_cost=total_cost),
        "path": full_path,
        "path_cost": total_cost,
        "time": t1-t0,
        "peak_memory": peak,
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "expanded_list": expanded_list,
        "generated_list": generated_list
    }
