import matplotlib.pyplot as plt
import networkx as nx
import typer

from commands.utils import use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="plane")


def draw_plane(vertices_points, edges):
    plt.title("Plane Graph", fontsize=19)
    plt.tick_params(axis="both", which="major", labelsize=9)

    for v, point in vertices_points.items():
        plt.scatter(point[0], point[1], s=10)
        plt.annotate(v, point)

    for edge in edges:
        start, end = zip(vertices_points[edge[0]], vertices_points[edge[1]])
        plt.plot(start, end)

    plt.show()


@app.command(name="plane")
@use_gstring
def plane(ctx: typer.Context):
    """
    Check if graph is planar, and if it is planner, draw a plane representation
    """
    g = ctx.use_params["graph"]
    is_planar, emmbeding = nx.check_planarity(g)
    color = typer.colors.BRIGHT_GREEN if is_planar else typer.colors.BRIGHT_RED
    typer.echo(typer.style(f"The graph is planar: {is_planar} \n", fg=color))

    if emmbeding:
        vp = nx.combinatorial_embedding_to_pos(emmbeding)
        draw_plane(vp, list(g.edges))


if __name__ == "__main__":
    app()
