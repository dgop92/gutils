import re

import networkx as nx
import numpy as np
import typer
import xlwt

from commands.utils import MAX_VALUE, use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="floyd")


def show_matrices(distance_matrix, path_matrix, original_form):
    typer.echo("Distance matrix\n")
    typer.echo(str(distance_matrix))
    typer.echo()
    typer.echo("Path matrix\n")
    n = len(path_matrix)
    if original_form:
        original_path_matrix = np.empty((n, n), dtype=str)
        for i in range(n):
            for j in range(n):
                original_path_matrix[i][j] = str(original_form(path_matrix[i][j]))
        typer.echo(str(original_path_matrix))
    else:
        typer.echo(str(path_matrix))
    typer.echo()


def floyd_warshall(g, original_form=None):
    n = len(g)

    distance_matrix = g.copy()
    path_matrix = np.full(
        (n, n),
        -1,
        dtype="int32",
    )

    for i in range(n):
        for j in range(n):
            path_matrix[i][j] = j

    typer.echo(typer.style("Initial matrices\n", fg=typer.colors.CYAN))
    show_matrices(distance_matrix, path_matrix, original_form)

    typer.echo(typer.style("Process\n", fg=typer.colors.CYAN))

    for k in range(n):
        for i in range(n):
            for j in range(n):
                new_dist = distance_matrix[i][k] + distance_matrix[k][j]
                if new_dist < distance_matrix[i][j]:
                    distance_matrix[i][j] = new_dist
                    path_matrix[i][j] = k

        typer.echo(typer.style(f"Iteration K = {k}\n", fg=typer.colors.GREEN))
        show_matrices(distance_matrix, path_matrix, original_form)

    return distance_matrix, path_matrix


@app.command(name="floyd")
@use_gstring
def floyd(ctx: typer.Context):
    """
    floyd-warshall algorithm
    """
    g = ctx.use_params["graph"]
    original_form = ctx.use_params["func_mapper"]["original_form"]
    nodelist = sorted(g.nodes())
    matrix = nx.to_numpy_array(g, dtype="int32", nodelist=nodelist)
    n = matrix.shape[0]
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i][j] == 0:
                matrix[i][j] = MAX_VALUE

    floyd_warshall(matrix, original_form)


@app.command(name="floyd_excel")
def floyd_excel(
    floyd_output: typer.FileText = typer.Option(
        ..., "--floyd-output", "-fo", help="The floyd output to create a excel file"
    ),
    cast_int: bool = typer.Option(True, "--casint", "-c", help="cast vertices to int"),
):
    """
    floyd-warshall output to excel
    """
    workbook = xlwt.Workbook()
    work_sheet = workbook.add_sheet("Floyd")

    i = 0
    BASE_COLUMN = 0

    element_pattern = r"\w+"

    lines = floyd_output.readlines()
    for line in lines:

        if line.find("[") != -1:
            elements = re.findall(element_pattern, line)
            n = len(elements)
            for j in range(n):
                element = elements[j]
                if cast_int:
                    element = int(element)
                work_sheet.write(i, BASE_COLUMN + j + 1, element)
        else:
            work_sheet.write(i, BASE_COLUMN, line)

        i += 1

    workbook.save("excel_files/floyd.xls")


if __name__ == "__main__":
    app()
