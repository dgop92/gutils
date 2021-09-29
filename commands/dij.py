import re
from heapq import heappop, heappush

import networkx as nx
import numpy as np
import typer
import xlwt

from commands.utils import FUNC_MAPPER_OPTIONS, MAX_VALUE, MapperOption, use_gstring
from core.gutils_core import GUtilTyper

app = GUtilTyper(name="dij")


def get_neighbors_with_weight(g, parent_index):
    neighbors = g.neighbors(parent_index)
    return map(lambda n: (n, g.get_edge_data(parent_index, n)["weight"]), neighbors)


def dij_algo(g, start_index, func_mapper):

    # order is the number of vertices in a graph
    order = g.order()
    visited = np.zeros(dtype="int32", shape=order)
    prev = visited - 1

    distance = np.full(order, MAX_VALUE, dtype="int32")
    distance[start_index] = 0

    priority_queue = []
    heappush(priority_queue, (0, start_index))

    step = 0
    while len(priority_queue) != 0:
        minValue, parent_index = heappop(priority_queue)
        visited[parent_index] = 1

        step += 1
        typer.echo(typer.style(f"Step: {step}", fg=typer.colors.GREEN))
        typer.echo()
        typer.echo(
            f"-> Min pair ({minValue}, {func_mapper['original_form'](parent_index)})"
        )

        neighbors = get_neighbors_with_weight(g, parent_index)

        for neighbor in neighbors:
            neighbor_index, neighbor_weight = neighbor
            if visited[neighbor_index]:
                continue

            new_dist = distance[parent_index] + neighbor_weight
            if new_dist < distance[neighbor_index]:
                distance[neighbor_index] = new_dist
                prev[neighbor_index] = parent_index
                heappush(priority_queue, (new_dist, neighbor_index))
        typer.echo(prev)
        typer.echo(distance)
        typer.echo()


@app.command(name="dij")
@use_gstring
def dij(
    ctx: typer.Context,
    start_index: int = typer.Option(0, "--start-index", "-s", help="start index"),
):
    """
    Dijkstra's algorithm
    """
    g: nx.Graph = ctx.use_params["graph"]
    func_mapper = ctx.use_params["func_mapper"]
    to_index0 = func_mapper["to_index0"]

    new_nodes = list(map(to_index0, list(g.nodes)))
    edges = g.edges(data=True)
    new_edges = list(
        map(lambda e: (to_index0(e[0]), to_index0(e[1]), e[2]["weight"]), edges)
    )

    g.clear()
    g.add_nodes_from(new_nodes)
    g.add_weighted_edges_from(new_edges)

    # nodelist = sorted(g.nodes())
    typer.echo()
    dij_algo(g, start_index, func_mapper=func_mapper)


@app.command(name="dij_excel")
def dij_excel(
    dij_output: typer.FileText = typer.Option(
        ..., "--dij-output", "-do", help="The dij output to create a excel file"
    ),
    mapper_option: MapperOption = typer.Option(
        MapperOption.alphabetical,
        "--mapper",
        "-m",
        help="A map function to map indexes with something else. ex: alphabetical maps 0 -> a",
    ),
):
    """
    Dijkstra's output to excel
    """
    workbook = xlwt.Workbook()
    work_sheet = workbook.add_sheet("Dij")
    font = xlwt.Font()
    font.bold = True
    selected_style = xlwt.XFStyle()
    selected_style.font = font

    func_mapper = FUNC_MAPPER_OPTIONS[mapper_option.value]
    to_index0 = func_mapper["to_index0"]
    to_original_form = func_mapper["original_form"]

    step_pattern = r"Step: \d+"
    element_pattern = r"\w+"
    prev_pattern = r"[\w-]+"
    minpair_pattern = r"\(([\w.]+), ([\w]+)\)"

    lines = dij_output.readlines()
    n = len(lines)
    step_lines_indexes = []
    for i in range(n):
        if re.match(step_pattern, lines[i]):
            step_lines_indexes.append(i)

    # create header

    work_sheet.write(0, 0, "V")
    for j, step_index in enumerate(step_lines_indexes, start=1):
        work_sheet.write(0, j, lines[step_index])

    # fill table
    for j, step_index in enumerate(step_lines_indexes, start=1):
        min_pair_index = step_index + 2
        prev_index = step_index + 3
        element_index = step_index + 4

        match = re.search(minpair_pattern, lines[min_pair_index])
        min_node = match.group(2)
        current_node_idx = to_index0(min_node)

        elements = re.findall(element_pattern, lines[element_index])
        prev_elements = re.findall(prev_pattern, lines[prev_index])
        n = len(elements)
        for i in range(n):
            distance = int(elements[i])
            if distance == MAX_VALUE:
                distance = "infinity"
                work_sheet.write(i + 1, j, distance)
                continue

            if prev_elements[i] == "-1":
                tuple_node = min_node
            else:
                tuple_node = to_original_form(int(prev_elements[i]))

            if current_node_idx == i:
                work_sheet.write(
                    i + 1, j, f"({distance}, {tuple_node})", style=selected_style
                )
            else:
                work_sheet.write(
                    i + 1,
                    j,
                    f"({distance}, {tuple_node})",
                )

    workbook.save("excel_files/dij.xls")


if __name__ == "__main__":
    app()
