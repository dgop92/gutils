import networkx as nx
import numpy as np
import typer

from commands.utils import use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="dfs")

MAX_VALUE = 100_000


def get_neighbors(matrix, i):
    neighbors = []
    n = len(matrix)
    for j in range(n):
        e = matrix[i][j]
        if e != MAX_VALUE and e != 0:
            neighbors.append(j)
    return neighbors


def dfs_algo(matrix, i):
    def dfs_recursive(i):

        if visited[i]:
            return

        visited[i] = 1
        typer.echo(i)

        neighbors = get_neighbors(matrix, i)
        for nei in neighbors:
            dfs_recursive(nei)

    visited = np.zeros(dtype="int32", shape=len(matrix))
    dfs_recursive(i)


@app.command(name="dfs")
@use_gstring
def dfs(ctx: typer.Context):
    """
    Matrices representations of a graph
    """
    g = ctx.use_params["graph"]
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
    dfs_algo(np_matrix, 0)


if __name__ == "__main__":
    app()
