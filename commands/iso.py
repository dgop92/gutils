import networkx as nx
import typer

from commands.info import info
from commands.utils import MapperOption, use_two_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="iso")


@app.command(name="iso")
@use_two_gstring
def iso(
    ctx: typer.Context,
):
    """
    Check if a graph is isomorphic to another graph
    """
    g1 = ctx.use_params["graph1"]
    g2 = ctx.use_params["graph2"]

    is_isomorphic = nx.is_isomorphic(g1, g2)

    color = typer.colors.BRIGHT_GREEN if is_isomorphic else typer.colors.BRIGHT_RED

    typer.echo(typer.style(f"The graph is isomorphic: {is_isomorphic} \n", fg=color))

    if ctx.params["info"]:
        typer.echo(typer.style("G1 info \n", fg=typer.colors.CYAN))
        ctx.params["gstring"] = ctx.params["gstring1"]
        info(ctx, ctx.params["gstring1"], mapper_option=MapperOption.alphabetical)
        typer.echo(typer.style("G2 info \n", fg=typer.colors.CYAN))
        ctx.params["gstring"] = ctx.params["gstring2"]
        info(ctx, ctx.params["gstring2"], mapper_option=MapperOption.alphabetical)


if __name__ == "__main__":
    app()
