from dag import DiagramDag, DiagramNode
import random
from .path import Gutter
from utils import get_edges_to_layer
import math

INITIAL_TEMPERATURE = 20
MAX_STEPS = 10

def permute(arr: list):
    n = len(arr)

    output = arr.copy()
    for i in range(n):
        swap_to = random.randint(i, n - 1)
        output[i], output[swap_to] = output[swap_to], output[i]
    return output

def temperature(time: float) -> float:
    return INITIAL_TEMPERATURE * (0.95 ** time)

def random_neighbour(arr: list) -> list:
    output = arr.copy()

    # Swap elements at two random indices
    rand_a, rand_b = random.sample(range(len(arr)), 2)
    output[rand_a], output[rand_b] = output[rand_b], output[rand_a]

    return output

def generate_paths_for_lane_assignment(gutter: Gutter, lanes: list[str], edges: list[tuple[str, str]]):
    # gutter.reset()
    pass


def assign_lanes(gutter: Gutter):
    nodes = gutter.left_layer
    dag = gutter.dag

    edges = get_edges_to_layer(dag, nodes)
    initial_lanes = permute(nodes)

    for k in range(MAX_STEPS):
        temp = temperature(1 - (k + 1)/MAX_STEPS)
