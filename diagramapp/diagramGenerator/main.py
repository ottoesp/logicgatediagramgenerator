from dag import DiagramNode, DiagramDag
from parseWff import  parse_wff
from topo import kahns_topological_sort, lex_cmp

def get_layers(dag: DiagramDag):

    topo_sorted = kahns_topological_sort(dag.get_node_ids(), dag.edges)


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
    get_layers(dag)


generate_diagram("not A or (A and not A) or A")
# generate_diagram("A")
#
# generate_diagram("((A and B) or (A and C)) or (A and not C)")
# generate_diagram("( (A or not (A and B)) or (C and not B))")