import networkx as nx
import numpy as np
import typer

from commands.utils import MAX_VALUE, use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="bfs")


def get_neighbors(matrix, i):
    neighbors = []
    n = len(matrix)
    for j in range(n):
        e = matrix[i][j]
        if e != MAX_VALUE and e != 0:
            neighbors.append(j)
    return neighbors


def bfs_algo(matrix, i, map_function):

    visited = np.zeros(dtype="int32", shape=len(matrix))

    q = []
    q.append(i)

    visited[i] = 1

    while len(q) != 0:
        i = q.pop(0)

        neighbors = get_neighbors(matrix, i)
        typer.echo(map_function(i))

        for nei in neighbors:
            if not visited[nei]:
                q.append(nei)
                visited[nei] = 1


@app.command(name="bfs")
@use_gstring
def dfs(ctx: typer.Context):
    """
    Matrices representations of a graph
    """
    g = ctx.use_params["graph"]
    func_mapper = ctx.use_params["func_mapper"]
    original_form = func_mapper["original_form"]
    typer.echo(typer.style("Node list", fg=typer.colors.BRIGHT_CYAN))
    typer.echo()
    nodelist = sorted(g.nodes())
    typer.echo(nodelist)
    typer.echo()

    typer.echo(typer.style("Adjacency matrix", fg=typer.colors.BRIGHT_CYAN))
    typer.echo()
    sparse_matrix = nx.adjacency_matrix(
        g,
    )
    np_matrix = sparse_matrix.toarray()
    typer.echo(np_matrix)
    typer.echo()
    bfs_algo(np_matrix, 0, original_form)


if __name__ == "__main__":
    app()
