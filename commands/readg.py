import typer
import tkinter as tk
import re

WEIGHTED_VERTEX_REGEX = r"[a-z]"
UNWEIGHTED_VERTEX_REGEX = r"[a-z]\d+"


class GraphParser:
    def __init__(self, str_representation):
        self.str_representation = str_representation
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
                    vertice, weight = child.split(".")
                except ValueError:
                    vertice, weight = child, 1

                self.str_edge_list.append(f"({parent}, {vertice}, {weight})")


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

        positionRight = int(
            self.textbox.winfo_screenwidth() / 2 - windowWidth / 2
        )
        positionDown = int(
            self.textbox.winfo_screenheight() / 2 - windowHeight / 2
        )

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))
        self.mainloop()

    def showinputtext(self):
        self.text_written = self.textbox.get("1.0", "end-1c")
        self.destroy()


class NotePadParser(GraphParser):
    def __init__(self):
        notepad = NotePad()
        super().__init__(notepad.text_written)


app = typer.Typer(name="readg")


@app.callback(invoke_without_command=True)
def readg():
    notepad = NotePad()
    gparser = GraphParser(notepad.text_written)
    gparser.parse()
    typer.echo(f"-> {gparser.str_edge_list}")

if __name__ == "__main__":
    app()
