import typer

from commands.utils import use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="minsetv")


@app.command(name="minsetv")
@use_gstring
def minsetv(ctx: typer.Context):
    """
    find the minimum covering set of vertices
    """
    g = ctx.use_params["graph"]
    degree_dict = dict(g.degree)
    temp_graph = g.copy()

    minimum_covering_vertices = []
    i = 1
    while temp_graph.size() > 0:
        max_degree_node = max(degree_dict, key=degree_dict.get)
        minimum_covering_vertices.append(max_degree_node)
        neighbors_view = temp_graph.neighbors(max_degree_node)
        neighbors = [n for n in neighbors_view]
        cover_edges = []
        for neighbor in neighbors:
            cover_edges.append((max_degree_node, neighbor))

        typer.echo(f"i = {i}")
        typer.echo(f"Node with max degree: {max_degree_node}")
        typer.echo(f"C = {minimum_covering_vertices}")
        # pattern = r"frozenset\({(\w+), (\w+)}\)"
        # cover_edges_str = re.sub(pattern, '(\g<1>,\g<2>)', str(cover_edges))
        typer.echo(f"M{i} = {cover_edges}")

        temp_graph.remove_node(max_degree_node)
        degree_dict.pop(max_degree_node)
        i += 1
        typer.echo()


if __name__ == "__main__":
    app()
