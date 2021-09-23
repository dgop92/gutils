import itertools
from dataclasses import dataclass
from enum import Enum
from heapq import heappop, heappush

import networkx as nx
import numpy as np
import typer

from commands.draw import draw
from commands.utils import get_gstring_for_graph, use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="mst")


@dataclass
class Edge:
    root: int
    to: int
    weight: int = 1

    def __str__(self):
        return f"({self.root}, {self.to}, {self.weight})"

    def get_original_form(self, of):
        return (
            of(self.root),
            of(self.to),
            self.weight,
        )

    def __repr__(self) -> str:
        return self.__str__()


def get_neighbors_with_weight(g, parent_index):
    neighbors = g.neighbors(parent_index)
    return map(lambda n: (n, g.get_edge_data(parent_index, n)["weight"]), neighbors)


def get_original_mst(mst_edges, original_form):
    def to_original_form(edge):
        if edge:
            return edge.get_original_form(original_form)
        else:
            return edge

    mst = list(map(to_original_form, mst_edges))
    return mst


def print_priority_queue(priority_queue, visited, original_form):
    edges = map(lambda e: e[2].get_original_form(original_form), priority_queue)
    joao_edges = set()
    for _, _, edge in priority_queue:
        if not visited[edge.to]:
            joao_edges.add(original_form(edge.to))
    # joao_edges = set(map(lambda e: original_form(e[2].to), priority_queue))
    typer.echo(f"Edges: {list(edges)}")
    typer.echo(f"Joao Edges: {joao_edges}")


def print_visited_nodes(visited, original_form):
    nodes_visited = []
    n = len(visited)
    for i in range(n):
        if visited[i]:
            nodes_visited.append(original_form(i))
    typer.echo(f"Visited: {nodes_visited}")


def prim(g, original_form, start=0):
    counter = itertools.count()
    n = g.order()
    m = n - 1
    edge_count = mst_cost = 0
    mst_edges = [None for _ in range(m)]
    visited = np.zeros(dtype="int32", shape=n)

    priority_queue = []

    def add_edges(node_index):
        visited[node_index] = 1
        neighbors = get_neighbors_with_weight(g, node_index)
        for nei in neighbors:
            if not visited[nei[0]]:
                heappush(
                    priority_queue,
                    (nei[1], next(counter), Edge(node_index, nei[0], nei[1])),
                )

    add_edges(start)
    typer.echo(typer.style("Initial PQ\n", fg=typer.colors.CYAN))
    typer.echo(f"Start: {original_form(start)}")
    print_priority_queue(priority_queue, visited, original_form)
    print_visited_nodes(visited, original_form)
    typer.echo()

    step = 1
    while len(priority_queue) != 0 and edge_count != m:
        _, _, edge = heappop(priority_queue)
        node_index = edge.to

        if visited[node_index]:
            continue

        mst_edges[edge_count] = edge
        edge_count += 1
        mst_cost += edge.weight

        typer.echo(typer.style(f"PQ step {step}\n", fg=typer.colors.CYAN))
        typer.echo(f"Pop: {original_form(node_index)}")
        add_edges(node_index)
        print_priority_queue(priority_queue, visited, original_form)
        print_visited_nodes(visited, original_form)
        original_mst = get_original_mst(mst_edges, original_form)
        typer.echo(f"MST: {original_mst}")
        typer.echo()
        step += 1

    if edge_count != m:
        return None, None

    return mst_cost, get_original_mst(mst_edges, original_form)


class AlgoType(str, Enum):
    network = "network"
    prim = "prim"


@app.command(name="mst")
@use_gstring
def mst(
    ctx: typer.Context,
    algo: AlgoType = typer.Option(AlgoType.network),
    start_index: int = typer.Option(0, "--start-index", "-s", help="start index"),
):
    """
    Find the minimum spanning tree of a graph
    """
    g = ctx.use_params["graph"]
    if algo.value == AlgoType.network:
        mst = nx.minimum_spanning_tree(g)
        gstring = get_gstring_for_graph(mst)
        draw(ctx, gstring, weighted=True, mapper_option=ctx.use_params["mapper_type"])
    else:
        func_mapper = ctx.use_params["func_mapper"]
        original_form = func_mapper["original_form"]
        to_index0 = func_mapper["to_index0"]

        new_nodes = list(map(to_index0, list(g.nodes)))
        edges = g.edges(data=True)
        new_edges = list(
            map(lambda e: (to_index0(e[0]), to_index0(e[1]), e[2]["weight"]), edges)
        )

        g.clear()
        g.add_nodes_from(new_nodes)
        g.add_weighted_edges_from(new_edges)
        _, mst_edges = prim(g, original_form, start=start_index)
        draw(
            ctx,
            f"{mst_edges}-[]-False",
            weighted=True,
            mapper_option=ctx.use_params["mapper_type"],
        )


if __name__ == "__main__":
    app()
