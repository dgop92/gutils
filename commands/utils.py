import networkx as nx

from gutils_exceptions import GUtilsException


def contains_repeated_edges(edge_list):
    edge_list = list(
        map(
            lambda t: (
                t[0],
                t[1],
            ),
            edge_list,
        )
    )
    edge_set = set(edge_list)
    return len(edge_list) != len(edge_set)


def get_graph_instance(edge_list, directed):
    repeated = contains_repeated_edges(edge_list)
    if repeated and directed:
        return nx.MultiDiGraph()
    if not repeated and directed:
        return nx.DiGraph()
    if repeated and not directed:
        return nx.MultiGraph()

    return nx.Graph()


def parse_gstring(gstring):
    try:
        components = gstring.split("-")
        edge_list, isolated_vertices, directed = map(eval, components)

        g = get_graph_instance(edge_list, directed)
        for v1, v2, weight in edge_list:
            g.add_edge(v1, v2, weight=weight)
        g.add_nodes_from(isolated_vertices)

        return g
    except Exception:
        raise GUtilsException("Invalid gstring representation")


def get_dot_languague_of_graph(g):
    pass
