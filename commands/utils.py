import tkinter as tk
from enum import Enum
from typing import Callable

import networkx as nx
import typer
from merge_args import merge_args

from core.gutils_core import GUtilsException

MAX_VALUE = 100_000


class NotePad(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.text_written = ""
        self.textbox = tk.Text(self, height=15, width=100)
        self.textbox.pack()
        self.submitbutton = tk.Button(self, text="OK", command=self.showinputtext)
        self.submitbutton.pack()

        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()

        positionRight = int(self.textbox.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.textbox.winfo_screenheight() / 2 - windowHeight / 2)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))
        self.mainloop()

    def showinputtext(self):
        self.text_written = self.textbox.get("1.0", "end-1c")
        self.destroy()


def contains_repeated_edges(edge_list):
    edge_list = list(
        map(
            lambda t: (
                t[0],
                t[1],
            ),
            edge_list,
        )
    )
    edge_set = set(edge_list)
    return len(edge_list) != len(edge_set)


def get_graph_instance(edge_list, directed):
    repeated = contains_repeated_edges(edge_list)
    if repeated and directed:
        return nx.MultiDiGraph()
    if not repeated and directed:
        return nx.DiGraph()
    if repeated and not directed:
        return nx.MultiGraph()

    return nx.Graph()


def parse_gstring(gstring):
    try:
        components = gstring.split("-")
        edge_list, isolated_vertices, directed = map(eval, components)

        g = get_graph_instance(edge_list, directed)
        for v1, v2, weight in edge_list:
            g.add_edge(v1, v2, weight=weight)
        g.add_nodes_from(isolated_vertices)

        return g
    except Exception:
        raise GUtilsException("Invalid gstring representation")


def to_index(u):
    return ord(u) - 97


def to_char(i):
    return chr(i + 97)


class MapperOption(str, Enum):
    alphabetical = "alphabetical"
    base0 = "base0"
    base1 = "base1"


FUNC_MAPPER_OPTIONS = {
    MapperOption.alphabetical: {
        "to_index0": to_index,
        "original_form": to_char,
    },
    MapperOption.base0: {
        "to_index0": lambda i: i,
        "original_form": lambda i: i,
    },
    MapperOption.base1: {
        "to_index0": lambda i: i - 1,
        "original_form": lambda i: i + 1,
    },
}


def use_gstring(
    func: Callable,
):
    @merge_args(func)
    def wrapper(
        ctx: typer.Context,
        gstring: str = typer.Argument(
            ..., help="gutils graph representation, use read for getting one"
        ),
        mapper_option: MapperOption = typer.Option(
            MapperOption.alphabetical, "--mapper", "-m"
        ),
        **kwargs,
    ):
        use_params = getattr(ctx, "use_params", {})
        use_params["graph"] = parse_gstring(gstring)
        use_params["func_mapper"] = FUNC_MAPPER_OPTIONS[mapper_option.value]
        ctx.use_params = use_params
        ctx.use_params["mapper_type"] = mapper_option
        return func(ctx=ctx, **kwargs)

    return wrapper


def use_two_gstring(
    func: Callable,
):
    @merge_args(func)
    def wrapper(
        ctx: typer.Context,
        gstring1: str = typer.Argument(..., help="first graph"),
        gstring2: str = typer.Argument(..., help="second graph"),
        info: bool = typer.Option(
            False, "--info", "-i", help="whether or not display info about graphs"
        ),
        **kwargs,
    ):
        use_params = getattr(ctx, "use_params", {})
        use_params["graph1"] = parse_gstring(gstring1)
        use_params["graph2"] = parse_gstring(gstring2)
        ctx.use_params = use_params
        return func(ctx=ctx, **kwargs)

    return wrapper


def get_gstring_for_graph(graph):

    edge_list = list(graph.edges(data=True))
    weighted_edge_list = []
    for edge in edge_list:
        weight = edge[2].get("weight", 1)
        weighted_edge_list.append((edge[0], edge[1], weight))

    isolated_nodes = list(nx.isolates(graph))
    is_directed = graph.is_directed()

    return f"{weighted_edge_list}-{isolated_nodes}-{is_directed}"
