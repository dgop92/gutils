from heapq import heappop, heappush

import networkx as nx
import numpy as np
import typer

from commands.utils import MAX_VALUE, use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="dij")


def get_neighbors_with_weight(g, parent_index):
    neighbors = g.neighbors(parent_index)
    return map(lambda n: (n, g.get_edge_data(parent_index, n)["weight"]), neighbors)


def dij_algo(g, start_index, func_mapper):

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
        typer.echo(
            f"-> Min pair ({minValue}, {func_mapper['original_form'](parent_index)})"
        )

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
):
    """
    Dijkstra's algorithm
    """
    g: nx.Graph = ctx.use_params["graph"]
    func_mapper = ctx.use_params["func_mapper"]
    to_index0 = func_mapper["to_index0"]

    new_nodes = list(map(to_index0, list(g.nodes)))
    edges = g.edges(data=True)
    new_edges = list(
        map(lambda e: (to_index0(e[0]), to_index0(e[1]), e[2]["weight"]), edges)
    )

    g.clear()
    g.add_nodes_from(new_nodes)
    g.add_weighted_edges_from(new_edges)

    # nodelist = sorted(g.nodes())
    typer.echo()
    dij_algo(g, start_index, func_mapper=func_mapper)


if __name__ == "__main__":
    app()
