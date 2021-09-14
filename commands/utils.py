from typing import Callable

import networkx as nx
import typer
from merge_args import merge_args

from core.gutils_core import GUtilsException


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


def use_gstring(
    func: Callable,
):
    @merge_args(func)
    def wrapper(
        ctx: typer.Context,
        gstring: str = typer.Argument(
            ..., help="gutils graph representation, use read for getting one"
        ),
        **kwargs,
    ):
        ctx.use_params = {"graph": parse_gstring(gstring)}
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
        ctx.use_params = {"graph1": parse_gstring(gstring1)}
        ctx.use_params["graph2"] = parse_gstring(gstring2)
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
