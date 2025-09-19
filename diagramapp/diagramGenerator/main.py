from logicalElementTree import DiagramNode, DiagramDag
from parseWff import  parse_wff

def generate_diagram(wff):
    dag = DiagramDag()
    root = DiagramNode("dummy")
    dag.insert_node(root)
    # Need this to not be a tree but actually have variables combining
    # Then use Kahn's algorithm https://en.wikipedia.org/wiki/Topological_sorting
    # for topological sorting into Coffman-Grahams Algorithm https://en.wikipedia.org/wiki/Coffman%E2%80%93Graham_algorithm
    # for optimal levels
    # Then https://en.wikipedia.org/wiki/Layered_graph_drawing

    parse_wff(wff, dag, root)
    dag.print_graph()

# generate_diagram("not A or (A and not B) or C")
# generate_diagram("A")
#
generate_diagram("(A or not (A and B))")