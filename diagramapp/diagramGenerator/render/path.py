from diagramNode import DiagramNode
from .charsets import MiscVisual, LineCase
from .rendervars import *
from dag import DiagramDag

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
    def __init__(self, x : int, y : int, width : int, height : int, dag: DiagramDag):
        self.paths : list[Path] = []
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.dag = dag

        # Initialise an empty grid to keep track of overlapping paths
        self.grid : list[list[set[str]]] = []
        for i in range(height):
            self.grid.append([])
            for j in range(width):
                self.grid[i].append(set())

        # Mapping from node ids to lane numbers
        self.next_lane = 0
        self.lanes : dict[str, int] = {}

    def add_path(self, start_id : str, dest_id : str):
        start_node = self.dag.get_node_by_id(start_id)
        dest_node = self.dag.get_node_by_id(dest_id)

        if start_id not in self.lanes.keys():
            self.lanes[start_id] = self.next_lane
            self.next_lane += 1
        lane = self.lanes[start_id]
        
        path = Path(start_node, dest_node)
        self.paths.append(path)

        lane_y = EDGE_SPACING + lane
        
        # Draw start, scanning horizontally from start node
        for y in range(lane_y):
            self.grid[start_node.x][y].add(start_id)

        # Draw vertical part, scanning vertically up or down the lane
        if (start_node.x < dest_node.x):
             for x in range(start_node.x, dest_node.x, 1):
                 self.grid[x][lane_y].add(start_id)
        else:
            for x in range(start_node.x, dest_node.x, -1):
                 self.grid[x][lane_y].add(start_id)

        # Draw end, scanning horizontally from lane to dest node
        for y in range(lane_y, self.width):
            self.grid[dest_node.x][y].add(start_id)

    def get_node_offset(self, start_node : DiagramNode, dest_node : DiagramNode) -> int:
        # get sibling nodes
        adj = self.dag.get_adjacency_list()
        siblings = list(adj[dest_node.get_id()])

        # order sibling nodes
        siblings.sort(key=lambda sib_id : self.dag.get_node_by_id(sib_id).x)

        return siblings.index(start_node.get_id())
    
    def print_gutter(self):
        for row in self.grid:
            print()
            for cell in row:
                print(f"{','.join(sorted(cell))}".ljust(3), end='')
