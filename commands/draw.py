import networkx as nx
import pyclip
import typer

from commands.utils import parse_gstring
from gutils_exceptions import GUtilsException, catch_exception

app = typer.Typer(name="draw")


@app.callback(invoke_without_command=True)
@catch_exception(GUtilsException)
def draw(
    gstring: str = typer.Argument(
        ..., help="gutils graph representation, use read for getting one"
    ),
):
    g = parse_gstring(gstring)
    typer.echo(typer.style("Dot representation \n", fg=typer.colors.CYAN))
    dot_representation = str(nx.nx_pydot.to_pydot(g))
    typer.style("Copy to clipboard!", fg=typer.colors.BRIGHT_GREEN)
    typer.echo(dot_representation)
    pyclip.copy(dot_representation)
    typer.echo(typer.style("Copy to clipboard!", fg=typer.colors.BRIGHT_GREEN))


if __name__ == "__main__":
    app()
