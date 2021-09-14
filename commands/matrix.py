from enum import Enum

import networkx as nx
import typer

from commands.utils import use_gstring
from core.gutils_core import GUtilTyper


class MatrixType(str, Enum):
    adj = "adj"
    lap = "lap"


app = GUtilTyper(name="matrix")


@app.command(name="matrix")
@use_gstring
def matrix(ctx: typer.Context, matrix_type: MatrixType):
    g = ctx.use_params["graph"]
    typer.echo(typer.style("Node list", fg=typer.colors.BRIGHT_CYAN))
    typer.echo()
    nodelist = sorted(g.nodes())
    typer.echo(nodelist)
    typer.echo()

    if matrix_type.value == matrix_type.adj:
        typer.echo(typer.style("Adjacency matrix", fg=typer.colors.BRIGHT_CYAN))
        typer.echo()
        sparse_matrix = nx.adjacency_matrix(
            g,
        )
        np_matrix = sparse_matrix.toarray()
        typer.echo(sparse_matrix)
        typer.echo()
        typer.echo(np_matrix)

    if matrix_type.value == matrix_type.lap:
        typer.echo(typer.style("Laplacian matrix", fg=typer.colors.BRIGHT_CYAN))
        typer.echo()
        sparse_matrix = nx.laplacian_matrix(g, nodelist=nodelist)
        np_matrix = sparse_matrix.toarray()
        typer.echo(sparse_matrix)
        typer.echo()
        typer.echo(np_matrix)


if __name__ == "__main__":
    app()
