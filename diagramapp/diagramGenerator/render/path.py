from diagramNode import DiagramNode
from .charsets import MiscVisual, LineCase
from .rendervars import *
from dag import DiagramDag
from nodeType import NodeType
import itertools

class PathCell:
    def __init__(self, x : int, y : int, value : LineCase | MiscVisual = MiscVisual.EMPTY):
        self.x = x
        self.y = y
        self.value = value

class Path:
    def __init__(self, start_node : DiagramNode, dest_node : DiagramNode):
        self.start_node = start_node
        self.dest_node = dest_node

        # x, y are the top left coordinates of the box that contains the path
        self.x = min(start_node.x, dest_node.x)
        self.y = min(start_node.y, dest_node.y)

        self.cells : list[PathCell] = []

class Gutter:
    def __init__(self, y : int, width : int, height : int, dag: DiagramDag, left_layer : list[str], right_layer : list[str]):
        self.paths : list[Path] = []
        self.y = y

        self.width = width
        self.height = height

        self.left_layer = left_layer
        self.right_layer = right_layer

        self.dag = dag

        # Initialise an empty grid to keep track of overlapping paths
        self.grid : list[list[set[str]]] = []
        for i in range(height):
            self.grid.append([])
            for j in range(width):
                self.grid[i].append(set())

        # Mapping from node ids to lane numbers
        self.lanes : dict[str, int] = {}
        self.assign_lanes()

    def enumerate_configurations(self) -> None:
        adj = self.dag.get_rev_adjacency_list()
        edges: list[tuple[DiagramNode, DiagramNode]] = []

        reduced_left: set[DiagramNode] = set()
        reduced_right: set[DiagramNode] = set()

        # Add edges to all non dummy nodes
        for left_id in self.left_layer:
            left = self.dag.get_node_by_id(left_id)

            # We have bounded the number of non-dummy nodes so we can be sure that this will be reasonably efficient
            if (left.nodeType not in [NodeType.DUMMY]): 
                reduced_left.add(left)
                for right_id in adj[left_id]:
                    right = self.dag.get_node_by_id(right_id)

                    reduced_right.add(right)
                    edges.append((left, right))
        
        lane_permutations = list(itertools.permutations(reduced_left))
    
    def assign_lanes(self):
        for i, left_node_id in enumerate(self.left_layer):
            self.lanes[left_node_id] = i

    def add_path(self, start_id : str, dest_id : str):
        start_node = self.dag.get_node_by_id(start_id)
        dest_node = self.dag.get_node_by_id(dest_id)

        offset_dest_x = dest_node.x + self.get_node_offset(start_node, dest_node)
        
        path = Path(start_node, dest_node)
        self.paths.append(path)

        lane_y = EDGE_SPACING + self.lanes[start_id]
        
        # Draw start, scanning horizontally from start node
        for y in range(lane_y):
            self.grid[start_node.x][y].add(start_id)

        # Draw vertical part, scanning vertically up or down the lane
        if (start_node.x < offset_dest_x):
             for x in range(start_node.x, offset_dest_x, 1):
                 self.grid[x][lane_y].add(start_id)
        else:
            for x in range(start_node.x, offset_dest_x, -1):
                 self.grid[x][lane_y].add(start_id)

        # Draw end, scanning horizontally from lane to dest node
        for y in range(lane_y, self.width):
            self.grid[offset_dest_x][y].add(start_id)

    def get_node_offset(self, start_node : DiagramNode, dest_node : DiagramNode) -> int:
        print(self.lanes)

        # get sibling node
        adj = self.dag.get_adjacency_list()
        start_id = start_node.get_id()

        siblings = adj[dest_node.get_id()]
        if len(siblings) == 1:
            return 0

        sibling_id, = siblings - {start_id}

        sibling_node = self.dag.get_node_by_id(sibling_id)

        start_higher = start_node.x > sibling_node.x

        if start_higher:
            max_x = start_node.x
            min_x = sibling_node.x
            higher_close = self.lanes[start_id] < self.lanes[sibling_id]
        else:
            max_x = sibling_node.x
            min_x = start_node.x
            higher_close = self.lanes[sibling_id] < self.lanes[start_id]

        offset_higher = False
        # Dest is above the two nodes and the upper node has a further lane
        if dest_node.x <= min_x and higher_close is False:
            offset_higher = True
        # Dest is below the two nodes and the upper node has a closer lane
        elif dest_node.x >= max_x and higher_close is True:
            offset_higher = True
        
        # Offset the start node if the start node is higher and we are offsetting the higher one
        if offset_higher == start_higher:
            return 1
        # Otherwise don't offset
        else:
            return 0
    
    def print_gutter(self):
        for row in self.grid:
            print()
            for cell in row:
                print(f"'{','.join(sorted(cell))}'".ljust(5), end='')
            print()
