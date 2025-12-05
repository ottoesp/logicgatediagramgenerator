import random
from ..utils import get_edges_to_layer
import math

INITIAL_TEMPERATURE = 100
FINAL_TEMPERATURE = 10**-3
MAX_STEPS_PER_NODE = 50
MAX_STEPS_TOTAL = 200

def permute(arr: list):
    n = len(arr)

    output = arr.copy()
    for i in range(n):
        swap_to = random.randint(i, n - 1)
        output[i], output[swap_to] = output[swap_to], output[i]
    return output

def temperature(time: int, alpha: float) -> float:
    return INITIAL_TEMPERATURE * (alpha ** time)

def random_arbitrary_neighbour(arr: list) -> list:
    output = arr.copy()
    # Swap elements at two random indices
    rand_a, rand_b = random.sample(range(len(arr)), k=2)
    output[rand_a], output[rand_b] = output[rand_b], output[rand_a]

    return output

def random_adj_neighbour(arr: list) -> list:
    output = arr.copy()

    # Swap elements at two random indices
    rand_idx = random.randint(0, len(arr) - 1)
    next_idx = (rand_idx + 1) % len(arr)
    output[rand_idx], output[next_idx] = output[rand_idx], output[next_idx]

    return output

def random_colliding_neighbour(arr: list, col_dict: dict[str, int], total_col: int) -> list:
    if total_col == 0:
        return random_adj_neighbour(arr)
    
    output = arr.copy()

    rand = random.uniform(0, 1)
    cumsum = 0.0
    
    swap_idx = 0
    for node in col_dict.keys():
        prob = col_dict[node]/total_col
        cumsum += prob
        if cumsum >= rand:
            swap_idx = arr.index(node)

    rand_idx = random.randint(0, len(arr) - 1)
    output[swap_idx], output[rand_idx] = output[swap_idx], output[rand_idx]

    return output

def acceptance_function(col1: int, col2: int, T: float) -> float:
    # Probability of transitioning from state 1 to state 2 given temperature T
    if col2 < col1:
        return 1.0
    else:
        return math.exp(-(col2 - col1)/T)

def calculate_collisions(gutter, lanes: list[str], edges: list[tuple[str, str]]) -> int:
    gutter.reset()
    lane_dict = {}
    for lane, node_id in enumerate(lanes):
        lane_dict[node_id] = lane
    gutter.lanes = lane_dict

    for edge in edges:
        collisions = gutter.add_path(edge[0], edge[1])

    return gutter.collisions

def get_optimal_lanes(gutter) -> list[str]:
    nodes = gutter.left_layer
    
    if len(nodes) <= 1:
        return nodes
    
    edges = get_edges_to_layer(gutter.dag, nodes)
    current_lanes = permute(nodes)
    current_collisions = calculate_collisions(gutter, current_lanes, edges) 

    steps = min(MAX_STEPS_PER_NODE * len(nodes), MAX_STEPS_TOTAL)
    alpha = (FINAL_TEMPERATURE/INITIAL_TEMPERATURE)**(1/steps)

    for k in range(steps ):
        temp = temperature(k, alpha)
        new_lanes = random_arbitrary_neighbour(current_lanes)
        new_collisions = calculate_collisions(gutter, new_lanes, edges)

        acceptance_value = acceptance_function(current_collisions, new_collisions, temp)
        if acceptance_value >= random.uniform(0, 1):

            current_lanes = new_lanes
            current_collisions = new_collisions

        if current_collisions == 0:
            break
    
    gutter.reset()
    return current_lanes
        