import typer

app = typer.Typer(name="mst")


@app.command()
def mst(graph_edge_list: str):
    typer.echo(graph_edge_list)


if __name__ == "__main__":
    app()
