import networkx as nx
import numpy as np
import typer

from commands.utils import use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="floyd")

MAX_VALUE = 100_000


def show_matrices(distance_matrix, path_matrix):
    typer.echo("Distance matrix\n")
    typer.echo(str(distance_matrix))
    typer.echo()
    typer.echo("Path matrix\n")
    typer.echo(str(path_matrix))
    typer.echo()


def floyd_warshall(g):
    n = len(g)

    distance_matrix = g.copy()
    path_matrix = np.full(
        (n, n),
        -1,
        dtype="int32",
    )

    for i in range(n):
        for j in range(n):
            path_matrix[i][j] = j

    typer.echo(typer.style("Initial matrices\n", fg=typer.colors.CYAN))
    show_matrices(distance_matrix, path_matrix)

    typer.echo(typer.style("Process\n", fg=typer.colors.CYAN))

    for k in range(n):
        for i in range(n):
            for j in range(n):
                new_dist = distance_matrix[i][k] + distance_matrix[k][j]
                if new_dist < distance_matrix[i][j]:
                    distance_matrix[i][j] = new_dist
                    path_matrix[i][j] = k

        typer.echo(typer.style(f"Iteration K = {k}\n", fg=typer.colors.GREEN))
        show_matrices(distance_matrix, path_matrix)

    return distance_matrix, path_matrix


@app.command(name="floyd")
@use_gstring
def floyd(ctx: typer.Context):
    """
    floyd-warshall algorithm
    """
    g = ctx.use_params["graph"]
    nodelist = sorted(g.nodes())
    matrix = nx.to_numpy_array(g, dtype="int32", nodelist=nodelist)
    n = matrix.shape[0]
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i][j] == 0:
                matrix[i][j] = MAX_VALUE

    floyd_warshall(matrix)


if __name__ == "__main__":
    app()
