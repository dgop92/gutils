from enum import Enum

import networkx as nx
import typer

from commands.utils import use_gstring
from core.gutils_core import GUtilTyper


class MatrixType(str, Enum):
    adj = "adj"


app = GUtilTyper(name="matrix")


@app.command(name="matrix")
@use_gstring
def matrix(ctx: typer.Context, matrix_type: MatrixType):
    g = ctx.use_params["graph"]
    if matrix_type.value == matrix_type.adj:
        typer.echo(typer.style("Adjacency matrix", fg=typer.colors.BRIGHT_CYAN))
        typer.echo()
        sparse_matrix = nx.adjacency_matrix(g, nodelist=sorted(g.nodes()))
        np_matrix = sparse_matrix.toarray()
        typer.echo(sparse_matrix)
        typer.echo()
        typer.echo(np_matrix)


if __name__ == "__main__":
    app()
