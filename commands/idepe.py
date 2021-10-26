import networkx as nx
import typer

from commands.utils import use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="idepe")


@app.command(name="idepe")
@use_gstring
def idepe(ctx: typer.Context):
    """
    find the maximal matching of the graph
    """
    g = ctx.use_params["graph"]
    max_matching = nx.maximal_matching(g)

    typer.echo(f"Edges: {g.edges}")
    typer.echo(f"Max matching: {max_matching}")


if __name__ == "__main__":
    app()
