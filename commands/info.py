import typer

from commands.draw import draw
from commands.utils import use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="info")


@app.command(name="info")
@use_gstring
def info(ctx: typer.Context):
    g = ctx.use_params["graph"]
    typer.echo(typer.style("General Data \n", fg=typer.colors.CYAN))
    typer.echo(f"n: {g.order()}")
    typer.echo(f"m: {g.size()}")
    typer.echo(f"edges: {g.edges}")
    typer.echo(f"vertices: {g.nodes}")

    typer.echo()
    typer.echo(typer.style("Family of degrees \n", fg=typer.colors.CYAN))
    if g.is_directed():
        typer.echo("Out degrees")
        vertices_out_degree = [(node, val) for (node, val) in g.out_degree]
        for (node, val) in vertices_out_degree:
            typer.echo(f"d({node}) = {val}")

        vertices_in_degree = [(node, val) for (node, val) in g.out_degree]
        typer.echo("In degrees")
        for (node, val) in vertices_in_degree:
            typer.echo(f"d({node}) = {val}")
    else:
        vertices_degree = [(node, val) for (node, val) in g.degree]
        for (node, val) in vertices_degree:
            print(f"d({node}) = {val}")

    typer.echo()
    draw(ctx, ctx.params["gstring"])


if __name__ == "__main__":
    app()
