import tkinter as tk

import typer

from core.gutils_core import GUtilsException, GUtilTyper


class GraphParser:
    def __init__(self, str_representation, directed=False):
        self.str_representation = str_representation
        self.directed = directed
        self.str_edge_list = []
        self.isolated_vertices = []

    def parse(self):

        raw_lines = self.str_representation.split("\n")
        for raw_line in raw_lines:
            self.parse_line(raw_line)

    def parse_line(self, raw_line):
        vertices = raw_line.split()

        if len(vertices) == 1:
            self.isolated_vertices.append(vertices[0])
        else:
            parent, *children = vertices

            for child in children:
                try:
                    vertice, weight = child.split("|")
                except ValueError:
                    vertice, weight = child, 1

                try:
                    weight = float(weight)
                except ValueError:
                    raise GUtilsException("Weight must be a number")

                edge = (
                    parent,
                    vertice,
                    weight,
                )
                self.str_edge_list.append(edge)

    def get_gstring(self):
        g_string = f"{self.str_edge_list}-{self.isolated_vertices}-{self.directed}"
        return g_string


class NotePad(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.text_written = ""
        self.textbox = tk.Text(self, height=15, width=100)
        self.textbox.pack()
        self.submitbutton = tk.Button(self, text="OK", command=self.showinputtext)
        self.submitbutton.pack()

        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()

        positionRight = int(self.textbox.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.textbox.winfo_screenheight() / 2 - windowHeight / 2)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))
        self.mainloop()

    def showinputtext(self):
        self.text_written = self.textbox.get("1.0", "end-1c")
        self.destroy()


app = GUtilTyper(name="read")


@app.command()
def read(
    directed: bool = typer.Option(False, help="whether or not the graph is directed"),
):
    notepad = NotePad()
    if len(notepad.text_written) == 0:
        raise GUtilsException("Adjacency representation is empty")
    gparser = GraphParser(notepad.text_written, directed=directed)
    gparser.parse()
    typer.echo(gparser.get_gstring())


if __name__ == "__main__":
    app()
