from heapq import heappop, heappush

import networkx as nx
import numpy as np
import typer

from commands.utils import use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="dij")

MAX_VALUE = 100_000


def to_index(u):
    return ord(u) - 97


def to_char(i):
    return chr(i + 97)


def get_neighbors_with_weight(g, parent_index):
    neighbors = g.neighbors(parent_index)
    return map(lambda n: (n, g.get_edge_data(parent_index, n)["weight"]), neighbors)


def dij_algo(g, start_index, mas=False):

    # order is the number of vertices in a graph
    order = g.order()
    visited = np.zeros(dtype="int32", shape=order)
    prev = visited - 1

    distance = np.full(order, MAX_VALUE, dtype="int32")
    distance[start_index] = 0

    priority_queue = []
    heappush(priority_queue, (0, start_index))

    step = 0
    while len(priority_queue) != 0:
        minValue, parent_index = heappop(priority_queue)
        visited[parent_index] = 1

        step += 1
        typer.echo(typer.style(f"Step: {step}", fg=typer.colors.GREEN))
        typer.echo()
        if mas:
            typer.echo(f"-> Min pair ({minValue}, {to_char(parent_index)})")
        else:
            typer.echo(f"-> Min pair ({minValue}, {parent_index})")

        neighbors = get_neighbors_with_weight(g, parent_index)

        for neighbor in neighbors:
            neighbor_index, neighbor_weight = neighbor
            if visited[neighbor_index]:
                continue

            new_dist = distance[parent_index] + neighbor_weight
            if new_dist < distance[neighbor_index]:
                distance[neighbor_index] = new_dist
                prev[neighbor_index] = parent_index
                heappush(priority_queue, (new_dist, neighbor_index))
        typer.echo(distance)
        typer.echo()


@app.command(name="dij")
@use_gstring
def dij(
    ctx: typer.Context,
    start_index: int = typer.Option(0, "--start-index", "-s", help="start index"),
    map_ascii: bool = typer.Option(
        False, "--map-ascii", "-mas", help="map ascii for nodes. ej: a -> 0"
    ),
):
    """
    Dijkstra's algorithm
    """
    g: nx.Graph = ctx.use_params["graph"]
    if map_ascii:
        new_nodes = list(map(to_index, list(g.nodes)))
        edges = g.edges(data=True)
        new_edges = list(
            map(lambda e: (to_index(e[0]), to_index(e[1]), e[2]["weight"]), edges)
        )

        g.clear()
        g.add_nodes_from(new_nodes)
        g.add_weighted_edges_from(new_edges)

    # nodelist = sorted(g.nodes())
    typer.echo()
    dij_algo(g, start_index, mas=map_ascii)


if __name__ == "__main__":
    app()
