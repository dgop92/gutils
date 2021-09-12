import typer

from commands.utils import parse_gstring
from gutils_exceptions import GUtilsException, catch_exception

app = typer.Typer(name="info")


@app.callback(invoke_without_command=True)
@catch_exception(GUtilsException)
def info(
    gstring: str = typer.Argument(
        ..., help="gutils graph representation, use read for getting one"
    )
):
    g = parse_gstring(gstring)
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


if __name__ == "__main__":
    app()
