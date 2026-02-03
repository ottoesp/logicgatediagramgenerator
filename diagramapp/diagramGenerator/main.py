import sys

from .dag import DiagramDag, build_dag_from_parse_tree, insert_dummy_edges
from .diagramNode import DummyNode, RootNode
from .parseSentence import parse_sentence, ParsingError
from .autoArrange.layers import get_layers, order_layers
from .autoArrange.verticalSpacing import assign_coordinates
from .utils import *
from .render.render import render_dag

class GeneratorResponse:
    def __init__(self, ok: bool, output: str|None = None, reasons: list[str]|None = None) -> None:
        self.ok = ok
        self.output = output
        self.reasons = reasons
    
    def __repr__(self) -> str:
        if self.ok:
            return self.output # type: ignore
        else:
            return ", ".join(self.reasons) # type: ignore

def generate_diagram(sentence: str, max_width: int) -> GeneratorResponse:
    """
    Then use Kahn's algorithm ttps://en.wikipedia.org/wiki/Topological_sorting
    for topological sorting into Coffman-Grahams Algorithm https://en.wikipedia.org/wiki/Coffman%E2%80%93Graham_algorithm
    for optimal levels
    Then https://en.wikipedia.org/wiki/Layered_graph_drawing
    """

    try:
        parse_tree = parse_sentence(sentence)
    except ParsingError as e:
        return GeneratorResponse(ok=False, reasons=[e.args[0]])

    dag = build_dag_from_parse_tree(parse_tree)

    layers = get_layers(dag, max_width)

    insert_dummy_edges(dag, layers)

    ordered_layers = order_layers(dag, layers)

    layer_y_coordinates = assign_coordinates(dag, ordered_layers, 3)

    output = render_dag(dag, ordered_layers, layer_y_coordinates)
    return GeneratorResponse(ok=True, output=output)