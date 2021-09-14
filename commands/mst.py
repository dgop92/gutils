import networkx as nx
import typer

from commands.draw import draw
from commands.utils import get_gstring_for_graph, use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="mst")


@app.command(name="mst")
@use_gstring
def mst(ctx: typer.Context):
    """
    Find the minimum spanning tree of a graph
    """
    g = ctx.use_params["graph"]
    mst = nx.minimum_spanning_tree(g)
    gstring = get_gstring_for_graph(mst)
    draw(ctx, gstring, weighted=True)


if __name__ == "__main__":
    app()
