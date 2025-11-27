from diagramNode import DiagramNode
from .charsets import MiscVisual, LineCase
from .rendervars import *
from dag import DiagramDag
from nodeType import NodeType
from .marchingLines import ml_lookup
from .charsets import default_charset
from utils import generate_empty_grid
from .laneAssignment import get_optimal_lanes

class PathCell:
    def __init__(self, x : int, y : int, value : LineCase | MiscVisual = MiscVisual.EMPTY):
        self.x = x
        self.y = y
        self.value = value

    def __repr__(self):
        return f'({self.x},{self.y}).{self.value.name}'

class Path:
    def __init__(self, start_node : DiagramNode, dest_node : DiagramNode, gutter):
        self.start_node = start_node
        self.dest_node = dest_node
        self.gutter = gutter

        # x, y are the top left coordinates of the box that contains the path
        self.x = min(start_node.x, dest_node.x)
        self.y = min(start_node.y, dest_node.y)

        self.cells : set[PathCell] = set()
    
    def generate_path(self):
        lane_y = EDGE_Y_SPACING + self.gutter.lanes[self.start_node.get_id()]
        offset_dest_x = self.dest_node.x + self.gutter.get_node_offset(self.start_node, self.dest_node)

        # Draw start, scanning horizontally from start node
        for y in range(lane_y):
            self.add_path_cell(self.start_node.x, y)

        # Draw vertical part, scanning vertically up or down the lane
        if (self.start_node.x < offset_dest_x):
             for x in range(self.start_node.x, offset_dest_x, 1):
                 self.add_path_cell(x, lane_y)
        else:
            for x in range(self.start_node.x, offset_dest_x, -1):
                 self.add_path_cell(x, lane_y,)

        # Draw end, scanning horizontally from lane to dest node
        for y in range(lane_y, self.gutter.width):
            self.add_path_cell(offset_dest_x, y)
    
    def add_path_cell(
            self, x: int, y: int,
            value : LineCase | MiscVisual = MiscVisual.EMPTY
    ) -> None:
        self.cells.add(PathCell(x, y, value))

class Gutter:
    def __init__(self, y : int, width : int, height : int, dag: DiagramDag, left_layer : list[str], right_layer : list[str]):
        self.paths : list[Path] = []
        self.y = y

        self.width = width
        self.height = height

        self.left_layer = left_layer
        self.right_layer = right_layer

        self.dag = dag
        
        self.collisions = 0

        # Initialise an empty grid to keep track of overlapping paths
        self.grid : list[list[set[str]]] = []
        for i in range(height):
            self.grid.append([])
            for j in range(width):
                self.grid[i].append(set())

        # Mapping from node ids to lane numbers
        self.lanes : dict[str, int] = {}
        self.assign_lanes()

    def reset(self):
        self.collisions = 0
        self.paths = []

        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = set()

        self.lanes = dict()

    def assign_lanes(self):
        optimal_lanes = get_optimal_lanes(self)
        for lane, node_id in enumerate(optimal_lanes):
            self.lanes[node_id] = lane

    def add_path(self, start_id : str, dest_id : str) -> int:
        start_node = self.dag.get_node_by_id(start_id)
        dest_node = self.dag.get_node_by_id(dest_id)
        
        path = Path(start_node, dest_node, self)
        self.paths.append(path)

        path.generate_path()

        collisions = 0
        for cell in path.cells:
            grid_cell = self.grid[cell.x][cell.y]
            if len(grid_cell) > 0 and start_id not in grid_cell:
                collisions += 1
            grid_cell.add(path.start_node.get_id())

        self.collisions += collisions
        return collisions

    def get_node_offset(self, start_node : DiagramNode, dest_node : DiagramNode) -> int:
        # get sibling node
        adj = self.dag.get_adjacency_list()
        start_id = start_node.get_id()

        siblings = adj[dest_node.get_id()] # Siblings includes start_id
        if len(siblings) == 1:
            return 0

        sibling_id, = siblings - {start_id} # Unpack the node that is not start

        sibling_node = self.dag.get_node_by_id(sibling_id)

        start_higher = start_node.x < sibling_node.x

        if start_higher:
            max_x = start_node.x
            min_x = sibling_node.x
            higher_close = self.lanes[start_id] < self.lanes[sibling_id]
        else:
            max_x = sibling_node.x
            min_x = start_node.x
            higher_close = self.lanes[sibling_id] < self.lanes[start_id]

        offset_higher = False
        if max_x > dest_node.x and min_x > dest_node.x and not higher_close:
            offset_higher = True
        elif max_x <= dest_node.x and min_x <= dest_node.x and higher_close:
            offset_higher = True
        
        offset_start = offset_higher == start_higher
        return 1 if offset_start else 0

    def get_cell_relation(self, source_id: str, x: int, y:int, overlapping: bool):
        cell = self.grid[x][y]
        if len(cell) == 0:
            return '0'
        elif source_id in cell:
            return 'M'
        elif overlapping:
            return 'Y'
        else:
            return '0'

    def get_ml_code(self, source_id: str, x: int, y:int):
        code = ""

        overlapping = False
        # Check centre
        if len(self.grid[x][y]) > 1:
            code += 'Y'
            overlapping = True
        else:
            code += '0'

        # Check above
        if x == 0: 
            code += '0'
        else:
            code += self.get_cell_relation(source_id, x - 1, y, overlapping)

        # Check right
        if y == (self.width - 1):
            code += 'M'
        else:
            code += self.get_cell_relation(source_id, x, y + 1, overlapping)

        # Check bottom
        if x == (self.height - 1):
            code += '0'
        else:
            code += self.get_cell_relation(source_id, x + 1, y, overlapping)
        
        # Check left
        if y == 0:
            code += 'M'
        else:
            code += self.get_cell_relation(source_id, x, y - 1, overlapping)

        return code

    """
    TODO work what cases are breaking and fix them
    """
    def render_path(self, path: Path, charset: dict[LineCase | NodeType | MiscVisual, str] = default_charset):
        block = generate_empty_grid(self.width, self.height, " ")
        for cell in path.cells: # Need to fix marching lines
            try:
                cell.value = ml_lookup[self.get_ml_code(path.start_node.get_id(), cell.x, cell.y)]
            except KeyError:
                cell.value = LineCase.ERROR
            block[cell.x][cell.y] = charset[cell.value]

        return "\n".join(["".join(row) for row in block])

    def print_gutter(self):
        for row in self.grid:
            print()
            for cell in row:
                print(f"'{','.join(sorted(cell))}'".ljust(6), end='')
            print()
