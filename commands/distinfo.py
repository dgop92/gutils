import networkx as nx
import typer

from commands.utils import use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="distinfo")


@app.command(name="distinfo")
@use_gstring
def distinfo(
    ctx: typer.Context,
    source: str = typer.Option(None, "--source", "-s", help="u node for min path"),
    target: str = typer.Option(None, "--to", "-t", help="v node for min path"),
    weighted: bool = typer.Option(
        False, "--weighted", "-w", help="whether or not the graph is weighted"
    ),
):
    """
    Distance info
    """
    g = ctx.use_params["graph"]

    if source and target:
        source = int(source) if source.isdigit() else source
        target = int(target) if target.isdigit() else target
        typer.echo(typer.style(f"d({source}, {target}) \n", fg=typer.colors.CYAN))
        weight_keyword = "weight" if weighted else None
        min_path = nx.shortest_path(
            g, source=source, target=target, weight=weight_keyword
        )
        min_path_lenght = len(min_path) - 1
        typer.echo(f"Min Path: {min_path}")
        typer.echo(f"Lenght: {min_path_lenght}")
        if weighted:
            cost = 0
            for i in range(min_path_lenght):
                cost += g.get_edge_data(min_path[i], min_path[i + 1])["weight"]
            typer.echo(f"Cost: {cost}")
    else:

        if weighted:
            spath = dict(nx.shortest_path_length(g, weight="weight"))
        else:
            spath = None

        typer.echo(typer.style("Eccentricities \n", fg=typer.colors.CYAN))
        eccentricities = nx.eccentricity(g, sp=spath)

        for (node, ecce) in eccentricities.items():
            typer.echo(f"e({node}) = {ecce}")

        typer.echo()

        typer.echo(typer.style("Diameter \n", fg=typer.colors.CYAN))
        diameter = nx.diameter(g, e=eccentricities)
        typer.echo(f"Diam(G) = {diameter}")

        typer.echo()

        typer.echo(typer.style("Radius \n", fg=typer.colors.CYAN))
        radius = nx.radius(g, e=eccentricities)
        typer.echo(f"r(G) = {radius}")


if __name__ == "__main__":
    app()
