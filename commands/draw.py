import networkx as nx
import pyclip
import typer

from commands.utils import use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="draw")


@app.command(name="draw")
@use_gstring
def draw(
    ctx: typer.Context,
    weighted: bool = typer.Option(
        False, "--weighted", "-w", help="whether or not the graph is weighted"
    ),
):
    g = ctx.use_params["graph"]
    typer.echo(typer.style("Dot representation \n", fg=typer.colors.CYAN))

    dot_graph = nx.nx_pydot.to_pydot(g)
    if weighted:
        dot_edges = dot_graph.get_edge_list()
        for edge in dot_edges:
            edge.set_label(edge.get_weight())

    dot_representation = str(dot_graph)
    typer.style("Copy to clipboard!", fg=typer.colors.BRIGHT_GREEN)
    typer.echo(dot_representation)
    pyclip.copy(dot_representation)
    typer.echo(typer.style("Copy to clipboard!", fg=typer.colors.BRIGHT_GREEN))


if __name__ == "__main__":
    app()
