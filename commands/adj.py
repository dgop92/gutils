from enum import Enum

import networkx as nx
import numpy as np
import typer

from commands.draw import draw
from commands.utils import MapperOption, NotePad, get_gstring_for_graph
from core.gutils_core import GUtilsException, GUtilTyper

app = GUtilTyper(name="adj")


class EdgeType(str, Enum):
    alphabetical = "alphabetical"
    base0 = "base0"
    base1 = "base1"


def parse_matrix(str_matrix):
    lines = str_matrix.split("\n")
    # the matrix must be n x n
    n = len(lines)
    matrix = np.empty((n, n), dtype="int32")

    for i in range(n):
        line = lines[i]
        elements = line.split()
        for j in range(n):
            element = elements[j]
            matrix[i][j] = float(element)

    return matrix


def is_symmetric(a, rtol=1e-05, atol=1e-08):
    return np.allclose(a, a.T, rtol=rtol, atol=atol)


@app.command(name="adj")
def adj(
    ctx: typer.Context,
    directed: bool = typer.Option(
        False, "--directed", "-d", help="whether or not the graph is directed"
    ),
    edge_type: EdgeType = typer.Option(
        EdgeType.alphabetical, help="The representation of the nodes in the graph"
    ),
):
    """
    Given an adjancency matrix, draw the respective graph

    Input example:

    1 0 0 0 1 0
    1 1 0 0 0 1
    0 0 0 0 1 1
    0 1 1 0 0 0
    0 0 1 2 0 0

    """
    notepad = NotePad()
    if len(notepad.text_written) == 0:
        raise GUtilsException("Adjacency representation is empty")
    matrix_as_string = notepad.text_written
    matrix = parse_matrix(matrix_as_string)
    n = len(matrix)
    node_mapper_options = {
        EdgeType.alphabetical: lambda i: chr(i + 97),
        EdgeType.base0: lambda i: i,
        EdgeType.base1: lambda i: i + 1,
    }
    node_mapper = node_mapper_options[edge_type.value]

    edge_list = []

    if not directed and not is_symmetric(matrix):
        raise GUtilsException("The matrix is not symmetric, therefore is not directed")

    if not directed:
        # if a matrix is not directed we only need
        # to traverse the lower triangular matrix + main diagonal
        for i in range(n):
            for j in range(i + 1):
                element = matrix[i][j]
                node_from = node_mapper(i)
                node_to = node_mapper(j)
                for _ in range(element):
                    edge_list.append((node_from, node_to))
        graph = nx.MultiGraph(edge_list)
    else:
        for i in range(n):
            for j in range(n):
                element = matrix[i][j]
                node_from = node_mapper(i)
                node_to = node_mapper(j)
                for _ in range(element):
                    edge_list.append((node_from, node_to))
        graph = nx.MultiDiGraph(edge_list)
    typer.echo()
    typer.echo(
        typer.style(
            "be aware of self loops, cannot be draw due to overlapping",
            fg=typer.colors.YELLOW,
        )
    )
    typer.echo()
    draw(ctx, get_gstring_for_graph(graph), mapper_option=MapperOption.alphabetical)


if __name__ == "__main__":
    app()
